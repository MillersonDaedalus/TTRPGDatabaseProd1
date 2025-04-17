import os
import datetime
import zipfile
import json

from django.core.files.storage import default_storage
from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


"""All architectures are wrong, some are useful..."""
# --------------------------------------  Master Models  ---------------------------------------------------------------
# These models inherit down to the data models with the default data, and the character data that copies
# from the default data


# Core Models. Most basic attributes every creature needs to have.
# Even Objects have Ability Scores and HP.
class MasterAbility(models.Model):
    ability = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(default=10, blank=True, null=True)
    modifier = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.ability

    def get_modifier(self, ability):
        pass
        #return round((score-10)/2)

class MasterHP(models.Model):
    """ This model is responsible for the group of values in the upper center of the character sheet. Mostly used
        during combat to keep track of the players condition."""
    # Armor Class.
    armor_class = models.IntegerField(default=10)

    # Initiative.
    initiative = models.IntegerField(default=0)


    # Hit Points.
    temp_hit_points = models.IntegerField(blank=True, null=True)
    max_hit_points  = models.IntegerField(default=4)
    hit_points      = models.IntegerField(default=4)
    max_hit_dice    = models.JSONField(blank=True, null=True)
    hit_dice        = models.JSONField(blank=True, null=True)
    # Death Saves.
    death_saves_success = models.IntegerField(default=0)
    death_saves_failure = models.IntegerField(default=0)

    # Hidden Fields
    # Keep track of the rolls you make to increase your max hit points on level up.
    new_hit_die_rolls = models.JSONField(blank=True, null=True)

    class Meta:
        abstract = True

    # methods
    def get_max_hit_points(self):
        pass


# Outlier Models and Standalone features that don't fit under another umbrella
class MasterInspiration(models.Model):
    inspiration = models.BooleanField(default=False)

    class Meta:
        abstract = True

''' Depreciated, moving forward actions will be applied to items. Actions are something an item "can do", not a standalone thing.
class MasterActions(models.Model):
    """Used to keep track of all weapon attacks, spells, and special resources."""

    # Choices
    ACTION_TYPE = {
        'action' : 'Action',
        'bonus action' : 'Bonus Action',
        'reaction' : 'Reaction',
        'free action' : 'Free Action',
        'special' : 'special'
    }


    action = models.CharField(max_length=255, default="")
    action_type = models.CharField(max_length=255, choices=ACTION_TYPE, default=ACTION_TYPE[0], blank=True, null=True)

    # What ability the action uses, and an alternate for things like finesse.
    ability = models.ForeignKey('MasterAbility', on_delete=models.CASCADE)
    alternate_ability = models.ForeignKey('MasterAbility', on_delete=models.CASCADE)

    # How much damage the action does (if any), and what type
    damage = models.CharField(max_length=255, default="")
    damage_type = models.CharField(max_length=255, default="")

    extra_info = models.TextField(default="")
    resource = models.CharField
    class Meta:
        abstract = True
'''

