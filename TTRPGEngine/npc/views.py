import os
import zipfile
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.management import call_command
from .models import *
from .forms import ContentSourceSelectionForm

# Create your views here.

def Rooster(request):
    return render(request, "character_select.html")


def character(request):
    return render(request, "character.html")

def ContentManager(request):
    # Get or create user's content profile
    profile, created = UserContentProfile.objects.get_or_create(user=request.user)

    # Handle form submission
    if request.method == 'POST':
        form = ContentSourceSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            selected_sources = form.cleaned_data['sources']
            profile.active_sources.set(selected_sources)
            messages.success(request, "Your content preferences have been updated.")
            return redirect('content_manager')
    else:
        form = ContentSourceSelectionForm(user=request.user, initial={
            'sources': profile.active_sources.all()
        })

    # Get available sources (installed data packs)
    installed_packs = DataPack.objects.filter(is_installed=True)
    available_sources = DataSource.objects.filter(
        id__in=installed_packs.values('source')
    )

    context = {
        'form': form,
        'installed_sources': available_sources,
        'active_sources': profile.active_sources.all(),
    }
    return render(request, 'content_manager.html', context)


@permission_required('content.install_datapack', raise_exception=True)
def install_pack(request, pack_id):
    if request.method == 'POST' and request.FILES.get('pack_file'):
        pack_file = request.FILES['pack_file']

        try:
            # Verify it's a valid ZIP file
            with zipfile.ZipFile(pack_file) as z:
                # Check for required files
                if 'metadata.json' not in z.namelist():
                    messages.error(request, "LSC file is missing metadata.json")
                    return redirect('content_manager')

                # Read metadata
                with z.open('metadata.json') as f:
                    metadata = json.load(f)

                # Get or create the content source
                source, created = DataSource.objects.get_or_create(
                    name=metadata.get('source_name', 'Unknown'),
                    defaults={
                        'abbreviation': metadata.get('source_abbr', 'UNK'),
                        'description': metadata.get('description', ''),
                        'version': metadata.get('version', '1.0'),
                        'is_srd': metadata.get('is_srd', False),
                        'is_core': metadata.get('is_core', False),
                    }
                )

            # Save the pack file
            pack = DataPack(
                source=source,
                file=pack_file,
                checksum=metadata.get('checksum', ''),
                metadata=metadata
            )
            pack.save()

            # Extract the pack
            if pack.extract_to_fixtures():
                # Load the fixtures
                with transaction.atomic():
                    for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, 'data_packs', 'fixtures')):
                        if filename.endswith('.json'):
                            fixture_path = os.path.join(settings.MEDIA_ROOT, 'data_packs', 'fixtures', filename)
                            call_command('loaddata', fixture_path)

                pack.is_installed = True
                pack.installed_at = timezone.now()
                pack.save()
                messages.success(request, f"Successfully installed {source.name} content pack")
            else:
                messages.error(request, "Failed to extract content pack")
                pack.delete()

        except (zipfile.BadZipFile, json.JSONDecodeError) as e:
            messages.error(request, f"Invalid LSC file: {str(e)}")

        return redirect('content_manager')

    return redirect('content_manager')


@permission_required('content.export_datapack', raise_exception=True)
def export_pack(request, source_id):
    source = get_object_or_404(DataSource, pk=source_id)

    # Get all models that belong to this source
    # You'll need to implement this based on your actual models
    fixtures = []
    for model in source.related_models.all():  # You'll need to set up this relationship
        fixtures.append(f'path/to/fixtures/{model._meta.model_name}.json')

    # Create temp directory
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    output_path = os.path.join(temp_dir, f'{source.abbreviation.lower()}_pack.lsc')

    # Create the pack
    pack = DataPack(source=source)  # Don't save, just using for methods
    if pack.create_lsc_from_fixtures(fixtures, output_path):
        # Serve the file for download
        with open(output_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'

        # Clean up
        os.remove(output_path)
        return response

    messages.error(request, "Failed to create content pack")
    return redirect('content_manager')