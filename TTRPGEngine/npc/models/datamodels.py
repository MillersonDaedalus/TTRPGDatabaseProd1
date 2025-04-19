from templates import *
import os
import datetime
import zipfile
import json
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
# -------------------------------------  Data Side Tables  -------------------------------------------------------------
# Key Class that make up the Data Tables
class MasterData(models.Model):
    source = models.ForeignKey('DataSource', on_delete=CASCADE, null=True)

    class Meta:
        abstract = True

class MasterSource(models.Model):
    """Represents a source book or data pack (e.g., PHB, Xanathar's Guide)"""
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    publisher = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    release_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['release_date', 'name']

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


# Inherit from MasterModule + MasterData

class DataAbility(MasterAbility, MasterData): # A little basic but will be used to prefill new characters.
    pass

class DataHP(MasterHP, MasterData): #Might not need this one
    pass

class DataFeatures(MasterFeatures):
    pass

#class DataFeatRelationships(MasterFeatRelationships):
    #feature = models.ForeignKey('DataFeatures', on_delete=CASCADE)

class DataEquipment(MasterEquipment, MasterData):
    pass

class DataProficiencies(MasterProficiencies, MasterData):
    ability = models.ForeignKey('DataAbility', on_delete=CASCADE, blank=True, null=True)

class DataOrigin(MasterOrigin, MasterData):
    features = models.ManyToManyField('DataFeatures')

class DataClassProgression(MasterClassProgression, MasterData):
    origin = models.ForeignKey(
        'DataOrigin',
        on_delete=models.CASCADE,
        related_name='progressions'
    )
    features = models.ManyToManyField('DataFeatures')

class DataSource(MasterSource):
    pass

class UserContentProfile(models.Model):
    """Tracks which content sources a user has activated"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='content_profile')
    active_sources = models.ManyToManyField('DataSource')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Content profile for {self.user.username}"


def validate_lsc_extension(value):
    if not value.name.endswith('.lsc'):
        raise ValidationError('Only .lsc files are allowed.')


class DataPack(models.Model):
    """Represents an installable data fixture package"""
    source = models.ForeignKey('DataSource', on_delete=models.CASCADE)
    file = models.FileField(upload_to='data_packs/')
    checksum = models.CharField(max_length=64)  # For verifying integrity
    is_installed = models.BooleanField(default=False)
    installed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Data pack for {self.source}"

    def extract_to_fixtures(self):
        """Extract LSC file to individual fixture files"""
        if not self.file:
            return False

        try:
            with zipfile.ZipFile(self.file.path) as z:
                # Extract metadata if exists
                if 'metadata.json' in z.namelist():
                    with z.open('metadata.json') as f:
                        self.metadata = json.load(f)

                # Extract all JSON files to fixtures directory
                for filename in z.namelist():
                    if filename.endswith('.json'):
                        fixture_name = os.path.basename(filename)
                        fixture_path = os.path.join('data_packs', 'fixtures', fixture_name)

                        with z.open(filename) as src_file:
                            content = ContentFile(src_file.read())

                            # Save extracted file to storage
                            default_storage.save(fixture_path, content)

            return True
        except (zipfile.BadZipFile, json.JSONDecodeError) as e:
            # Handle extraction errors
            return False

    def create_lsc_from_fixtures(self, fixture_files, output_path):
        """Create an LSC file from multiple fixture files"""
        with zipfile.ZipFile(output_path, 'w') as z:
            # Add metadata
            metadata = {
                'source': self.source.name,
                'version': self.source.version,
                'created_at': datetime.now().isoformat()
            }
            z.writestr('metadata.json', json.dumps(metadata))

            # Add all fixture files
            for fixture in fixture_files:
                z.write(fixture, os.path.basename(fixture))