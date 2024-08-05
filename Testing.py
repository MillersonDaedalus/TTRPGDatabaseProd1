import CharacterCreation as CC

if __name__ == "__main__":
    races = ['Elf','Orc']
    for i in range(2):
        globals()['character'+str(i)] = CC.Character(races[i])
    print(character0.race)
    print(character1.race)
