from ProjectDataCleaning.fileControl import *
from dictonaries import *

# Assigns all realted information to a move, for a given pokemon.
class Move:
    def __init__(self,moveName):
        movesFile = selectFile(["DataTables"],"full_move_data.txt")
        moveFileLines = readFile(movesFile,"\t")

        for line in moveFileLines:
            if moveName in line:
                moveInformation = line

        # As I am using two different sources for moves and pokemon, sometimes names don't quite line up
        # Try function is only necessary while I am testing.
        try: 
            self.name = moveName
        except UnboundLocalError:
                print(f"Error. {moveName} could not be found.")
                exit()

        self.moveID = moveInformation[0]
        self.typing = type_IDs[int(moveInformation[5]) + 1]
        self.damageClass = move_damage_classes[int(moveInformation[7]) + 1]
        self.power = int(moveInformation[8])
        self.accuracy = int(moveInformation[9])
        self.pp = int(moveInformation[10])
        self.maxpp = int(moveInformation[10])
        self.priority = int(moveInformation[11])
        self.critStage = int(moveInformation[19])
        self.recoilChance = int(moveInformation[20])
        self.flinchChance = int(moveInformation[22])

        self.statChanges = [[],[],[]]
        for i in range(9):
            self.statChanges[i % 3].append(moveInformation[25 + i])


        self.hitAmount = [int(moveInformation[13]),int(moveInformation[12])]
        if self.hitAmount == [0,0]:
            self.hitAmount = [1,1]

        self.turnAmount = [int(moveInformation[17]),int(moveInformation[18])]
        if self.turnAmount == [0,0]:
            self.turnAmount = [1,1]



    # Prints move values to terminal, mainly just for checking everything is working
    def printMoveValues(self):
        print(f"Move ID: {self.moveID}")
        print(f"Move Name: {self.name}")
        print(f"Typing: {self.typing}")
        print(f"Damage Class: {self.damageClass}")
        print(f"Power: {self.power}")
        print(f"Hit No.: {self.hitAmount[0]}-{self.hitAmount[1]}")
        print(f"Turn No.: {self.turnAmount[0]}-{self.turnAmount[1]}")
        print(f"PP: {self.pp}")
        print(f"Accuracy: {self.accuracy}")
        print(f"Priority: {self.priority}")


    # End of Move Class
    