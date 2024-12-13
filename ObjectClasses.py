# Core
class Abilities:
    def __init__(self, str, dex, con, int, wis, cha):
        self.strength = str
        self.dexterity = dex
        self.constitution = con
        self.intelligence = int
        self.wisdom = wis
        self.charisma = cha

    def get_modifer(self, ability):
        print("getting mod")
        ability = getattr(self, ability)
        return int((ability-10)/2)

class Proficiencies:
    def __init__(self, abilities, skills, tools, weapons, armors):
        self.abilities = abilities

        self.skills = skills
        self.tools = tools
        self.weapons = weapons
        self.armors = armors

    def set_proficiencies(self, skilllist, indexedprof):
        skill_names = list(skilllist.keys())  # Get list of skill names
        for i, skill_name in enumerate(skill_names):
            ability, proficiency_level = skilllist[skill_name]
            self_value = skilllist[i]  # Get the value for this skill from the list
            setattr(self, skill_name, self_value)  # Assign value to self.<skill_name>
class Health:
    pass

class ArmorClass:
    pass

class Actions:
    pass
class Class:
    pass

class SubClass:
    pass
class Level:
    pass

# Features
class Features:
    pass
    '''
    def __init__(self, ab_mod, ability):
        self.ability_modifier = ab_mod
        self.ability = ability
    '''

class Feature:
    pass


# Equipment

class Inventory:
    pass
class Item:
    pass
    '''
    def __init__(self, damage, weight, value):
        self.damage = damage
        self.weight = weight
        self.value = value
    '''

class Armor(Item):
    pass
    '''
    def __init__(self, AC, weight, value):
        self.armor_class = AC
        self.weight = weight
        self.value = value
    '''

# Lineages
class Race:
    pass
    '''
    def __init__(self, name=str, type=str, subtypes=[], ASI=[], proficencies=[], size=str, resistance=[], darkvision=int, age_range=str, alignment=str):
        # Core
        self.name = name
        self.type = type
        self.subtypes = subtypes
        self.ASI = ASI
        self.proficencies = proficencies
        self.size = size
        self.resistance = resistance
        self.darkvision = darkvision
        # Details
        self.age_range = age_range
        self.alignment = alignment
        # Extra
    '''

class SubRace:
    pass



# Backgrounds
class Background:
    pass





if __name__ == "__main__":
    skill_list = {  "Acrobatics": ("Dexterity", 0),
                    "Animal Handling": ("Wisdom", 0),
                    "Arcana": ("Intelligence", 0),
                    "Athletics": ("Strength", 0),
                    "Deception": ("Charisma", 0),
                    "History": ("Intelligence", 0),
                    "Insight": ("Wisdom", 0),
                    "Intimidation": ("Charisma", 0),
                    "Investigation": ("Intelligence", 0),
                    "Medicine": ("Wisdom", 0),
                    "Nature": ("Intelligence", 0),
                    "Perception": ("Wisdom", 0),
                    "Performance": ("Cha",0),
                    "Persuasion": ("Cha",0),
                    "Religion": ("Int",0),
                    "Sleight of, Hand": ("Dex", 0),
                    "Stealth": ("Dex",0),
                    "Survival": ("Wis",0)
                    }

    ability = Abilities(10, 10, 14, 15, 18, 7)
    print(ability.get_modifer("charisma"))
    proficencies = Proficiencies(ability, skill_list, {},{},{})
    # print(proficencies.skills.keys())
    # print(proficencies.skills["Deception"][1])
