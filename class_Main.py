import random, shutil

import user_inputs
from class_Battle import *
from class_Player import *
from class_Trainer import *
from dictonaries import *
from ProjectDataCleaning.fileControl import *

# Contains all the functions that tie the rest of the game together
class Main:
    def __init__(self,selected_inctance = ""):
        self.player = ""
        self.selected_instance = selected_inctance

        self.playerManagment()
        self.roamingLoop("Route 001")

# ---------------------------------------------------------------------------------

# Player Managment Functions
    def playerManagment(self):
        self.loadAllInstances()
        print("--------------------Player Instance Managment--------------------")
        print(f"This is where you can manage existing player instances and make new ones.")
        
        while True:
            print(f"Currently Selected Instance: ")
            choice = user_inputs.selectOption(["Continue","New","Delete"])
            
            if choice == "Continue":
                if self.selected_instance == "":
                    self.selectPlayerInstance()
                self.loadPlayerInstance(self.selected_instance)
                return

            elif choice == "New":
                print("Create a new player instance? ")
                if user_inputs.yes_or_no():
                    self.player = Player()
                    self.selected_instance = self.player.uniqueID
                    return
        
            elif choice == "Select":
                self.selectPlayerInstance()

            elif choice == "Delete":
                if self.selected_instance == "":
                    self.selectPlayerInstance()
                print(f"Are you sure you want to delete {self.selected_instance}?")
                print("It cannot be undone.")

                if user_inputs.yes_or_no():
                    self.deletePlayerInstance(self.selected_instance)

            else:
                print(f"Could you try that again please.")
                

    # Load all valid instance codes of players
    def loadAllInstances(self):
        instances_file_path = selectFile(["SavedObjects","PlayerInstances"],"player_instance_codes.txt")
        with open(instances_file_path, "r") as instances_file:
            self.exisiting_instances = instances_file.readlines()
            instances_file.close()
        for index in range(len(self.exisiting_instances)):
            self.exisiting_instances[index] = self.exisiting_instances[index][:-1]

    
    # Allows a user to select an instance to interact with
    def selectPlayerInstance(self):
        print(f"Which player instance would you like to select?")
        player_instances = self.exisiting_instances[1:]
        for item in player_instances:
            item = item[0]
        self.selected_instance = user_inputs.selectOption(player_instances)


    # Loads the correct player object for the given instance code
    def loadPlayerInstance(self,instance_code):
        storage_path = os.path.join(format(os.getcwd()),"SavedObjects","PlayerInstances",instance_code)
        with open(storage_path,"rb") as playerFile:
            playerInfo =  playerFile.read()
            playerFile.close()
        self.player = pickle.loads(playerInfo)


    # Delete a player instance saved data along with all their saved pokemon data
    def deletePlayerInstance(self,instance_code):
        self.exisiting_instances.remove(instance_code)
        writeable_lines = ["\n"]

        for item in self.exisiting_instances:
            writeable_lines.append(item + "\n")

        instances_file_path = selectFile(["SavedObjects","PlayerInstances"],"player_instance_codes.txt")
        with open(instances_file_path,"w") as file:
            for line in writeable_lines:
                file.writelines(line)
            file.close()


        object_file_path = selectFile(["SavedObjects","PlayerInstances"],self.selected_instance)
        os.remove(object_file_path)

        storage_file_path = selectFile(["SavedObjects","PokemonStorage"],self.selected_instance)
        shutil.rmtree(storage_file_path)

        
# ---------------------------------------------------------------------------------

# Gameplay Loops
    # Main Loop when player is not looking to battle. Used for managing plyaer instances, pokemon party and player inventory
    def neutralLoop(self):
        pass


    # Runs while player is not in an inventory/menu, results in random encounters.
    def roamingLoop(self,location):
        while True:
            total = 0
            cumulative_ratios = []
            for i in encounter_type_ratios[location]:
                total += i
                cumulative_ratios.append(total)

            selected_encounter = random.randint(1,total)

            index = 0
            for i in cumulative_ratios:

                if i < selected_encounter:
                    index += 1
                elif i >= selected_encounter:
                    encounter_type = encounter_type_ratios["Index"][index]
                    break

            # For running correct battle type on battle-related encounters

            if encounter_type == "Trainer":
                
                trainer = Trainer(self.player,"Trainer")
                Battle(self.player,trainer,"1v1")

            elif encounter_type == "Wild":

                trainer = Trainer(self.player,"Wild")
                Battle(self.player,trainer,"Wild")

            elif encounter_type == "Item":
                all_items = list(self.player.inventory.keys())
                item = random.choice(all_items)
                self.player.inventory[item] += 1
                print(f"You found a {item} on the ground. Nice.")

            else:
                print("I'm not sure that this is supposed to be happening.")

