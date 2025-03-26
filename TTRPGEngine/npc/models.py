from django.db import models
from django.db.models import CASCADE


# Master Models
# These models inherit down to the data models with the default data, and the character data that copies
# from the default data

# Default Data

class MasterAbility(models.Model):
    ability = models.CharField(max_length=255)
    score = models.IntegerField(default=10)
    modifier = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def get_modifier(self, ability):
        pass
        #return round((score-10)/2)



class MasterSkills(models.Model):
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

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_LIST)
    ability = models.ForeignKey('MasterAbility', on_delete=CASCADE, blank=True, null=True)
    proficiency_level = models.IntegerField(default=0, choices=PROFICIENCY_LEVEL)
    bonus = models.IntegerField(default=0)
    passive_bonus = models.IntegerField(default=10)

    class Meta:
        abstract = True

    def get_bonus(self, name):
        pass

    def get_passive(self, name):
        pass



class MasterHP(models.Model):
    """ This model is responsible for the group of values in the upper center of the character sheet. Mostly used
        during combat to keep track of the players condition."""
    # Armor Class.
    armor_class = models.IntegerField(default=10)

    # Initiative.
    initiative = models.IntegerField(default=0)

    # Speed.
    speed = models.IntegerField(default=30)

    # Hit Points.
    temp_hit_points = models.IntegerField(null=True)
    max_hit_points  = models.IntegerField(default=4)
    hit_points      = models.IntegerField(default=4)
    max_hit_dice    = models.JSONField(null=True)
    hit_dice        = models.JSONField(null=True)
    # Death Saves.
    death_saves_success = models.IntegerField(default=0)
    death_saves_failure = models.IntegerField(default=0)

    # Hidden Fields
    new_hit_die_rolls = models.JSONField(null=True)

    class Meta:
        abstract = True

    # methods
    def get_max_hit_points(self):
        pass



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













class MasterEquipment(models.Model):
    """All things wearable and carriable"""
    item = models.CharField(max_length=255, default="item", blank=False)
    type = models.CharField(max_length=255, default="")
    value = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    description = models.TextField()

    class Meta:
        abstract = True

class MasterPersonality(models.Model):
    traits  = models.TextField()
    ideals  = models.TextField()
    bonds   = models.TextField()
    flaws   = models.TextField()

    class Meta:
        abstract = True

class MasterFeatures(models.Model):
    feature = models.CharField(max_length=255)
    description = models.TextField()



class MasterLineage(models.Model):
    size_choices = {'tiny'  : 'Tiny',
            'small' : 'Small',
            'medium': 'Medium',
            'large' : 'Large',
            'huge'  : 'Huge',
            'gargantuan' : 'Gargantuan'}


    #Name
    classification = models.CharField(max_length=255, default="", blank=False)
    # Basic Attributes
    ability_score_increase = models.JSONField()
    max_age = models.IntegerField()
    alignment = models.CharField(max_length=255)
    size = models.CharField(max_length=255, choices=size_choices)
    speed = models.IntegerField(default=30)
    languages = models.TextField()
    sublineage = models.ForeignKey('MasterSubLineage', on_delete=CASCADE, )


class MasterSubLineage(MasterLineage)












class Description(models.Model):
    age     = models.CharField(max_length=255)
    height  = models.CharField(max_length=255)
    weight  = models.CharField(max_length=255)
    eyes    = models.CharField(max_length=255)
    skin    = models.CharField(max_length=255)
    hair    = models.CharField(max_length=255)
    appearance  = models.TextField(max_length=255)
    appearance_photo = models.ImageField(max_length=255)
    backstory   = models.TextField(max_length=255)
    organization_name = models.CharField(max_length=255)
    organization_symbol = models.ImageField(max_length=255)
    organization_description = models.TextField(max_length=255)





# Create your models here.
class Lineage(models.Model):
    #Name
    classification = models.CharField(max_length=255, default="", blank=False)
    # Basic Attributes
    Sublineage = models.ForeignKey('MasterSubLineage', on_delete=CASCADE, )

class Background(models.Model):
    pass




class NPC(models.Model):
    name = models.CharField(max_length=255, default="", blank=False)
    inspiration = models.BooleanField(default=False)
    lineage = models.ForeignKey(Lineage, on_delete=models.CASCADE, blank=False)
    proficiency_bonus = models.IntegerField(default=2)

