# A file to control all the things that require user input, so it's easier to see what the chatbot will need to know.
# Will probably see massive changes when the chatbot is properly implemented

from dictonaries import *

Yes = ["y","yep","yes","yeah","alright","certanly","absolutely","yup","ok","okay","indeed","very well","sure","roger","right","agree","aye","affimative"]
No = ["n","not","no","negtive","never","nope","nay"]

# ---------------------------------------------------------------------------------

# Re-Occuring functions, need to be well refined

# For checking user answer when required yes or no
# Could be expanded quite easily with a dictionary for positive and negative confiramtions
def yes_or_no():
    
    while True:
        user_input = input(" > ")
        
        if user_input.lower() in Yes:
            return True
        elif user_input.lower() in No:
            return False
        else:
            print("Not a valid affirmation nor negation. Please try again. ")


# Checking if input matches valid options.
# Will include passing input through functions that work as autocorrect for spelling mistakes or synonyms
def selectOption(options):
    options_lower = []
    for option in options:
        
        if type(option) == list:
            print(f" - " + " ".join(map(str,option)))
        else:
            print(f" - {option}")

        options_lower.append(option.lower())
    
    while True:
        user_input = input(" > ")
        
        if user_input.lower() in options_lower:
            index = options_lower.index(user_input.lower())
            print(f"You want to select {options[index]}?")

            if yes_or_no():
                return options[index]
        
        try:
            
            if 0 < int(user_input) <= len(options):
                print(f"You want to select {options[int(user_input) - 1]}? ")

                if yes_or_no():
                    return options[int(user_input) - 1]

        except:
            pass


# ---------------------------------------------------------------------------------

# Inital setup functions, only runs once, doesn't need too much interpretation

# Ask what name the player would like to use
def pickPlayerName(player):
    namePicked = False
    
    while not namePicked:
        print("What name would you like to use?")
        user_input = input(" > ")
        print(f"You would like to be known as {user_input}. Is that correct? ")
        
        if yes_or_no():
            player.name = user_input
            namePicked = True
        else:
            print(f"I suppose you should give it another try then.")
    
    print(f"Hello {player.name}. It's nice to meet you.")


# Asking what starting pokemon the player would like to use
def pickStartingPokemon(player):
    print(f"""To begin your adventure you are going to require a Pokémon. You may choose from of these three: 
Bulbasaur the Grass type, Charmander the Fire type or Squirtle the Water type.
They might not look very powerful now, but given some time, a bit of practice and plently of love,
I assure you they will grow to be among the powerful Pokémon to ever live. """)
    print(f"So {player.name}, who will it be?")
    user_input = input(" > ")
    starter  = user_input
    validInput = False
    
    while not validInput:
        
        if starter.lower() in ["bulbasaur","charmander","squirtle"]:
            print(f"You would like to take care of {starter}?")
            
            if yes_or_no():
                f"{starter} looks gleefully at you. This might just be the start of a beautiful freindship."
                validInput = True 
            else:
                print(f"I'm sure {starter} will find a trainer in no time, but who to pick instead?")
                starter = input(" > ")
        else:
            print(f"I'm sorry {player.name}, but I'm not sure what you mean. Could you repeat that?")
            starter = input(" > ")
    
    print(f"Would you like to give {starter} a nickname?")
    nickname = starter[0].upper() + starter[1:len(starter)].lower()
    
    if yes_or_no():
        print(f"What would you like {starter} to be known as?")
        user_input = input(" > ")
        nickname = user_input
        assignedName = False
        
        while not assignedName:
            print(f"{nickname}, is that correct? ")
            
            if yes_or_no(): 
                assignedName =  True
            else:
                print("You should probably try again then.")
                nickname = input(" > ")

    return starting_pokemon[starter.lower()], nickname

# ---------------------------------------------------------------------------------

# Roaming functions



# ---------------------------------------------------------------------------------

# Battle-related inputs

# Takes input from the user to return a list with information for the  
def userBattleMain(player,playerPokemonIndex,playerInPlay,opponent,opponentInPlay):
    validInput = False
    playerPokemon = player.party[playerPokemonIndex]
    playerActive = []
    for index in playerInPlay:
        playerActive.append(player.party[index])

    opponentActive = []
    for index in opponentInPlay:
        opponentActive.append(opponent.party[index])

    while not validInput:
        turnAction = ["Player",playerPokemonIndex]
        print(f"\nChoose an action for {playerPokemon.nickname}:")
        print(" 1. Move \n 2. Item \n 3. Switch \n 4. Check \n 5. Flee")
        user_input = input(" > ")

        # If user wants to use a move
        if user_input.lower() in ["1","move"]:
            turnAction.append("Move")
            moveIndex = userBattleMove(player,playerPokemon)
            
            if moveIndex != "":
                turnAction.append(moveIndex)
                turnAction.append("Opponent")
                pokemonIndex = userBattleSelectPokemon(opponentActive,playerPokemon.knownMoves[moveIndex].name)
                turnAction.append(pokemonIndex)
                print(f"You want to use {playerPokemon.knownMoves[moveIndex].name} against {opponentActive[pokemonIndex].nickname}? ")
                validInput = yes_or_no()

        # If user wants to use an item
        elif user_input.lower() in ["2","item"]:
            turnAction.append("Item")
            item = userBattleItem(player.inventory)
            turnAction.append(item)
            
            if item in ["Poke Ball","Great Ball","Ultra Ball","Master Ball"]:
                
                if opponent.context in ["Wild"]:
                    pokemonIndex = userBattleSelectPokemon(opponentActive)
                    turnAction.append("Opponent")
                    turnAction.append(pokemonIndex)
                    print(f"You want to use {item} on {opponent.party[pokemonIndex].nickname}?")
                    validInput = yes_or_no()
                    
                else:
                    print("You cannot catch pokemon in a trainer battle.")
            
            elif item != "":
                turnAction.append("Player")
                pokemonIndex = userBattleSelectPokemon(player.party,item)
                turnAction.append(pokemonIndex)
                print(f"You want to use {item} on {player.party[pokemonIndex].nickname}?")
                validInput = yes_or_no()

        # If user wants to switch to a different Pokemon
        elif user_input.lower() in ["3","switch"]:
            turnAction.append("Switch")
            pokemonIndex = userBattleSelectPokemon(player.party)
            
            if pokemonIndex != "":
                turnAction.append(pokemonIndex)
                print(f"Switch out {playerPokemon.nickname} and switch in {player.party[pokemonIndex].nickname}?")
                validInput = yes_or_no()

        # If user wants to check the stats of a pokemon on the battlefield
        elif user_input.lower() in ["4","check"]:
            checkablePokemon = playerActive + opponentActive
            pokemonIndex = userBattleSelectPokemon(checkablePokemon)
            
            if pokemonIndex != "":
                checkablePokemon[pokemonIndex].printBattleStats()

        # If user want to flee from the battle
        elif user_input.lower() in ["5","flee"]:
            turnAction.append("Flee")
            print("You want to run away? Are you sure?")
            validInput = yes_or_no()

        else:
            print(f"Sorry {player.name}, but I don't know what it is you mean. Could you try again, please?")

    return turnAction