# --------------------------------------  Template Models  -------------------------------------------------------------
# These models are the templates that are applied to objects. Completely swappable at any time. Modular
# Base template model with common features
class MasterTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# Core Minor Modules.
# Inventory System.
class MasterEquipment(MasterTemplate):
    """All things wearable and carriable"""
    TYPE_LIST = {
        'Adventuring Gear' : {
            'equipment pack' : 'Equipment Pack',
            'common item' : 'Common Item',
            'usable item' : 'Usable Item',
            'clothes' : 'Clothes',
            'arcane focus' : 'Arcane Focus',
            'druidic focus' : 'Druidic Focus',
            'holy symbol' : 'Holy Symbol',
            'container' : 'Container',
        },
        'Armor' : {
            'light armor' : 'Light Armor',
            'medium armor' : 'Medium Armor',
            'heavy armor' : 'Heavy Armor',
            'shield' : 'shield'
        },
        'trinket' : 'Trinket',
        'Weapon' : {
            'simple melee' : 'Simple Melee',
            'simple ranged' : 'Simple Ranged',
            'martial melee' : 'Martial Melee',
            'martial ranged' : 'Martial Ranged'
        },
        'explosive' : 'Explosive',
        'Wonderous Item' : {
            'wonderous item' : 'Wonderous Item',
            'potion' : 'Potion',
            'ring' : 'Ring',
            'rod' : 'Rod',
            'staff' : 'Staff',
            'scroll' : 'Scroll',
            'wand' : 'Wand',
        },
        'Currency' : {
            'coin' : 'Coin',
            'trade good' : 'Trade Good',
            'gem stone' : 'Gem Stone'
        },
        'Poison' : {
            'contact' : 'Contact',
            'ingested' : 'Ingested',
            'inhaled' : 'Inhaled',
            'injury' : 'Injury'
        },
        'Tool' : {
            'artisan' : 'Artisan',
            'gaming set' : 'Gaming Set',
            'musical instrument' : 'Musical Instrument',
            'tool' : 'Tool'
        },
        'siege equipment' : 'Siege Equipment',
        'Animal' : {
            'animal' : 'Animal',
            'tack_and_harness' : 'Tack & Harness'
        },
        'Vehicles' : {
            'land' : 'Land',
            'water' : 'Water'
        }
    }

    PERIOD_LIST = {
        '' : '---',
        'renaissance' : 'Renaissance',
        'modern' : 'Modern',
        'futuristic' : 'Futuristic'
    }

    RARITY_LIST = {
        '' : '---',
        'common' : 'Common',
        'uncommon' : 'Uncommon',
        'rare' : 'Rare',
        'very rare' : 'Very Rare',
        'legendary' : 'Legendary',
        'artifact' : 'Artifact',
        'other' : 'Other'
    }

    DAMAGE_PROFILES = {
        '' : '---',
        'melee' : 'Melee',
        'ranged' : 'Ranged',
        'cone' : 'Cone',
        'cylinder' : 'Cylinder',
        'emanation' : 'Emanation',
        'line' : 'Line',
        'sphere' : 'Sphere',
        'square' : 'Square'
    }


    type = models.CharField(max_length=255, choices=TYPE_LIST)
    time_period = models.CharField(max_length=255, choices=PERIOD_LIST, blank=True, default='')
    # is_equipped = models.BooleanField(default=False) This needs moved to Player table
    value = models.IntegerField(blank= True, null=True)
    weight = models.IntegerField(blank= True, null=True)

    #Armor Specific
    ac_formula = models.JSONField(blank=True, null=True)
    strength_requirement = models.IntegerField(blank=True, null=True)
    stealth_disadvantage = models.BooleanField(blank=True, null=True)

    #Weapon Specific
    damage = models.CharField(max_length=255, blank=True, null=True)
    damage_type = models.CharField(max_length=255, blank=True, null=True)
    damage_profile = models.CharField(max_length=255, choices=DAMAGE_PROFILES, blank=True, default='')
    normal_range = models.IntegerField(blank=True, null=True) #0 = self, 5 = touch, everything else is ranged
    max_range = models.IntegerField(blank=True, null=True)

    #Wonderous Item
    rarity = models.CharField(max_length=255, choices=RARITY_LIST, blank=True, default='')
    requires_attunment = models.BooleanField(default=False)


    class Meta:
        abstract = True


# Skills System. A lot more than just skills care about proficiencies.
# Proficiency bonus is located in the race module.
# TODO include logic that allows origins to populate this without duplication.
class MasterProficiencies(MasterTemplate):
    TYPE_LIST = {
        'skill' : 'Skill',
        'armor': 'Armor',
        'weapon': 'Weapon',
        'tool' : 'Tool',
        'gaming set': 'Gaming Set',
        'instrument': 'Instrument',
        'saving throw' : 'Saving Throw',
        'language' : 'Language',
        'other' : 'Other'
    }

    PROFICIENCY_LEVEL = {
        0 : 'Not Proficient',
        1 : 'Proficient',
        2 : 'Expertise'
    }

    # name inherited from parent
    type = models.CharField(max_length=255, choices=TYPE_LIST)
    ability = models.ForeignKey('MasterAbility', on_delete=CASCADE, blank=True, null=True)
    proficiency_level = models.IntegerField(default=0, choices=PROFICIENCY_LEVEL)
    misc_bonus = models.IntegerField(default=0)
    passive_bonus = models.IntegerField(default=10)
    advantage = models.BooleanField(default=False)
    disadvantage = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def get_bonus(self, name):
        pass

    def get_passive(self, name):
        pass

