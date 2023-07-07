import os
import pickle 

from ProjectDataCleaning.fileControl import *
from class_Pokemon import Pokemon
from other_functions import *
import user_inputs

class Player:
    def __init__(self):
        self.createUniqueID()
        self.createStorageFolder()
        self.money = 0
        self.inventory = {
            "Potion": 10,"Super Potion": 0,"Hyper Potion": 0,"Max Potion": 0,"Full Restore": 0,
            "Antidote": 0,"Burn Heal": 0,"Ice Heal": 0,"Awakening": 0,"Paralyze Heal": 0,"Full Heal": 0,
            "PokeBall": 10,"GreatBall": 0,"UltraBall": 0,"MasterBall": 0}
        self.party = []

        user_inputs.pickPlayerName(self)
        starterID, nickname = user_inputs.pickStartingPokemon(self)
        self.party.append(Pokemon(starterID,5,5,"Player",self.uniqueID))
        self.party[0].nickname = nickname
        self.party[0].picklePokemonObject()

        self.picklePlayerObject()

    # ---------------------------------------------------------------------------------

    # "Behind the Scenes" Admin functions

    # Creates the Unique ID for identifing a specific Player class instance
    def createUniqueID(self):
        player_codes_path = os.path.join(format(os.getcwd()),"SavedObjects","PlayerInstances","player_instance_codes.txt")
        self.uniqueID = generateUniqueReference(player_codes_path)


    # Creates a new Folder in the pokemon Storage Folder for all of pokemon belonging to this player instance
    def createStorageFolder(self):
        player_pokemon_storage = os.path.join(format(os.getcwd()),"SavedObjects","PokemonStorage",self.uniqueID)
        if not os.path.exists(player_pokemon_storage):
            os.makedirs(player_pokemon_storage)
            

    # Pickles pokemon data to the relevant file adn directory
    # This also saves all data for the pokemon in the the players party, which is rather handy
    def picklePlayerObject(self):
        player_pickle_path = os.path.join(format(os.getcwd()),"SavedObjects","PlayerInstances",self.uniqueID)
        if not os.path.exists(player_pickle_path):
            with open(player_pickle_path,"x") as file:
                file.close()
        with open(player_pickle_path,"wb") as pickle_file:
            pickle.dump(self,pickle_file)
            pickle_file.close()

        for pokemon in self.party:
            pokemon.picklePokemonObject()

    
    # ---------------------------------------------------------------------------------

    # In-Game Player Admin functions

    # Swaps the position of two pokemon in the party, mainly so position 0 can be the party leader
    def reorderParty(self,swapFrom,swapTo):
        index1 = self.party.index(swapFrom)
        index2 = self.party.index(swapTo)
        temp = self.party[index1]
        self.party[index1] = self.party[index2]
        self.party[index2] = temp

    
    # Moves pokemon into the current party from the pokemon storage
    def moveToParty(self,pokemonID):
        storage_path = os.path.join(format(os.getcwd()),"SavedObjects","PokemonStorage",self.uniqueID,pokemonID)
        with open(storage_path,"rb") as pokemonFile:
            pokemonInfo =  pokemonFile.read()
            pokemonFile.close()
        pokemon = pickle.loads(pokemonInfo)
        self.party.append(pokemon)


    # Reset relevant values and move pokemon out of party to pokemon storage
    def moveToStorage(self,pokemon_object):
        pokemon_object.resetBattleValues()
        pokemon_object.picklePokemonObject()
        self.party.remove(pokemon_object)

    # ---------------------------------------------------------------------------------

    # Gameplay Mechanics Functions

    # Adds a new pokemon to the players party or to their storage if party is full
    # Also changes relevant attributes and datasets to refelct this
    def captureNewPokemon(self,pokemon):
        pokemon.owner = self.uniqueID
        pokemon.context = "Player"
        if len(self.party) < 6:
            self.party.append(pokemon)
        pokemon_instances_path = os.path.join(format(os.getcwd()),"SavedObjects","PokemonStorage","pokemon_instance_codes.txt")
        pokemon.uniqueID = generateUniqueReference(pokemon_instances_path)
        pokemon.picklePokemonObject()


    # Chooses and processes the move the player will make on any given battle turn
    def chooseBattleAction(self):
        user_inputs.userBattleTurn()


    # Necessary so that a function in Battle class works for both the player and the trainer classes
    def pokemonFainted(self,player_active):
        return user_inputs.userBattleSelectPokemon(self.party,"switch")

    # ---------------------------------------------------------------------------------

    def printStats(self):
        print(f"Name: {self.name}")
        print(f"Unique ID: {self.uniqueID}")
        print(f"Money: {self.money}")
        print(f"\nCurrent Party: ")

        for pokemon in self.party:
            pokemon.printStats()
            print("")


    # ---------------------------------------------------------------------------------

    # Test Functions


    # End of Player class
