# This just contains the functions that I rewrote or scrapped completely following their inital completion
# Might not work as ajoining functions may also have been rewritten
# A lot of the inital ones are because I discovered the csv library

import os,random,pickle,math,numpy

from ProjectDataCleaning.fileControl import *
from input_interpretation import *
from class_Main import *
from class_Player import Player
from class_Trainer import Trainer
from class_Battle import Battle

# -----------------------------------------------------------------------------------------------------

# From ProjectDataCleaning\fileControl.py

# Redone as csv library used to make some steps redundant
# Opens and reads a given file, so that the data can be manipulated
def readFile(filePath):
   print(filePath)
   with open(filePath, 'r') as file:
      fileLines = file.readlines()
      file.close()
   for line in fileLines:
      line = line[:-2]
   return fileLines

# Redone as csv library used to make some steps redundant
# Writes new lines to the corerct file
def writeFile(filePath, fileLines):
   file = open(filePath, "w")
   for item in fileLines:
      item = item[:-1]
      file.writelines(item + "\n")

# -----------------------------------------------------------------------------------------------------

# ProjectDataCleaning\cleaning.py
# Whole file redundant once data was cleaned.

# Almost whole thing made redundant by csv library
# Will split each line of file into a list, will keep all elements in the list keepElements
def cleanData(rawLineStrings, keepItems):
   rawLineLists = []
   
   for line in rawLineStrings:
      line = line.split(",")
      
      rawLineLists.append(line)
   
   cleanLineStrings = []
   
   for line in rawLineLists:
      cleanLine = []
      cleanString = ''
      for item in keepItems:
         cleanLine.append(line[item])

      for item in cleanLine:
         cleanString = f"{cleanString}{item},"
              
      cleanLineStrings.append(cleanString)
   
   return cleanLineStrings


# Removes the coloumns that are unneeded
def cleanData(rawLines, keepItems):
   cleanLines = []
   for rawLine in rawLines:
      cleanLine = []
      for item in keepItems:
         cleanLine.append(rawLine[item])
      cleanLines.append(cleanLine)
   return cleanLines


# Just execute the correct functions in the correct order, completely useless except specifically here
# I will concede that this function is in fact, quite a mess. But what can you do
def run1(fileName, keepLines): 
   print("Reading Lines...")
   file = selectFile(["ProjectDataCleaning","rawData"], fileName)
   rawLines = readFile(file)
   print("Cleaning File...")
   cleanedLines = cleanData(rawLines, keepLines)
   print("Writing to File...")
   cleanFile = selectFile(["ProjectDataCleaning","cleanedData"], fileName)
   writeFile(cleanFile, cleanedLines)
   print("Done.")

# run1("moves.txt", [0,1,3,4,5,6,7,8,9,10,11])

# Because the code insists on adding random empty lines, which were not present when I had to run it through codio
# Why this added even more lines I do not know
# I now know.
def removeBlanks(fileLines):
   for line in fileLines:
      if line == ' ':
         fileLines.remove(' ')
   return fileLines


# Another 'beautifully' written hyperspecific function, that I'll never reuse
def run2(fileName):
   file = selectFile(["ProjectDataCleaning","cleanedData"], fileName)
   lines = readFile(file)
   lines = removeBlanks(lines)
   writeFile(file, lines)
   
# run2("evolutions.txt")

# Adds empty elements to csv files to stop Index Errors
def padLines(folders,filename,numPad):
   file = selectFile(folders,filename)
   lines = readFile(file)
   padLines = []

   for line in lines:
      while len(line) < numPad:
         line.append("")
      padLines.append(line)

   writeFile(file,padLines)

# padLines(["DataTables"], "pokemonBaseStats.txt",15)

# File contains the various pokedex entries, but they are in the way, so they must go.
# Slightly altered to allow removal of other unnecessary lines
def removeLines():
   dataFile = selectFile(["DataTables"],"full_pokemon_data.txt")
   lines = readFile(dataFile,",")
   running = True
   i = 0
   while running:
      try: 
         if 'Dynamax!' in lines[i]:
            lines.remove(lines[i])
         else:
            i += 1
      except IndexError:
         i += 1
      if i >= 64000:
         running = False
   
   writeFile(dataFile, lines)


# Reformat move names form DataTable\moveInformation.txt
def reformatNames():
   filePath = selectFile(["DataTables"],"moveInformation.txt")
   fileLines = readFile(filePath, ",")
   for i in range(1,len(fileLines)):
      line = fileLines[i][1]
      line = line.split("-")
      for j in range(len(line)):
         if j == 0:
            newLine = line[0][0].upper() + line[0][1:len(line[0])]
            print(newLine)
         else:
            try:
               newLine = newLine + " " + line[j][0].upper() + line[j][1:len(line[1])]
               print(newLine)
            except IndexError:
               pass
      fileLines[i][1] = newLine

   for line in fileLines:
      print(line)
   
   writeFile(filePath,fileLines)

