from math import sqrt
import random
from dictonaries import *
import user_inputs

# Stats are based on this formula and I think it is redone every levelup, based on experience
# Level: 1-100; IV: 0 - 31 per Stat; EV: 0 - 255 per stat, 510 across all stats cumulatively (Wild Pokemon have none)
# Nature Modifier for health should always be just one and will be either 0.9,1 or 1.1 for all other stats
def calculateStat(base,level,IV,EV,isHP,natureModifier,stage = 0):
    stat = ((2 * base + IV + (EV//4)) * level) // 100
    if isHP:
        stat += level + 5
    stat += 5
    stat *= statStageMultiplers[stage]
    stat *= natureModifier
    stat = int(stat // 1)
    return stat


# The base damage of an attack is determined by a constant formula based on the intrinsic attributes of both pokemon and the move used
# Several external factors are then applied, there are quite a few of them
def calculateDamage(attacker,defender,move):
    if move.damageClass == "Physical":
        damage = (((2 * attacker.level)//5 + 2) * move.power * attacker.actualStats[2]//defender.actualStats[1])//20 + 2
    elif move.damageClass == "Special":
        damage = (((2 * attacker.level)//5 + 2) * move.power * attacker.actualStats[4]//defender.actualStats[5])//20 + 2
    elif move.damageClass == "Status":
        return 0,[]

    appliedMultipliers = []

    # Typing related damage multipliers
    for i in range(2):

        if defender.types[i] in type_matching[move.typing][0]:
            damage *= 2
            appliedMultipliers.append("Supereffective")
        elif defender.types[i] in type_matching[move.typing][1]:
            damage *= 0.5
            appliedMultipliers.append("Ineffective")
        elif defender.types[i] in type_matching[move.typing][5]:
            damage *= 0
            appliedMultipliers.append("Nullified")

    # Randomly applies critical hits
    if random.randint(1,critStages[move.critStage]) == 1:
        damage *= 2
        appliedMultipliers.append("Critical")
        
    return int(damage // 1),appliedMultipliers


# Calculate experience gain from a pokemon fainting 
def calulateExperience(attacker,target):
    exp = (target.base_exp * target.level) // 5
    exp *= (2 * (target.level + 10) // (target.level + attacker.level + 10)) ** 2.5 + 1
    return exp


# Calulates the relative likelihood of an escape attempt being successful
def escapeOdds(attacker,target,escape_attempts):
    return ((attacker.actualStats[5] * 128) // target.actualStats[5] + 30 * escape_attempts) % 256


# Relative likelihood of a wild pokemon being caught 
def captureRate(target,pokeball):
    a = 3 * target.adjustedStats[0] - 2 * target.actualStats[0]
    a *= 4096 * int(target.base_catch_chance) * pokeball_catch_multiplier[pokeball]
    a //= 3 * target.adjustedStats[0]

    shake_check = 1048560 // sqrt(sqrt(16711680//a))
    
    return shake_check


# Generates a unique string of length 10 to identify pokemon and player objects
# There is absolutely no need for it to be done this way, I just prefer it to straight up numbering them
def generateUniqueReference(existing_instances_path):
   with open(existing_instances_path,"r") as file:
      existingInstances = file.readlines()
      file.close()
   
   uniqueString = False
   while not uniqueString:
    string = ""

    for i in range(10):
        string += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    string += "\n"

    if string not in existingInstances:
        existingInstances.append(string)
        uniqueString = True
   
    with open(existing_instances_path,"w") as file:
        for line in existingInstances:
            file.writelines(line)
        file.close()

   return string[0:-1]


# To be run at any point to break out of current game and return to start
def gameBreak(player_instance):
    print(f"Are you sure that you want to exit?")
    if user_inputs.yes_or_no():
        exit()

