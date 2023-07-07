import random

from ProjectDataCleaning.fileControl import *
from dictonaries import *
from other_functions import *
import user_inputs
import input_interpretation

class Battle:
    def __init__(self,player,opponent,battleType):
        self.player = player
        self.opponent = opponent

        self.player_escapes = 0
                
        maxActive = {"1v1": 1,"2v2": 2,"3v3": 3,"Wild": 1}

        self.playerActive = []
        for i in range(0,len(player.party)):
            player.party[i].resetBattleValues()
            if not player.party[i].isFainted and len(self.playerActive) < maxActive[battleType]:
                player.party[i].isActive = True
                self.playerActive.append(i)
                
        self.opponentActive = []
        for i in range(0,maxActive[battleType]):
            opponent.party[i].isActive = True
            self.opponentActive.append(i)
            
        print(f"\nYou are approached by {self.opponent.title} {self.opponent.name}.")
        if battleType != "Wild":
            print(f"{self.opponent.title} {self.opponent.name} has {len(self.opponent.party)} pokemon.")
        print(f"\n{self.opponent.title} {self.opponent.name} sends out {self.opponent.party[self.opponentActive[0]].nickname}.")
        print(f"Go, {self.player.party[self.playerActive[0]].nickname}.")

        self.battleLoop()
        
    # --------------------------------------------------------------

    # Functions that run during the course of the battle

    # Prints relevatnt info at the start of each turn
    def printTurnInfo(self):
        self.turn += 1
        print("----------------------------------------------------------") 
        print(f"Turn {self.turn}")
        print("----------------------------------------------------------") 

        print("\nPlayer Active: ")
        for index in self.playerActive:
            pokemon = self.player.party[index]
            pokemon.printBattleStats()

        print("\nOpponent Active: ")
        for index in self.opponentActive:
            pokemon = self.opponent.party[index]
            pokemon.printBattleStats()

        print("\n----------------------------------------------------------") 

    # The basic battle loop that runs every turn
    def battleLoop(self):
        self.battleOngoing = True
        self.turn = 0
        while self.battleOngoing:
            self.printTurnInfo()

            for i in range(len(self.playerActive)):
                self.player.party[self.playerActive[i]].turnAction = input_interpretation.battleInput(self.player,self.opponent,self.opponentActive,self.player.party[self.playerActive[i]])

            for i in range(len(self.opponentActive)):
                self.opponent.party[self.opponentActive[i]].turnAction = self.opponent.battleTurn(self.opponent.party[self.opponentActive[i]],self.opponentActive,self.playerActive)
            
            self.determineActionOrder()
            
            # Executes all currently items in the action queue, different funnctions called for different action types
            for i in range(len(self.actionQueue)):
                pokemon = self.actionQueue[i][0]
                action = self.actionQueue[i][0].turnAction
                
                if action[2] == "Move" and not pokemon.isFainted:
                    print(action)
                    self.useMove(pokemon,action)
                elif action[2] == "Item":
                    self.useItem(pokemon,action)
                elif action[2] == "Switch":
                    self.switchOut(action)
                elif action[2] == "Flee":
                    self.checkFleeBattle(pokemon)
                
                if not self.battleOngoing:
                        break

            switch_in = self.pokemonUnconcious(self.playerActive,self.player)
            if switch_in not in ["Blackout",None]:
                print(f"Go, {self.player.party[switch_in].nickname}.")
            elif switch_in == "Blackout":
                self.defeat("Blackout")

            switch_in = self.pokemonUnconcious(self.opponentActive,self.opponent)
            if switch_in not in ["Blackout",None]:
                print(f"Opponent sends out {self.opponent.party[switch_in].nickname}.")
            elif switch_in == "Blackout":
                self.victory("Blackout")


    # Checks if any active pokemon become unconcious and then prompts the correct side for a switch in
    def pokemonUnconcious(self,active_list,trainer):
        for active_pokemon in active_list:
            pokemon = trainer.party[active_pokemon]
            if pokemon.actualStats[0] <= 0:
                print(f"\n{pokemon.nickname} has fainted.")
                pokemon.isFainted = True
                pokemon.isActive = False
                remaining_pokemon = False
                for pokemon in trainer.party:
                    if not pokemon.isFainted:
                        remaining_pokemon = True

                if remaining_pokemon:
                    switch_in = trainer.pokemonFainted(active_list)
                    trainer.party[switch_in].isActive = True
                    active_list[active_list.index(active_pokemon)] = switch_in
                    return switch_in
                else:
                    return "Blackout"


    # Determines in what order each action should occur.
    def determineActionOrder(self):
        self.actionQueue = []
        priorityLevels = {"Item":1,"Switch":2,"Flee":3}
        
        # Assing priority for type of action and move priority level
        allActiveActions = []
        for index in self.playerActive:
            allActiveActions.append(self.player.party[index])

        for index in self.opponentActive:
            allActiveActions.append(self.opponent.party[index])
  
        for pokemon in allActiveActions:
            if pokemon.turnAction[2] == "Move":
                priority = pokemon.knownMoves[pokemon.turnAction[3]].priority
                priority += pokemon.actualStats[5]

            else:
                priority = 1000 + priorityLevels[pokemon.turnAction[2]]
            action = [pokemon,priority]
            self.actionQueue.append(action)
        
        
        # Reorders moves based on priority, it is bubble sort and it is very inefficent, but there will be six items max, so it's good enough
        ordered = False
        while not ordered:
            moves = 0
            for i in range(1,len(self.actionQueue)):
                if self.actionQueue[i][1] > self.actionQueue[i - 1][1]:
                    self.actionQueue[i],self.actionQueue[i - 1] = self.actionQueue[i - 1],self.actionQueue[i]
                    moves += 1

            if moves == 0:
                ordered = True


    # Use a named move an inflicts relavant effects
    def useMove(self,pokemon,action):
        if action[4] == "Player":
            target = self.player.party[self.playerActive[action[5]]]
        elif action[4] == "Opponent":
            target = self.opponent.party[self.opponentActive[action[5]]]
        
        move = pokemon.knownMoves[action[3]]
        move.pp -= 1
        moveDamage,appliedMultipliers = calculateDamage(pokemon,target,move)

        hit_amount = random.randint(move.hitAmount[0],move.hitAmount[1])
        
        actual_hit_amount = 0
        for i in range(hit_amount):
            actual_hit_amount += 1
            print(f"\n{pokemon.nickname} used {pokemon.knownMoves[action[3]].name} on {target.nickname}.")
            
            accuracy = battleStageMultipliers[pokemon.baseStatStages[6]] * battleStageMultipliers[target.baseStatStages[7]] * (move.accuracy / 100)
            if random.random() > accuracy:
                print("But it missed!")
                break

            if moveDamage ==  0 and "Nullified" not in appliedMultipliers and move.damageClass != "Status":
                moveDamage = 1

            target.actualStats[0] -= moveDamage
            if target.actualStats[0] <= 0:
                target.actualStats[0] = 0
                target.isFainted = True
                break

            print(f"{target.nickname} took {moveDamage} damage and now has {target.actualStats[0]}/{target.adjustedStats[0]}")

            
        if hit_amount > 1:
            print(f"It hit {actual_hit_amount} times.")


        if action[0] == "Player" and target.actualStats[0] == 0:
                for i in range(6):
                    pokemon.addEVs(target.evYield)
                    self.exp_gain = calulateExperience(pokemon,target)
                    pokemon.addExperience(self.exp_gain)

        if "Nullified" in appliedMultipliers:
            print("It had no effect.")
        elif "Supereffective" in appliedMultipliers and "Ineffective" not in appliedMultipliers:
            print("It was Supereffective.")
        elif "Uneffective" in appliedMultipliers and "Supereffective" not in appliedMultipliers:
            print("It wasn't very effective.")

        if "Critical" in appliedMultipliers:
            print("It was a Critical Hit.")


    def useItem(self,pokemon,action):
        if action[3] in ["Poke Ball","Great Ball","Ultra Ball","Master Ball"]:
            self.usePokeball(action)
        else:
            self.useMedicine(action)

    # Use a specified item and inflict 
    def useMedicine(self,action):
        target = self.player.party[action[5]]
        target_inital_health = target.actualStats[0]
        
        target.actualStats[0] += medicine_stats[action[3]][0]
        if target.actualStats[0] > target.adjustedStats[0]:
            target.actualStats[0] = target.adjustedStats[0]

        heal_amount = target.actualStats[0] - target_inital_health
        if heal_amount > 0:
            print(f"{target.nickname} recovered {heal_amount} health.")
            print(f"{target.nickname} now has {target.actualStats[0]}/{target.adjustedStats[0]}")
        
        for effect in target.effects:
            if effect in medicine_stats[action[3]]:
                target.effects.remove(effect)
                print(f"{target.nickname} recovered from {effect}.")


    # Determines if a target pokemon should be captured when a pokeball is thrown at them
    def usePokeball(self,action):
        target = self.opponent.party[action[5]]
        shake_check = captureRate(target,action[3])

        for i in range(3):
            print("*shake* *shake*")
            if shake_check <= random.randint(0,65535):
                print(f"{target.nicknmae} broke free.")
                return
        
        self.player.captureNewPokemon(target)
        print(f"{target.nickname} successfully caught.")
        self.victory("Capture")


    # Switches out to a desired Pokemon
    def switchOut(self,action):
        if action[0] == "Player":
            index = self.playerActive.index(action[1])
            self.playerActive[index] = action[3]
        elif action[0] == "Opponent":
            index = self.opponentActive.index(action[1])
            self.opponentActive[index] = action[3]


    # Checks if a the battle can be fled, and then acts accordingly
    def checkFleeBattle(self,pokemon):
        print(f"{pokemon.nickname} attempts to flee.")
        self.player_escapes += 1
        if pokemon.actualStats[5] > self.opponent.party[self.opponentActive[0]].actualStats[5]:
            self.defeat("Flee")
        elif escapeOdds(pokemon,self.opponent.party[self.opponentActive[0]],self.player_escapes) < random.randint(0,255):
            self.defeat("Flee")
        else:
            print(f"{pokemon.nickname} did not escape.")

    # --------------------------------------------------------------

    # Functions that run at the end of the battle

    # For all the conditions under which the playe rwins the battle
    def victory(self,reason):

        if reason == "Blackout":
            print(f"{self.opponent.title} {self.opponent.name} has no more pokemon left.")
            
            total_score = 0
            party_size = 0
            for pokemon in self.player.party:
                total_score += pokemon.level
                party_size += 1

            payout = (base_payout[total_score % (10 * party_size)] * random.randint(-30,30) / 100) // 1
            print(f"You win {payout}₽")
            self.player.money += payout


        elif reason == "Capture":
            print("Capture")
        
        self.endBattle()


    # For all the conditions under which the player loses the battle
    def defeat(self,reason):
        if reason ==  "Blackout":
            print("You have no more Pokémon that can fight.")

        elif reason == "Flee":
            print("You managed to successfully flee.")
        
        self.endBattle()


    # The stuff that always has to run at the end of the battle
    def endBattle(self):
        for pokemon in self.player.party:
            pokemon.isActive = False
        self.player.picklePlayerObject()
        self.battleOngoing = False