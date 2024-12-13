# TTRPGDatabaseProd1
Iteration 1 of my TTRPG character generator

Todo:
1. Change character creation to call master object instances, copy them to the character, then delete master objects after character creation.
2. Install embedded database and code out the programs data
3. Create installation exe
4. Objectifiy other parts of the character such as health, ability scores, skills. Implement methods to allow objects to talk to each other.


Flow Chart

First run:
- initialize database with cleartext data
- validate data

Startup:
- initilize roller
- Prompt for character creation
- Initilize character objects from input
  - Objects call roller indiviually
- Prompt user for choices as needed.
- Validate character creation