from multiprocessing.resource_tracker import register

from django.contrib import admin

from .models import *


# Register your models here.

class AbilityInLine(admin.StackedInline):
    model = NPCAbility
    extra = 1


class HPInLine(admin.StackedInline):
    model = NPCHP
    extra = 0


class InspirationInLine(admin.StackedInline):
    model = NPCInspiration
    extra = 0


class FeaturesInLine(admin.StackedInline):
    model = NPCFeatures
    extra = 1


class EquipmentInLine(admin.StackedInline):
    model = NPCEquipment
    extra = 1


class ProficienciesInLine(admin.StackedInline):
    model = NPCProficiencies
    extra = 1


class OriginInLine(admin.StackedInline):
    model = NPCOrigin
    extra = 1


class ProgressionInLine(admin.StackedInline):
    model = NPCClassProgression
    extra = 1


class DescriptionInLine(admin.StackedInline):
    model = NPCDescription
    extra = 0

@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    inlines = [AbilityInLine, HPInLine, InspirationInLine, FeaturesInLine, EquipmentInLine, ProficienciesInLine,
               OriginInLine, ProgressionInLine, DescriptionInLine]

@admin.register(NPCEquipment)
class EquipmentAdmin(admin.ModelAdmin):
    pass