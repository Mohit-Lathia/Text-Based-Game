from user_inputs import yes_or_no

# Check user inputted string against available command words with reasonable margin for spelling error
def autocorrect(available_words,user_input):
    user_input = user_input.split(" ")
    used_words_lower = []
    checked_positions = []

    # Makes all available words lowercase
    available_words_lower = []
    for word in available_words:
        available_words_lower.append(word.lower())

    # Removing punctuation and checking for exact matches
    for index in range(len(user_input)):
        user_input[index] = user_input[index].strip(r".,;:?!()[]{}''")
        if user_input[index].lower() in available_words_lower:
            used_words_lower.append(user_input[index])
            checked_positions.append(index)

    # Testing similar length words for basic spelling errors
    for index in (x for x in range(len(user_input)) if x not in checked_positions):
        
        test_word = user_input[index]
        for target_word in available_words_lower:
            
            # If word length too different, following checks are skipped
            if not (-3 < (len(test_word) - len(target_word)) < 3):
                break

            i,j = 0,0
            max_i = len(target_word) - 1
            max_j = len(test_word) - 1
            mistakes = 0
            matches = 0

            # Padding Data to avoid Index Errors
            test_word_pad = test_word + " " * 3
            target_word_pad = target_word + " " * 3

            if len(target_word) < len(test_word):
                target_word_pad = target_word + " " * (len(test_word) - len(target_word) + 3)

            elif len(test_word) < len(target_word):
                test_word_pad = test_word + " " * (len(target_word) - len(test_word) + 3)

            # Checking each letter of the target_word against the coresponding letter(s) of test_word
            while i <= max_i and j <= max_j:
                
                # Check if postions match
                if target_word_pad[i] == test_word_pad[j]:
                    matches += 1

                # Checking for subtitution of letters
                elif target_word_pad[i + 1] == test_word_pad[j + 1]:
                    mistakes += 1
                
                elif target_word_pad[i + 2] == test_word_pad[j + 2]:
                    mistakes += 1
                    i,j = i + 1,j + 1

                # Checking for insertion of letters
                elif target_word_pad[i] == test_word_pad[j + 1]:
                    mistakes += 1
                    j += 1

                elif target_word_pad[i] == test_word_pad[j + 2]:
                    mistakes += 1
                    j += 2

                # Checking for deletion of letters
                elif target_word_pad[i + 1] == test_word_pad[j]:
                    mistakes += 1
                    i += 1

                elif target_word_pad[i + 2] == test_word_pad[j]:
                    mistakes += 1
                    i += 2

                else:
                    mistakes += 10
                    break

                i,j = i + 1,j + 1

            if mistakes <= len(target_word) // 3:
                used_words_lower.append(target_word)

    used_words = []
    for word in used_words_lower:
        index = available_words_lower.index(word)
        used_words.append(available_words[index])

    return used_words


#iprovment of input matcher and prompt for clarifcation & unecessary info
def battleInput(player,opponent,opponent_active,pokemon):
    # Get the names of all pokemon,moves and items in plain English
    player_pokemon = []
    for i in range(len(player.party)):
        player_pokemon.append(player.party[i].nickname)

    opponent_pokemon = []
    for i in opponent_active:
        opponent_pokemon.append(opponent.party[i].nickname)
    
    available_moves = []
    for i in range(len(pokemon.knownMoves)):
        available_moves.append(pokemon.knownMoves[i].name)

    available_items = []
    for entry in player.inventory:
        available_items.append(entry)

    options = ["Switch","Check","Flee"]

    all_possible_input = player_pokemon + opponent_pokemon + available_moves + available_items + options

    while True:
        turn_action = ["Player",player.party.index(pokemon)]
        player_amount = 0
        opponent_amount = 0
        move_amount = 0
        item_amount = 0
        option_amount = 0

        user_input = input(" > ")

        used_words = autocorrect(all_possible_input,user_input)

        # Checking how many inputs of eaach category list have been used
        for word in used_words:

            if word in player_pokemon:
                player_amount += 1
            elif word in opponent_pokemon:
                opponent_amount += 1
            elif word in available_moves:
                move_amount += 1
            elif word in available_items:
                item_amount += 1
            elif word in options:
                option_amount += 1
            else:
                print("What. How?")
        
        # Checking fo repeated inputs of the same category type
        invalid_input = False
        selected_values = 0
        for value in [player_amount,opponent_amount,move_amount,item_amount,option_amount]:
            
            if value > 1:
                invalid_input = True
                print("Too many inputs of the same kind, please be specfic about you requests.")
                break
            
            elif value == 1:
                selected_values += 1

            if selected_values > 2:
                invalid_input == True
                print("Too many types of inputs selected")
                break
            
        # Checking for not enough inputs to process request
        if selected_values <= 1 and "Flee" not in used_words:
            invalid_input = True
            print("Not enough input types entered, I don't understand what you mean")
            continue

        # Make sure items are in correct order for interpretting
        try: 
            if used_words[1] in opponent_pokemon + player_pokemon:
                used_words[0],used_words[1] = used_words[1],used_words[0]
        except IndexError:
            pass

        # Checking for correct combination and executing accordingly
        if player_amount == 1 and item_amount == 1:
            turn_action.append("Item")
            turn_action.append(used_words[1])
            turn_action.append("Player")
            player_index = player_pokemon.index(used_words[0])
            turn_action.append(player_index)
            print(f"Use {used_words[1]} on {player_pokemon[player_index]}?")

        elif opponent_amount == 1 and move_amount == 1:
            turn_action.append("Move") 
            move_index = available_moves.index(used_words[1])
            turn_action.append(move_index)
            turn_action.append("Opponent")
            opponent_index = opponent_pokemon.index(used_words[0])
            turn_action.append(opponent_index)
            print(f"Use {available_moves[move_index]} on {opponent_pokemon[opponent_index]}?")

        elif "Switch" in used_words and player_amount == 1:
            turn_action.append("Switch")
            player_index = player_pokemon.index(used_words[0])
            turn_action.append(player_index)
            print(f"Switch to {player_pokemon[player_index]}?")

        elif "Check" in used_words and player_amount == 1:
            pokemon_index = player_pokemon.index(used_words[0])
            player.party[pokemon_index].printBattleStats()
        
        elif "Check" in used_words and opponent_amount == 1:
            pokemon_index = opponent_pokemon.index(used_words[0])
            opponent.party[opponent_active[pokemon_index]].printBattleStats()

        elif "Flee" in used_words:
            turn_action.append("Flee")

        else:
            invalid_input = True
            print("Not a valid combination of inputs catergories.")

        # Prompt user confirmation if and only if a valid input has been inputted
        if ("Check" not in used_words and not invalid_input):
            if yes_or_no(): break

    return turn_action