import math

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
format_length = 50  #default value
border_char = "|"   #default value
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
        print(game_vars["bag"].items())
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

#region draw farm functions
def draw_plant_tile(tile_data):
    if tile_data == None:
        tile_data = " " * 5
    print(f"{tile_data:^5}", end="")
    print(border_char, end="")

def draw_player_tile(tile_data):
    if tile_data == None:
        tile_data = " " * 5
    print(f"{tile_data:^5}", end="")
    print(border_char, end="")

def draw_quantity_tile(tile_data):
    if tile_data == None:
        tile_data = " " * 5
    print(f"{tile_data:^5}", end="")
    print(border_char, end="")

def draw_farm(farm_data, rows, columns):
    for row in range(rows):
        tile_data = ""

        print("+" + "-----+" * 5)
        print(border_char, end="")

        for column in range(columns):
            tile_data = farm_data[row][column]  #tile_data set here now that column is known
            draw_plant_tile(tile_data)
        print()

        print(border_char, end="")
        for column in range(columns):
            draw_player_tile(tile_data)
        print()

        print(border_char, end="")
        for column in range(columns):
            print("     " + border_char, end="")

        print()
    print("+" + "-----+" * 5)
#endregion

def in_farm(game_vars, farm_data):

    draw_farm(farm_data, 5, 5)

def show_stats(game_vars):
    print_border_line(format_length, "+", "-")

    line = (f"Day {game_vars['day']} Energy: {game_vars['energy']} Money: ${game_vars['money']}")
    print_formatted_line(line, format_length, border_char)

    if not game_vars["bag"]:
        print_formatted_line("You have no seeds.", format_length, border_char)
    else:
        print_formatted_line("Your seeds:", format_length, border_char)
        for seed in game_vars["bag"]:
            print_formatted_line(f"    {seed}: {game_vars['bag'][seed]}", format_length, border_char)

    print_border_line(format_length, "+", "-")

def end_day(game_vars):
    pass

def save_game(game_vars, farm_data):
    with open ("save_game.txt", "w") as save_file:
        for key in game_vars:
            save_file.write(str(game_vars[key]) + "\n")
            print(key, game_vars[key])

def load_game(game_vars, farm_data):
    try: 
        save_file = open("save_game.txt", "r")
    except FileNotFoundError:
        input("No save game found.")
        return
    
    with open ("save_game.txt", "r") as save_file:
        for key in game_vars:
            game_vars[key] = save_file.readline()
            print(key, game_vars[key])

while True:
    print_border_line(format_length, "-", "-")
    print("Welcome to Sundrop Farm!")
    print()
    print("You took out a loan to buy a small farm in Albatross Town.")
    print("You have 30 days to pay off your debt of $100.")
    print("You might even be able to make a little profit.")
    print("How successful will you be?")
    print_border_line(format_length, "-", "-")

    print("1) Start a new game")
    print("2) Load your saved game")
    print()
    print("0) Exit Game")

    choice = input("Your choice? ")

    match choice:
        case "1":
            in_town(game_vars)

        case "2":
            load_game(game_vars, farm_data)
            in_town(game_vars)

        case "0":
            exit()

        case _:
            # Notify the player of invalid input and waits for acknowledgement
            input("Invalid choice. Please try again.")   
            continue
