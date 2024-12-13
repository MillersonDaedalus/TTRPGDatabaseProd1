from ZODB import FileStorage, DB
import ObjectClasses as OC


datastore = FileStorage.FileStorage('data.fs')
db = DB(datastore)
connection = db.open()
root = connection.root()

elf = OC.Race('elf',85,'perception')
orc = OC.Race('Orc', 24, 'Athletics')

root['Races'] = [elf,orc,'Dragonborn']
root['Backgrounds'] = ['Acolyte','Criminal','Soldier']

print(root['Races'][1].name)