# To pick a move to use from the available moveset
def userBattleMove(player,playerPokemon):
    print(f"\n{playerPokemon.nickname} has available, moves: ")
    validInput = False

    while not validInput:
        for i in range(0,len(playerPokemon.knownMoves)):
            move= playerPokemon.knownMoves[i]
            print(f" {i + 1}. {move.name} Type: {move.typing} Power: {move.power} PP: {move.pp}/{move.maxpp} ")

        print(f"\nWhat move should {playerPokemon.nickname} use?")
        user_input = input(" > ")

        if user_input.lower() == "cancel":
            return ""
        
        try:
            if int(user_input) in range(1,len(playerPokemon.knownMoves) + 1):
                moveIndex = int(user_input) - 1
                validInput = True

            else:
                print(f"Sorry {player.name}, but {playerPokemon.nickname} doesn't have a move with at that index.")

        except ValueError:
            print(f"Sorry {player.name}, but I don't know what it is you mean. Could you try again, please?")

    return moveIndex
        

# To pick and use an item in battle
def userBattleItem(Inventory):
    validInput = False
    
    while not validInput:
        print("Available Items:")
        for item in Inventory:
            print(f" - {item}: {Inventory[item]}")
        
        print("Which item would you like to use? ")
        user_input = input(" > ")
        
        if user_input.lower() == "cancel":
            return ""

        for entry in Inventory:
            if entry.lower() == user_input.lower():
                if Inventory[entry] > 0:
                    item = entry
                    validInput = True
                else:
                    print(f"You don't have any {entry}s to use.")

    return item

        
# To select a pokemon, for either a move, an item or for switching in
def userBattleSelectPokemon(affectablePokemon,action = ""):
    validInput = False

    while not validInput:
        print("\nAffectable Pokémon: ")
        for i in range(len(affectablePokemon)) :
            print(f" - {i + 1}. {affectablePokemon[i].nickname}")

        if action != "switch":
            print(f"\nOn which Pokémon do you want to use {action}? ")
        else:
            print(f"\nWho should switch in?")
        
        user_input = input(" > ")

        if user_input.lower() == "cancel":
            return ""

        try:
            if int(user_input) in range(1,len(affectablePokemon) + 1):
                pokemonIndex = int(user_input) - 1
                validInput = True

            else:
                print("\nThere isn't a Pokémon at the given index. Please re-enter.")

        except ValueError:
            print(f"\nSorry, but I don't know what it is you mean. Could you try again, please?")
        
        if action == "switch" and affectablePokemon[pokemonIndex].isFainted:
            print(f"\n{affectablePokemon[pokemonIndex].nickname} is passed out and cannot be switched to.")
            validInput = False

        if action == "switch" and affectablePokemon[pokemonIndex].isActive:
            print(f"\n{affectablePokemon[pokemonIndex].nickname} is already active and cannot be switched to.")
            validInput = False

    return pokemonIndex


# ---------------------------------------------------------------------------------

# Pokemon Events

# Asks user if they want replace an old move, when their pokemon levels up and tries to learn a new move.
def learnLevelMove(pokemon,newMove):
    print(f"{pokemon.nickname} wants to learn {newMove}.")
    print(f"Would you like {pokemon.nickname} to forget an old move and learn {newMove}?")
    
    if yes_or_no():
        print(f"{pokemon.nickname} knows the moves:")
        
        for move in pokemon.knownMoves:
            print(move.name)
        moveChosen = False
        
        while not moveChosen:
            print(f"Which move should {pokemon.nickname} forget?")
            user_input = input(f" > ")
            
            for i in range(len(pokemon.knownMoves)):
                
                if user_input.lower() == pokemon.knownMoves[i].name.lower():
                    print(f"{pokemon.nickname} should forget {user_input}?")
                    
                    if yes_or_no():
                        pokemon.assignNewMove(pokemon.knownMoves[i],newMove)
                        print(f"{pokemon.nickname} has successfully learnt {newMove}.")
                        moveChosen = True

            if user_input == "cancel":
                print(f"{pokemon.nickname} did not learn {newMove}.")
                break

    else:
        print(f"{pokemon.nickname} did not learn {newMove}.")

# ---------------------------------------------------------------------------------
