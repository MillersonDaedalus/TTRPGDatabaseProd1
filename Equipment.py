class Weapon:
    def __init__(self, damage, weight, value):
        self.damage = damage
        self.weight = weight
        self.value = value

class Armor:
    def __init__(self, AC, weight, value):
        self.armor_class = AC
        self.weight = weight
        self.value = value