# Container for all features from the other modules.
# logic
class MasterFeatures(MasterTemplate):
    # Name and Description Inherited from Parent


    #class related fields.
    level_requirement = models.PositiveSmallIntegerField(blank=True, null=True)
    currency_cost = models.IntegerField(blank=True, null=True) # Cost for using this ability against the class.

    class Meta:
        abstract = True


    class Meta:
        abstract = True
# Core Major Modules
# Race & Background options for players TO-DO make the system more robust for monster stat blocks, check, Origin now has
# slots for race background and class which is enough to cover almost everything for monsters
# Races and backgrounds are pretty much just containers for skills and features. Combined together with things like
# epic boons, and dark gifts. Added classes to that list, class progression will be in a separate table.
class MasterOrigin(MasterTemplate):
    TYPE_LIST = {
        'lineage' : 'Lineage',
        'sublineage' : 'Sublineage',
        'background' : 'Background',
        'class' : 'Class',
        'subclass' : 'Subclass',
        'blessing' : 'Blessing',
        'charm' : 'Charm',
        'Dark Gift' : 'Dark Gift',
        'draconic gift' : 'Draconic Gift',
        'epic boon' : 'Epic Boon',
        'supernatural gift' : 'Supernatural Gift',
        'madness' : 'Madness'
    }

    SIZE_LIST = {
            '' : '---',
            'tiny'  : 'Tiny',
            'small' : 'Small',
            'medium': 'Medium',
            'large' : 'Large',
            'huge'  : 'Huge',
            'gargantuan' : 'Gargantuan'
    }

    ALIGNMENT_LIST = {
        '' : '---',
        'lawful good'     : 'Lawful Good',
        'lawful neutral'  : 'Lawful Neutral',
        'lawful evil'     : 'Lawful Evil',
        'neutral good'    : 'Neutral Good',
        'true neutral'    : 'True Neutral',
        'neutral evil'    : 'Neutral Evil',
        'chaotic good'    : 'Chaotic Good',
        'chaotic neutral' : 'Chaotic Neutral',
        'chaotic evil'    : 'Chaotic Evil'
    }

    # Name and Description from parent.
    # Common Fields.
    type = models.CharField(max_length=255, choices=TYPE_LIST)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtype')
    # Used for effects like polymorphy that would deactivate racial traits without removing them.
    # Generally only one of each type should be active at a time for things like race, but being able to combine types
    # in this way is a feature of the flexible design and will not error.
    is_active = models.BooleanField(default=True)
    # Used for Multiclassing where the entry needs added to the list but the first level effects are not active.
    is_primary = models.BooleanField(default=True)

    proficiencies = models.TextField(blank=True, null=True)  # TODO Need to fix the logic on this and tie it to the skills system
    features = models.ManyToManyField('MasterFeature', through='MasterFeatOriginRelation')
    equipment = models.TextField(blank=True, null=True)  # TODO tie this in with equipment system

    # Race Traits
    ability_score_increase = models.JSONField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(max_length=255, choices=ALIGNMENT_LIST, default='', blank=True, null=True)
    size = models.CharField(max_length=255, choices=SIZE_LIST, default='', blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)

    # Background traits
    personality_traits = models.TextField(blank=True, null=True)
    ideals = models.TextField(blank=True, null=True)
    bonds = models.TextField(blank=True, null=True)
    flaws = models.TextField(blank=True, null=True)

    # Class Traits
    hit_die_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class MasterClassProgression(models.Model):
    """Level-by-level class features"""
    origin = models.ForeignKey(
        'MasterOrigin',
        on_delete=models.CASCADE,
        related_name='progressions'
    )
    level = models.PositiveSmallIntegerField()
    features = models.ManyToManyField('MasterFeature', through='MasterFeatOriginRelation')
    class_currency = models.JSONField() # Keep track of multiple types, including different spell-slot levels.

    class Meta:
        abstract = True
        unique_together = [('origin', 'level')]
        ordering = ['level']

