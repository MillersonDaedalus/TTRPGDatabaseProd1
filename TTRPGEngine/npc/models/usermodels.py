from .model_templates import *
from .rule import *

# --------------------------------------  User Side tables  ------------------------------------------------------------
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

# Outlier Models and Standalone features that don't fit under another umbrella
class MasterInspiration(models.Model):
    inspiration = models.BooleanField(default=False)

    class Meta:
        abstract = True

# ----------------------------------------------------------------------------------------------------------------------
# Eventually this will all be replaced with a factory function.
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