# To remove dashes from the full_pokemon_data.txt file
def removeCharacter(filePath,character):
   fileLines = readFile(filePath, ",")
   print(fileLines)
   i = 0
   running = True
   while running:
      try:
         if character in fileLines[i]:
            fileLines[i].remove(character)
         else:
            i += 1
      except IndexError:
         i += 1
         pass
      if i > 64000:
         running = False
   writeFile(filePath,fileLines)

filePath = selectFile(["DataTables"],"full_pokemon_data.txt")
removeCharacter(filePath, "-")

# -----------------------------------------------------------------------------------------------------

# ProjectDataCleaning.compiling.py
# Once again file was redundant once all data had been compilied into relevant files

# Specificaly for rearranging the evolutions data
# Had to write on Codio as the Uni PC did not have a python intepreter for some reason
def reOrderEvolution():
    evolutionsPath = selectFile(["ProjectDataCleaning","cleanedData"], "evolutionChains.txt")
    evolutionLines = readFile(evolutionsPath)
    print(f"Before: \n {evolutionLines}")

    # Take each line and then add the correct evolutions
    for line in range(1, len(evolutionLines)):
        if evolutionLines[line][2] != "":
            evolvesFrom = int(evolutionLines[line][2])
            evolutionLines[evolvesFrom].append(evolutionLines[line][0])

    # Adds missing coloumn to those species who do not evolve
    for line in range(1, len(evolutionLines)):
        if len(evolutionLines[line]) < 4:
            evolutionLines[line].append("")

    print(f"After: \n {evolutionLines}")
    writeFile(evolutionsPath, evolutionLines)


# Combines the columns of different csv files, lists keep1 and keep2 ,specify which colums to keep from each file
# File2 will be esentially appended to file1 minus any unwanted lines
def combineFiles(file1, file2, keep1, keep2):
    # Open repective files
    file1Path = selectFile(["ProjectDataCleaning","cleanedData"], file1)
    file2Path = selectFile(["ProjectDataCleaning","cleanedData"], file2)
    file1Lines = readFile(file1Path)
    file2Lines = readFile(file2Path)
    newLines = []
    lineID = 0
    
    for line in file1Lines:
        newLine = []

        # Adds all desired columns from file 1
        for item in keep1:
            newLine.append(file1Lines[lineID][item])
        
        # Adds all desired columns from file 2
        for item in keep2:
            newLine.append(file2Lines[lineID][item])

        newLines.append(newLine)
        lineID += 1
    
    writeFile(file1Path, newLines)

# With the new data, some species are missing from the information. This compiles a list of all available species that can be used

def  compileSpecies():
    pokemon_data_file = selectFile(["DataTables"],"full_pokemon_data.txt")
    species_file = selectFile(["DataTables"],"available_species.txt")

    availableSpecies = []
    pokemonData = readFile(pokemon_data_file," ")

    finished = False
    newSpecies  = False
    i = 0
    while not finished:
        try: 
            if pokemonData[i][0] == "======":
                i += 1
                newLine = []
                newLine.append(pokemonData[i][0])
                availableSpecies.append(newLine)
                i += 1
        except IndexError:
            pass
        i += 1
        if i >= 64000:
            finished = True

    writeFile(species_file,availableSpecies)

# -----------------------------------------------------------------------------------------------------

# ProjectDataCleaning.generateEvolutionBounds

# Completely redundant from switching to itJavi data rather than PokeAPI data
# Evolution  wasn't reimplemented afterwards as notenough information or time following the switch

# As I can't find evolution data in a form that I can use, I will generate appropriate bounds for all evolvable pokemon
# These will not accurately match the main series and will likely be changed later on if I have extra time
# They will however suffice as a basic system to allow me to move on to other aspects of the game

from random import randint
from ProjectDataCleaning.fileControl import *

# Creates a file that provides a list of all species on the same evolution chain.
# This does have the issue of repeats where some pokemon have multiple evolutions, 
# They are few in number and can be handled as special cases and processed individaully
def generateEvolutionChains():
    evolutionsFile = selectFile(["ProjectDataCleaning","CleanedData"],"evolutions.txt")
    evolutionsLines = readFile(evolutionsFile)
    evolutionChainsLines = []
    categorizedSpecies = []

    # Cycles through all species
    for species in range(1,len(evolutionsLines)):
        baseSpeciesFound = False
        chainCompleted = False

        newChainLine = []
        if int(species) not in (categorizedSpecies):
           
           # Finds the base (first) evolution in each chain
            while not baseSpeciesFound:
                if evolutionsLines[int(species)][2] == "":
                    baseSpeciesFound = True
                    newChainLine.append(int(species))
                    categorizedSpecies.append(int(species))
                else:
                    species = evolutionsLines[int(species)][2]
            
            # Goes up the chain adding each item to a list until end of the chain is reached
            while not chainCompleted:
                if evolutionsLines[int(species)][3] == "":
                    chainCompleted = True 
                else:
                    species = evolutionsLines[int(species)][3]
                    newChainLine.append(int(species))
                    categorizedSpecies.append(int(species))
                    
            evolutionChainsLines.append(newChainLine)
    
    # Write data to new File, for later use
    evolutionChainsFile = selectFile(["ProjectDataCleaning","CleanedData"],"evolutionChains.txt")
    writeFile(evolutionChainsFile, evolutionChainsLines)

