from django.core.files.storage import default_storage
from .rule import *
from django.db.models import CASCADE



"""All architectures are wrong, some are useful..."""
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

    @property
    def features(self):
        f = MasterFeatures.objects.filter(character=self)
        return f

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


# --------------------------------------  Relationship Tables  ---------------------------------------------------------
#

class MasterFeatOriginRelation(models.Model):
    origin = models.ForeignKey('MasterOrigin', on_delete=CASCADE)
    feature = models.ForeignKey('MasterFeatures', on_delete=CASCADE)

    class Meta:
        abstract = True

