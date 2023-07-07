# Generates the oppposing trainers for battles
# At first, they will just be random at an approximated strength
# Might add more stuff later on to refine the process

import os
from math import sqrt
from random import randint

from ProjectDataCleaning.fileControl import *
from class_Pokemon import Pokemon
from dictonaries import *

class Trainer:
    def __init__(self,opponent,context):
        self.context = context
        self.party = []
        self.opponent = opponent

        if context == "Trainer":
            self.generateParty()
            self.title = "Trainer"
            self.name = "Dummy"
        
        elif context == "Wild":
            self.generateWildPokemon()
            self.title = "Wild"
            self.name = self.party[0].nickname
            

    # ---------------------------------------------------------------------------------

    # Generating Tainer and their party
    
    # Makes Trainer party length similar to that of the opponent that is being faced
    def generateParty(self):
        party_size = len(self.opponent.party) + randint(-1,1)
        if party_size > 6: 
            party_size = 6
        if party_size < 1: 
            party_size = 1

    # Makes trainers pokemon a level that should make the fight relatively fair, definetley room for improvent though
        total_player_score =  0
        for pokemon in self.opponent.party:
            total_player_score += pokemon.level ** 2
        baseLvl = sqrt(total_player_score / party_size) // 1

    # Generate a random party for the trainer, that is relatively well balanced level-wise with the player
        available_species_path = selectFile(["DataTables"],"available_species.txt")
        available_species = readFile(available_species_path," ")

        minLvl = int(baseLvl - 3 - (baseLvl * 0.1) // 1) if int(baseLvl - 3 - (baseLvl * 0.1) // 1) > 0 else 1
        maxLvl = int(baseLvl + 3 + (baseLvl * 0.1) // 1)
        for i in range(party_size):
            item = randint(0,len(available_species)-1)
            chosen_species = available_species[item][0]
            self.party.append(Pokemon(chosen_species,minLvl,maxLvl,"Trainer"))


    # Generates a pokemon for a wild encounter
    def generateWildPokemon(self):
        total_level = 0
        for pokemon in self.opponent.party:
            total_level += pokemon.level
        average_level = total_level // len(self.opponent.party)

        available_species_path = selectFile(["DataTables"],"available_species.txt")
        available_species = readFile(available_species_path," ")

        minLvl = int(average_level * 0.85)
        maxLvl = int(average_level * 1.15)

        item = randint(0,len(available_species)-1)
        chosen_species = available_species[item][0]
        self.party.append(Pokemon(chosen_species,minLvl,maxLvl,"Wild"))

    # ---------------------------------------------------------------------------------

    # Gameplay Functions (pretty much just battles though)
    # This'll be the trainers AI, I doubt it'll be too much, just some simple rules.
    
    def battleTurn(self,pokemon,active_pokemon,opp_active_pokemon):
        target_index = randint(0,len(opp_active_pokemon) - 1)
        target = self.opponent.party[opp_active_pokemon[target_index]]

        # Finding relative effectiveness of each move
        move_effectiveness = []
        for move in pokemon.knownMoves:
            multiplier = 1
            for i in range(2):
                if move.typing in type_matching[pokemon.types[i]][2]:
                    multiplier *= 0.5
                elif move.typing in type_matching[pokemon.types[i]][3]:
                    multiplier *= 2
                elif move.typing in type_matching[pokemon.types[i]][4]:
                    multiplier *= 0

                if move.pp == 0:
                    multiplier = -1
                
                if move.damageClass == "Status":
                    multiplier *= 0.5

            move_effectiveness.append(multiplier)

        # Finding moves with the best effectiveness
        most_effective_moves = [0]
        for i in range(1,len(move_effectiveness)):
            if move_effectiveness[most_effective_moves[0]] < move_effectiveness[i]:
                most_effective_moves = [i]
            elif move_effectiveness[most_effective_moves[0]] == move_effectiveness[i]:
                most_effective_moves.append(i)
        
        if len(most_effective_moves) > 1:
            most_effective_moves = [most_effective_moves[randint(0,len(most_effective_moves) - 1)]]
            
        return ["Opponent",self.party.index(pokemon),"Move",most_effective_moves[0],"Player",target_index]


    # Allows the trainer AI to pick a new pokemon should an active one faint
    def pokemonFainted(self,active_pokemon):
        available_pokemon = []
        for i in range(len(self.party)):
            if not self.party[i].isFainted and i not in active_pokemon:
                available_pokemon.append(i)
        return available_pokemon[randint(0,len(available_pokemon) - 1)]


    # ---------------------------------------------------------------------------------

    # Just print relevant information about the trainers attributes
    def printPartyStats(self):
        print(f"{self.title} {self.name}")
        print("Party: ")
        for pokemon in self.party:
            stats = pokemon.actualStats
            moves = pokemon.knownMoves
            print("--------------------------------------------------")
            print(f" > Lvl {pokemon.level} {pokemon.species}")
            print(f"   Typing: {pokemon.types[0]} {pokemon.types[1]}")
            print(f"   Health: {pokemon.actualStats[0]}/{pokemon.adjustedStats[0]}")
            print(f"   Stats: ATK:{stats[1]} DEF:{stats[2]} SPA:{stats[3]} SPD:{stats[4]} SPE:{stats[5]}")
            print(f"   Available Moves: ")
            for move in moves:
                print(f"     - {move.name}")
            
    # ---------------------------------------------------------------------------------

    # End of Trainer Class