# User Only Tables. Will Not be getting a master data table
class MasterDescription(models.Model):
    age     = models.CharField(max_length=255, blank=True, null=True)
    height  = models.CharField(max_length=255, blank=True, null=True)
    weight  = models.CharField(max_length=255, blank=True, null=True)
    eyes    = models.CharField(max_length=255, blank=True, null=True)
    skin    = models.CharField(max_length=255, blank=True, null=True)
    hair    = models.CharField(max_length=255, blank=True, null=True)
    appearance  = models.TextField(max_length=255, blank=True, null=True)
    appearance_photo = models.ImageField(blank=True, null=True)
    backstory   = models.TextField(max_length=255, blank=True, null=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    organization_symbol = models.ImageField(blank=True, null=True)
    organization_description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class MasterThisIsYourLife(models.Model):
    pass

    class Meta:
        abstract = True

# --------------------------------------  Implementation Models  -------------------------------------------------------
# Combined with master models to make usable tables.
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

# Key Class that makes up the user side tables. Includes character reference.
class MasterPlayer(models.Model):
    character = models.ForeignKey('NPC', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class MasterNPC(models.Model):
    # The only thing about the character that shouldn't change. John is still John even if he gets turned into a rabbit.
    name = models.CharField(max_length=255, default="", blank=False)
    player = models.CharField(max_length=255, default="NPC", blank=False)
    # All other traits are defined as a foreign key relationship back to the character
    #related_names = [
    #    'abilities',
    #    'hitpoints',
    #    'inspiration'
    #    'proficiencies',
    #    'inventory',
    #    'features',
    #    'origin'
    #]

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_attribute(self, attribute):
        pass

    # methods
    def get_race(self):
        pass

    def get_background(self):
        pass

    def get_classes(self):
        pass

# --------------------------------------  Relationship Tables  ---------------------------------------------------------
#

class MasterFeatOriginRelation(models.Model):
    origin = models.ForeignKey('MasterOrigin', on_delete=CASCADE)
    feature = models.ForeignKey('MasterFeatures', on_delete=CASCADE)

    class Meta:
        abstract = True

# -------------------------------------  Data Side Tables  -------------------------------------------------------------
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

class DataDescription(MasterDescription, MasterData):
    pass

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

# --------------------------------------  User Side tables  ------------------------------------------------------------

# . Inherit from MasterModule + MasterUser, overwrite relationships to non-abstract tables.

class NPCAbility(MasterAbility, MasterPlayer):
    pass

class NPCHP(MasterHP, MasterPlayer):
    pass

class NPCInspiration(MasterInspiration, MasterPlayer):
    pass

class NPCFeatures(MasterFeatures):
    pass

#class NPCFeatRelationships(MasterFeatRelationships):
    #feature = models.ForeignKey('NPCFeatures', on_delete=CASCADE)

class NPCEquipment(MasterEquipment, MasterPlayer):
    pass

class NPCProficiencies(MasterProficiencies, MasterPlayer):
    ability = models.ForeignKey('NPCAbility', on_delete=CASCADE, blank=True, null=True)

class NPCOrigin(MasterOrigin, MasterPlayer):
    features = models.ManyToManyField('NPCFeatures', through='NPCFeatOriginRelation')

class NPCClassProgression(MasterClassProgression, MasterPlayer):
    origin = models.ForeignKey(
        'NPCOrigin',
        on_delete=models.CASCADE,
        related_name='progressions'
    )
    features = models.ManyToManyField('NPCFeatures')

class NPCDescription(MasterDescription, MasterPlayer):
    pass

class NPC(MasterNPC):
    pass

class NPCFeatOriginRelation(MasterFeatOriginRelation, MasterPlayer):
    origin = models.ForeignKey('NPCOrigin', on_delete=CASCADE)
    feature = models.ForeignKey('NPCFeatures', on_delete=CASCADE)