from django.db import models

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

class Types(models.Model):
    category = models.CharField