# generateEvolutionChains()

# Assigns the level bounds at which each evolution occurs
# They are pretty much random, might make it player changeable.
def generateEvolutionBounds():
    evolutionChainsFile = selectFile(["ProjectDataCleaning","CleanedData"],"evolutionChains.txt")
    evolutionChainsLines = readFile(evolutionChainsFile)
    pokemonFile = selectFile(["DataTables"],"pokemonBaseStats.txt")
    pokemonLines = readFile(pokemonFile)
    
    for chain in evolutionChainsLines:
        if len(chain) == 1:
            pokemonLines[int(chain[0])].append("")
        elif len(chain) == 2:
            evolutionBound = randint(25,61)
            pokemonLines[int(chain[0])].append(evolutionBound)

        elif len(chain) == 3:
            evolutionBound1 = randint(16,31)
            evolutionBound2 = randint(45,71)
            pokemonLines[int(chain[0])].append(evolutionBound1)
            pokemonLines[int(chain[1])].append(evolutionBound2)
        
    writeFile(pokemonFile,pokemonLines)

# generateEvolutionBounds()



# -----------------------------------------------------------------------------------------------------

# From createPokemon.py

# The original function for retrieving basic pokemon information upon creation from file DataTables\PokemonBaseStats.txt
# Upon discovery of the itsjavi github though, more complete data wsas found and was used to replace this old one
# Copying all relevant information from baseStats table
# Used initaily and upon evolution to update relevant attributes
def copyBaseValues(self, speciesID):
   pokemonInfoFile = selectFile(["DataTables"],"pokemonBaseStats.txt")
   pokemonInfo = readFile(pokemonInfoFile)
   speciesInfo = pokemonInfo[speciesID]
      
   self.species = speciesInfo[1]

   try: 
      self.evolveTo = int(speciesInfo[13])
      self.evolveAtLevel = int(speciesInfo[14])
   except:
      self.evolveTo = ""
      self.evolveAtLevel = 1000

   self.baseStats = [int(speciesInfo[5]),int(speciesInfo[6]),int(speciesInfo[7]),int(speciesInfo[8]),int(speciesInfo[9]),int(speciesInfo[10])]
   self.types = [speciesInfo[2],speciesInfo[3]]
      
   if speciesInfo[11] == "true":
      self.isLegendary = True
   else:
      self.isLegendary = False


# The original fuction for evolving before I had full evolution information
# Evolves Pokemon
def evolve(self):
        if self.level >= self.evolveAtLevel and self.allowedEvolve:
            print(f"{self.nickname} is evolving!")
            initalSpecies = self.species
            self.copyBaseValues(self.evolveTo)
            print(f"{self.nickname} evolved in {self.species}")
            if self.nickname == initalSpecies:
                self.nickname = self.species
            self.calculateAdjustedStats()

# -----------------------------------------------------------------------------------------------------

# Code that was purely for testing or changing things to make testing easier

# A fucntion whose entire purpose was to check the typing table was filled out and working correctly. It was.
def checkTypingTable():
   file = selectFile(["DataTables"],"typeDamageMult.txt")
   typingInfo = readFile(file)
   for type1 in range(1,18):
      for type2 in range(1,18):
         print(f"{typingInfo[type1][0]} does {typingInfo[type1][type2]}x damage to {typingInfo[0][type2]}")
         # print(f"{typingInfo[type2][0]} does {typingInfo[type2][type1]}x damage to {typingInfo[0][type1]}")


# Just  a bit of code to bulk out my test player to test some functions.
pickleFilePath = selectFile(["SavedObjects","PlayerInstances"],"WJD6K0E4TT")
with open(pickleFilePath, "rb") as pickleFile:
    pickleInfo = pickleFile.read()
    pickleFile.close()
    
player = pickle.loads(pickleInfo)

pokemon = Pokemon("007",5,5,"Wild")
player.captureNewPokemon(pokemon)

player.printStats()
player.party[0].printStats()
player.party[1].printStats()

with open(pickleFilePath, "wb") as pickleFile:
    pickle.dump(player,pickleFile)
    pickleFile.close()


# Generates random Test pokemon to check pokemon generation is working
def generateTestPokemon(amount,minLvl,maxLvl):
    available_species_path = selectFile(["DataTables"],"available_species.txt")
    availableSpecies = readFile(available_species_path," ")
    for i in range(0,amount):
        item = randint(0,len(availableSpecies)-1)
        chosenSpecies = availableSpecies[item][0]
        mypokemon = Pokemon(chosenSpecies,minLvl,maxLvl,"Wild")
        print(f"Generated Pokemon {i  +  1}")
        mypokemon.printStats()
        print("-----------------------------------------------")
        mypokemon.testLeveling()

# -----------------------------------------------------------------------------------------------------
