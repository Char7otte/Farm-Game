import math

player_position = [2, 2]

game_vars = {
    'day': 1,
    'energy': 10,
    'money': 20,
    'bag': {},
}

seed_list = ['LET', 'POT', 'CAU']
seeds = {
    'LET': {'name': 'Lettuce',
            'price': 2,
            'growth_time': 2,
            'crop_price': 3
            },

    'POT': {'name': 'Potato',
            'price': 3,
            'growth_time': 3,
            'crop_price': 6
            },

    'CAU': {'name': 'Cauliflower',
            'price': 5,
            'growth_time': 6,
            'crop_price': 14
            },
}

farm_data = [ 
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, 'HSE', None, None],
    [None, None, None, None, None],
    [None, None, None, None, None] ]

#region format functions for the game's menus
def print_border_line(length, border_char, fill_char):
    print(border_char + fill_char * (length - 2) + border_char)
    return

def print_formatted_line(string, length, border_char):
    print(border_char + " " + string + " " * (length - len(string) - 3) + border_char)
    return
#endregion

def in_town(game_vars):
    while True:
        show_stats(game_vars)

        print("You are in Albatross Town")
        print_border_line(25, "-", "-")
        print("1) Visit Shop")
        print("2) Visit Farm")
        print("3) End Day")
        print()
        print("9) Save Game")
        print("0) Exit Game")
        print_border_line(25, "-", "-")
        choice = input("Your choice? ")

        match choice:
            case "1":
                in_shop(game_vars)
                break

            case "2":
                in_farm(game_vars, farm_data)
                break

            case "3":
                end_day(game_vars)

            case "9":
                save_game(game_vars, farm_data)

            case "0":
                exit()

            case _:
                # Notify the player of invalid input and waits for acknowledgement
                input("Invalid choice. Please try again.")   
                continue

def buy_seeds(game_vars, seed):
    money = game_vars["money"]
    seed_name = seed["name"]
    seed_price = seed["price"]

    print(f"You have ${money}")
    buy_quantity = int(input("How many do you wish to buy? "))
    total_cost = seed_price * buy_quantity

    if money >= total_cost:
        print(f"You bought {buy_quantity} {seed_name} seeds.")
        game_vars["money"] -= total_cost
        if seed_name in game_vars["bag"]:
            game_vars["bag"][seed_name] += buy_quantity
        else:
            game_vars["bag"][seed_name] = buy_quantity
    else:
        input("You can't afford that!")
    
def in_shop(game_vars):
    shop_string_format = "{:<15}{:^9}{:^13}{:^13}"
    print("Welcome to Pierce's Seed Shop!")

    while True:
        show_stats(game_vars)
        print("What do you wish to buy?")
        print(shop_string_format.format("Seed", "Price", "Days to Grow", "Crop Price"))
        print_border_line(48, "-", "-")

        x = 0
        for seed_key in seeds:
            x += 1

            seed_value_dict = seeds[seed_key]

            name = seed_value_dict["name"]
            name_display = f"{x}) {name}"
            price = seed_value_dict["price"]
            growth_time = seed_value_dict["growth_time"]
            crop_price = seed_value_dict["crop_price"]

            print(shop_string_format.format(name_display, price, growth_time, crop_price))
        
        print()
        print("0) Leave")
        print_border_line(48, "-", "-")
        choice = input("Your choice? ")

        match choice:
            case "1":
                buy_seeds(game_vars, seeds["LET"])
            case "2":
                buy_seeds(game_vars, seeds["POT"])
            case "3":
                buy_seeds(game_vars, seeds["CAU"])
            case "0":
                in_town(game_vars)
            case _:
                # Notify the player of invalid input and waits for acknowledgement
                input("Invalid choice. Please try again.")   
                continue

def draw_farm(farm_data, farm_size, player_position = [2, 2]):
    rows = farm_size[0]
    columns = farm_size[1]

    for row in range(rows):
        print("+" + "-----+" * 5)

        #region info row
        print("|", end="")
        for column in range(columns):
            tile_data = farm_data[row][column]
            if tile_data == None:
                tile_data = " " * 5
            print(f"{tile_data:^5}", end="")
            print("|", end="")
        print()
        #endregion

        #region player row
        print("|", end="")
        for column in range(columns):
            if [row, column] == player_position:
                tile_data = "X"
            else:
                tile_data = " " * 5
            print(f"{tile_data:^5}", end="")
            print("|", end="")
        print()
        #endregion

        #region quantity row
        print("|", end="")
        for column in range(columns):
            if tile_data == None:
                tile_data = " " * 5
            print(f"{tile_data:^5}", end="")
            print("|", end="")
        #endregion

        print()
    print("+" + "-----+" * 5)

def move_player(player_position, movement):
    player_row, player_column = player_position
    row_move, column_move = movement
    player_row += row_move
    player_column += column_move

    if player_row < 0 or player_row > 4 or player_column < 0 or player_column > 4:
        input("You can't go that way.")
        return
    return [player_row, player_column]

def in_farm(game_vars, farm_data):
    global player_position
    while True:
        draw_farm(farm_data, (5,5), player_position)

        print(f"Energy: {game_vars["energy"]}")
        print("[WASD] Move")
        print("R)eturn to Town")
        choice = input("Your choice? ").lower()

        match choice:
            case "w":
                decision = move_player(player_position, [-1, 0])
            case "a":
                decision = move_player(player_position, [0, -1])
            case "s":
                decision = move_player(player_position, [1, 0])
            case "d":
                decision = move_player(player_position, [0, 1])
            case "r":
                in_town(game_vars)
            case _:
                # Notify the player of invalid input and waits for acknowledgement
                input("Invalid choice. Please try again.")
                continue

        if decision == None:
            continue
        else:
            player_position = decision

def show_stats(game_vars):
    print_border_line(50, "+", "-")

    line = (f"Day {game_vars['day']} Energy: {game_vars['energy']} Money: ${game_vars['money']}")
    print_formatted_line(line, 50, "|")

    if not game_vars["bag"]:
        print_formatted_line("You have no seeds.", 50, "|")
    else:
        print_formatted_line("Your seeds:", 50, "|")
        for seed in game_vars["bag"]:
            print_formatted_line(f"    {seed}: {game_vars['bag'][seed]}", 50, "|")

    print_border_line(50, "+", "-")

def end_day(game_vars):
    pass

def save_game(game_vars, farm_data):
    with open ("save_game.txt", "w") as save_file:
        for key in game_vars:
            save_file.write(str(game_vars[key]) + "\n")
            print(key, game_vars[key])

def load_game(game_vars):
    try: 
        save_file = open("save_game.txt", "r")
    except FileNotFoundError:
        input("No save game found.")
        return
    
    with open ("save_game.txt", "r") as save_file:
        for key in game_vars:
            game_vars[key] = save_file.readline()
            print(key, game_vars[key])
        
        in_town(game_vars)

while True:
    print_border_line(50, "-", "-")
    print("Welcome to Sundrop Farm!")
    print()
    print("You took out a loan to buy a small farm in Albatross Town.")
    print("You have 30 days to pay off your debt of $100.")
    print("You might even be able to make a little profit.")
    print("How successful will you be?")
    print_border_line(50, "-", "-")

    print("1) Start a new game")
    print("2) Load your saved game")
    print()
    print("0) Exit Game")

    choice = input("Your choice? ")

    match choice:
        case "1":
            in_town(game_vars)

        case "2":
            load_game(game_vars)

        case "0":
            exit()

        case _:
            # Notify the player of invalid input and waits for acknowledgement
            input("Invalid choice. Please try again.")   
            continue
