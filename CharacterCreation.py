

class Character:
    def __init__(self, race):
        self.name = 'kyle'
        self.race = race
        self.background = 'sage'
        self.equipment = []

    def equip(self, item):
        self.equipment.append(item)