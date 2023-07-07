# If this is still in by accident upon submission, know that this is just a file for testing function before they are integrated
# It just makes them a bit easier to work with an cuts down on general clutter. Although I don't really use it all that much.

import os,random,pickle,math,numpy

from ProjectDataCleaning.fileControl import *
from input_interpretation import *
from class_Main import *
from class_Player import Player
from class_Trainer import Trainer
from class_Battle import Battle

def loadPlayerInstance(player_code):
    pickle_file_path = selectFile(["SavedObjects","PlayerInstances"],player_code)
    with open(pickle_file_path, "rb") as pickle_file:
        pickle_info = pickle_file.read()
        pickle_file.close()
        
    return pickle.loads(pickle_info)

def testBattle(player_code):
    player = loadPlayerInstance(player_code)

    for pokemon in player.party:
        pokemon.resetBattleValues()
        pokemon.update()

    trainer = Trainer(player,"Trainer")

    print(f"\nTrainer: {trainer.title} {trainer.name}")
    print(f"Party:")
    for pokemon in trainer.party:
        print(f"\n - Lvl {pokemon.level} {pokemon.species}")
        for move in pokemon.knownMoves:
            print(f"   > {move.name}")

    Battle(player,trainer,"1v1")

# Main()

# instance_code = Player().uniqueID
# givePokemon(instance_code,"001")
# givePokemon(instance_code,"007")

# testBattle("D65W5KV85H")

moves_file = selectFile(["DataTables"],"full_move_data.txt")
moves_file_lines = readFile(moves_file,"\t")

for line in moves_file_lines:
    print(f"{line[1]}   {line[25]}   {line[28]}   {line[31]}")