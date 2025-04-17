from django.contrib import admin
from django.urls import path
from django.contrib.contenttypes.admin import GenericStackedInline
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
import nested_admin
from .models import *
from .utils.pack_utils import create_lsc_file, get_fixture_paths_for_source

# Register your models here.

class AbilityInLine(admin.TabularInline):
    model = NPCAbility
    extra = 0


class HPInLine(admin.TabularInline):
    model = NPCHP
    extra = 0


class InspirationInLine(admin.StackedInline):
    model = NPCInspiration
    extra = 0


class FeaturesInLine(admin.StackedInline):
    model = NPCFeatures
    extra = 0


class EquipmentInLine(admin.StackedInline):
    model = NPCEquipment
    extra = 0


class ProficienciesInLine(admin.StackedInline):
    model = NPCProficiencies
    extra = 0


class OriginInLine(admin.StackedInline):
    model = NPCOrigin
    extra = 0


class ProgressionInLine(admin.StackedInline):
    model = NPCClassProgression
    extra = 0


class DescriptionInLine(admin.StackedInline):
    model = NPCDescription
    extra = 0

class RelationInLine(admin.StackedInline):
    model = NPCFeatOriginRelation

@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ["name","player"]

    inlines = [AbilityInLine, HPInLine, InspirationInLine, EquipmentInLine, ProficienciesInLine,
               OriginInLine, ProgressionInLine, DescriptionInLine, RelationInLine]

@admin.register(NPCEquipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["name", "character"]

@admin.register(NPCFeatures)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'version')
    list_filter = ('publisher', 'release_date')
    search_fields = ('name', 'abbreviation')


@admin.register(UserContentProfile)
class UserContentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'active_sources_list', 'updated_at')
    list_filter = ('active_sources',)
    search_fields = ('user__username',)

    def active_sources_list(self, obj):
        return ", ".join([s.name for s in obj.active_sources.all()])

    active_sources_list.short_description = 'Active Sources'


@admin.register(DataPack)
class DataPackAdmin(admin.ModelAdmin):
    list_display = ('source', 'is_installed', 'installed_at')
    list_filter = ('is_installed', 'source')
    actions = ['mark_as_installed', 'mark_as_uninstalled']

    def mark_as_installed(self, request, queryset):
        queryset.update(is_installed=True)

    mark_as_installed.short_description = "Mark selected packs as installed"

    def mark_as_uninstalled(self, request, queryset):
        queryset.update(is_installed=False)

    mark_as_uninstalled.short_description = "Mark selected packs as not installed"

    change_form_template = 'admin/datapack_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/export/',
                self.admin_site.admin_view(self.export_pack),
                name='datapack_export'
            ),
        ]
        return custom_urls + urls

    def export_pack(self, request, object_id):
        pack = get_object_or_404(DataPack, pk=object_id)
        fixtures = get_fixture_paths_for_source(pack.source)

        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        output_path = os.path.join(temp_dir, f'{pack.source.abbreviation.lower()}_pack.lsc')

        checksum = create_lsc_file(
            pack.source.name,
            pack.source.abbreviation,
            pack.source.version,
            fixtures,
            output_path
        )

        # Update the pack with the new file
        with open(output_path, 'rb') as f:
            pack.file.save(
                f'{pack.source.abbreviation.lower()}_pack.lsc',
                ContentFile(f.read())
            )
        pack.checksum = checksum
        pack.save()

        # Clean up
        os.remove(output_path)

        self.message_user(request, "Pack exported successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))