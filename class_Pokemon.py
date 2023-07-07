# Importing necessary functions and classes
# Built in python libraries
import pickle
from random import randint

# My own functions adn classes
from class_Move import Move
from ProjectDataCleaning.fileControl import *
from other_functions import *
from dictonaries import *
import user_inputs


# Defines the basic design for each pokemon, unsure quite how much this will control at this point
# Is inital passed the SpeciesID number(from Pokedex) and the range the pokemon should be in
# Context determines whether or not specific things should happen (such as giving trainer pokemon EVs)
class Pokemon:
    def __init__(self,speciesID,minLvl,maxLvl,context,owner = ""):
        # Get the basic stats, set required things as they are required to be
        # Unique ID only if pokemon Data needs to be saved (ie. when caught by a player)
        self.uniqueID = ""
        self.context = context
        self.owner = owner

        self.copyBaseValues(str(speciesID))
        self.nickname = self.species
        self.heldItem = ""
        self.allowedEvolve = True
        self.inParty = False

        self.level = randint(minLvl,maxLvl)
        self.experience = levelingBounds[self.level]
        self.assignRandomNature()
        self.EVs = [0,0,0,0,0,0]
        self.IVs = []
        for each in range(6):
            iv = randint(0,31)
            self.IVs.append(iv)

        # Apply all context specfic attribute alterations
        if context == "Wild":
            pass
        
        if context == "Trainer":
            self.setTrainerEVs()

        if context == "Player":
            pokemonInstancesPath = os.path.join(format(os.getcwd()),"SavedObjects","PokemonStorage","pokemon_instance_codes.txt")
            self.uniqueID = generateUniqueReference(pokemonInstancesPath)

        # Sets "adjusted" stats and give the pokemon its starting moveset
        self.calculateAdjustedStats()
        self.assignLeveledMoves()
        self.assignAllowedMoves()
        self.determineStartMoveset()

        # Actual Stats are a pokemons stats following the effects of items and move buffs/debuffs
        # They are only altered during the course of battle, so are initally the same as adjusted stats
        self.resetBattleValues()

    # ---------------------------------------------------------------------------------

    # "Admin" Functions
    def update(self):
        total_base_stats = 0
        for stat in self.baseStats:
            total_base_stats += int(stat)
        self.base_exp = total_base_stats // 2


    # Pickles the pokemon to save all it's attributes
    # This will only really be called by the parent Player class.
    def picklePokemonObject(self):
        storage_path = os.path.join(format(os.getcwd()),"SavedObjects","PokemonStorage",self.owner,self.uniqueID)
        if not os.path.exists(storage_path):
            with open(storage_path,"x") as file:
                file.close()
        with open(storage_path,"wb") as pickleFile:
            pickle.dump(self,pickleFile)
            pickleFile.close()

    # ---------------------------------------------------------------------------------

    # Pokemon setup Functions

    # Should probably break sections into different functions, just to make it a bit cleaner
    def copyBaseValues(self,speciesID):
        # Open File and splits each line into a list at " "s
        statsFilePath = selectFile(["DataTables"],"full_pokemon_data.txt")
        statsFileLines = readFile(statsFilePath, ",")
        
        self.speciesData = []
        line = 0
        # Goes through every line in the document to find the start of the correct entry
        # It is suprisingly fast for 63323 lines
        foundSpecies = False
        while not foundSpecies:
            # New Data has some slight gaps, this if statement will only really be used during testing
            try:
                if statsFileLines[line][0] == speciesID:
                    self.speciesData.append(statsFileLines[line])
                    foundSpecies = True
            except IndexError:
                print(IndexError)
                pass
            line += 1 
        
        # Read from the starting line to the end line displayed as "======". 
        fullData = False
        while not fullData:
            line += 1
            try:
                if statsFileLines[line] == ['======']:
                    fullData = True
                else:
                    self.speciesData.append(statsFileLines[line])
            except IndexError:
                line += 1
                pass

        self.species = self.speciesData[0][1]
        self.types = [self.speciesData[6][1]]
        try:
            self.types.append(self.speciesData[6][3])
        except IndexError:
            self.types.append("")
        self.baseStats = self.speciesData[1][2].split(".")
        self.evYield = self.speciesData[2][2].split(".")
        total_base_stats = 0
        for stat in self.baseStats:
            total_base_stats += int(stat)
        self.base_exp = total_base_stats // 2
        self.base_catch_chance = self.speciesData[4][2]

    # Find and assign moves learnt by leveling up.
    def assignLeveledMoves(self):
        self.leveledMoves = []
        collectingMoves = True
        foundStart = False
        i = 0
        while collectingMoves: 
            if foundStart:
                newMove = []
                moveName = ""
                newMove.append(self.speciesData[i][0])
                for j in range(1,len(self.speciesData[i])):
                    if j == 1:
                        moveName = self.speciesData[i][j]
                    else:
                        moveName = moveName + " " + self.speciesData[i][j]
                newMove.append(moveName)
                self.leveledMoves.append(newMove)
                
            if self.speciesData[i] == ['Level', 'Up', 'Moves:']:
                foundStart = True

            i += 1
            if self.speciesData[i] == ['TMs:'] or self.speciesData[i] == ["Egg","Moves:"]:
                collectingMoves = False


    # Then we do somethings very similar, but for all possible learnt moves
    def assignAllowedMoves(self):
        self.allowedMoves = []
        collectingMoves = True
        foundStart = False
        i = 0
        while collectingMoves:
            if self.speciesData[i] == ["TRs:"]:
                i += 1

            if foundStart:
                newMove = []
                moveName = ""
                newMove.append(self.speciesData[i][0])
                for j in range(1,len(self.speciesData[i])):
                    if j == 1:
                        moveName = self.speciesData[i][j]
                    else:
                        moveName = moveName + " " + self.speciesData[i][j]
                newMove.append(moveName)
                self.allowedMoves.append(newMove)
            
            if self.speciesData[i] == ['TMs:']:
                foundStart = True

            i += 1
            if self.speciesData[i] == ['Armor','Tutors:']:
                collectingMoves = False
                

    # Determines the moves a pokemon should start with based on the allowed moves
    def determineStartMoveset(self):
        availableStartMoves = []
        for i in range(0,len(self.leveledMoves)):
            if int(self.leveledMoves[i][0]) <= self.level:
                availableStartMoves.append(self.leveledMoves[i][1])
        self.knownMoves = []
        
        # Assigns a maximum  of four moves, only if there are that many moves available
        for i in range(4):
            try:
                chosenMove = randint(0,len(availableStartMoves) - 1)
                self.knownMoves.append(Move(availableStartMoves[chosenMove]))
                availableStartMoves.remove(availableStartMoves[chosenMove])
            except ValueError:
                pass


    # Replaces a previously known move with a new one, only necessary if pokemon knows 4 moves already
    def assignNewMove(self,oldMove,newMove):
        print(f"{self.nickname} has forgotten the move {oldMove.name}")
        moveIndex = self.knownMoves.index(oldMove)
        self.knownMoves[moveIndex] = Move(newMove)
        print(f"{self.nickname} has learnt the move {newMove}")


    # Picks a random nature and assigns correct multipliers from the pokemon_natures dictonary
    def assignRandomNature(self):
        natureID = randint(1,25)
        natureInfo = pokemon_natures[natureID]
        self.nature = natureInfo[0]
        self.natureMultipliers = [1,1,1,1,1,1]
        self.natureMultipliers[natureInfo[1] - 1] = 1.1
        self.natureMultipliers[natureInfo[2] - 1] = 0.9


    # Trainer pokemon are given EVs based on their difficulty to make them more challenging than wild pokemon
    def setTrainerEVs(self):
        pass
        
    # ---------------------------------------------------------------------------------

    # Gameplay Mechanics Functions

    # Calculate stats adjusted for Lvl, IVs, EVs and nature
    def calculateAdjustedStats(self):
        self.adjustedStats = []
        isHP = True 
        statID = 0
        for each in self.baseStats:
            lvlAdjustedStat = calculateStat(int(self.baseStats[statID]),self.level,self.IVs[statID],self.EVs[statID],isHP,self.natureMultipliers[statID])
            self.adjustedStats.append(lvlAdjustedStat)
            statID += 1
            isHP = False


    # Resets all values used in a battle. Run when pokemon is haeled
    def resetBattleValues(self):
        self.effects = []
        self.isFainted = False
        self.isActive = False
        # HP,ATK,DEF,SPA,SPD,SPE,ACC,EVA
        self.baseStatStages = [0,0,0,0,0,0,0,0]
        self.actualStats = self.adjustedStats.copy()
        self.turnAction = []


    # Adds EVs gained from beating other pokemon in battle
    def addEVs(self,evs):
        total_new_evs = 0
        for ev in evs:
            total_new_evs += int(ev)
        
        total_self_evs = 0
        for ev in self.EVs:
            total_self_evs += ev

        if total_new_evs + total_self_evs > 255:
            return
        
        for i in range(6):
            if self.EVs[i] < 31:
                self.EVs[i] += int(evs[i])
            if self.EVs[i] > 31:
                self.EVs[i] = 31


    # Just increase the pokemons experience by a given amount and runs levelUp check
    def addExperience(self,newExperience):
        self.experience += newExperience
        self.levelUp()


    # Runs whenever experience gained , to detetmine if levelUp should occur
    def levelUp(self):
        fullyLeveled = False
        while not fullyLeveled and self.level < 100:
            nextLevel = self.level + 1
            nextBound =  levelingBounds[nextLevel]
            if self.experience <= nextBound:
                fullyLeveled = True
            else:
                self.level += 1
                self.calculateAdjustedStats()
                print(f"\n{self.nickname} has Leveled Up.")
                print(f"{self.nickname} is now Level {self.level}")
                print(f"HP:{self.adjustedStats[0]} ATK:{self.adjustedStats[1]} DEF:{self.adjustedStats[2]} SPA:{self.adjustedStats[3]} SPD:{self.adjustedStats[4]} SPE:{self.adjustedStats[5]}")
                self.levelLearnMove()

    # Checks if pokemon can learn a new move. And calls to ask user
    def levelLearnMove(self):
        for item in self.leveledMoves:
            if int(item[0]) == self.level and len(self.knownMoves) < 4:
                newMove = item[1]
                self.knownMoves.append(Move(newMove))
                print(f"{self.nickname} has learnt {newMove}.")

            elif int(item[0]) == self.level and len(self.knownMoves) >= 4:
                newMove = item[1]
                user_inputs.learnLevelMove(self,newMove)


    # Following levelUp, checks if the pokemon should levelUp
    def evolve(self):
        pass
            
    # ---------------------------------------------------------------------------------

    # Prints pokemons stats to terminal.
    def printStats(self):
        print(f"Species: {self.species} of nature {self.nature}")
        print(f"Typing: {self.types[0]}  {self.types[1]} ")
        print(f"Lvl: {self.level} from Exp: {self.experience} ")
        print(f"Base Stats: HP:{self.baseStats[0]} ATK:{self.baseStats[1]} DEF:{self.baseStats[2]} SPA:{self.baseStats[3]} SPD:{self.baseStats[4]} SPE:{self.baseStats[5]}")
        print(f"IVs: HP:{self.IVs[0]} ATK:{self.IVs[1]} DEF:{self.IVs[2]} SPA:{self.IVs[3]} SPD:{self.IVs[4]} SPE:{self.IVs[5]}")
        print(f"EV Yield: HP:{self.evYield[0]} ATK:{self.evYield[1]} DEF:{self.evYield[2]} SPA:{self.evYield[3]} SPD:{self.evYield[4]} SPE:{self.evYield[5]}")
        print(f"Adjusted Stats: HP:{self.adjustedStats[0]} ATK:{self.adjustedStats[1]} DEF:{self.adjustedStats[2]} SPA:{self.adjustedStats[3]} SPD:{self.adjustedStats[4]} SPE:{self.adjustedStats[5]}")
        print("Knows Moves:")
        for i in range(0,len(self.knownMoves)):
            print(f"- {self.knownMoves[i].name}")

    def printBattleStats(self):
        print(f"Lvl. {self.level} {self.species}")
        print(f"Health: {self.actualStats[0]}/{self.adjustedStats[0]}")
        print(f"ATK: {self.actualStats[1]} DEF: {self.actualStats[2]} SPA: {self.actualStats[3]} SPD: {self.actualStats[4]} SPE: {self.actualStats[5]}")
        print(f"Type: {self.types[0]}  {self.types[1]}")
        print("Knows Moves:")
        for i in range(0,len(self.knownMoves)):
            print(f"- {self.knownMoves[i].name}")

    # ---------------------------------------------------------------------------------

    # Test Functions, will be removed later.

    # Allows adding experience amounts to check the pokemon is leveling up appropriatley
    def testLeveling(self):
        while True:  
            validInput = False
            while not validInput:  
                user_input = input("Add Experience: \n> ")
                if user_input == "exit":
                    break
                
                try:
                    experienceAdd = int(user_input)
                    validInput = True
                except TypeError:
                    print("Invalid Value as Integer.")
            
            if user_input == "exit":
                    break
            
            self.experience += experienceAdd
            self.levelUp()
            
    # ---------------------------------------------------------------------------------

    # End of Pokemon class
    