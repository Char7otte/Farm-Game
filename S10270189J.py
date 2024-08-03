import math

#region game variables
player_variables = {
    "day": 1,
    "energy": 10,
    "money": 20,
    "position": [2, 2],
    "seed_bag": {},
}

farm_layout = [ 
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, {"HSE": None}, None, None],
    [None, None, None, None, None],
    [None, None, None, None, None] ]

seed_list = {
    "Lettuce": 
        {"name": "Lettuce",
        "id": "LET",
        "price": 2,
        "growth_time": 2,
        "crop_price": 3
        },
    "Potato": 
        {"name": "Potato",
        "id": "POT",
        "price": 3,
        "growth_time": 3,
        "crop_price": 6
        },
    "Cauliflower": 
        {"name": "Cauliflower",
        "id": "CAU",
        "price": 5,
        "growth_time": 6,
        "crop_price": 14
        },
}
#endregion

def try_choice():
    try:
        choice = input("Your choice? ")
    except:
        throw_error()
        return None
    return choice

def throw_error():
    input("Invalid choice. Please try again.")

#region format functions for the game's menus
def print_border_line(length, border_char, fill_char):
    print(border_char + fill_char * (length - 2) + border_char)
    return

def print_formatted_line(string, length, border_char):
    print(border_char + " " + string + " " * (length - len(string) - 3) + border_char)
    return
#endregion


#region Town Menu
def print_in_town_menu(variables):
    show_stats(variables)
    print("You are in Albatross Town")
    print_border_line(25, "-", "-")
    print("1) Visit Shop")
    print("2) Visit Farm")
    print("3) End Day")
    print()
    print("9) Save Game")
    print("0) Exit Game")
    print_border_line(25, "-", "-")

def in_town(variables, farm_data, seed_data):
    print_in_town_menu(variables)
    try:
        choice = input("Your choice? ")
    except:
        throw_error()
        in_town(variables, farm_data, seed_data)

    if choice == "0":
        exit()
    elif choice == "1":
        print("Welcome to Pierce's Seed Shop!")
        in_shop(variables, farm_data, seed_data)
    elif choice == "2":
        variables["position"] = [2, 2]
        in_farm(variables, farm_data, seed_data)
    elif choice == "3":
        end_day(variables, farm_data, seed_data)
    elif choice == "9":
        save_game(variables, farm_data)
        input("Game saved.")
        in_town(variables, farm_data, seed_data)
    else:
        throw_error()
        in_town(variables, farm_data, seed_data)
#endregion


#region Shop Menu
def buy_seeds(variables, seed_info):
    player_money = variables["money"]
    seed_name = seed_info["name"]
    seed_price = seed_info["price"]

    print(f"You have ${player_money}")
    buy_quantity = int(input("How many do you wish to buy? "))
    total_cost = seed_price * buy_quantity

    if player_money >= total_cost:
        print(f"You bought {buy_quantity} {seed_name} seeds.")
        variables["money"] -= total_cost
        if seed_name in variables["seed_bag"]:
            variables["seed_bag"][seed_name] += buy_quantity
        else:
            variables["seed_bag"][seed_name] = buy_quantity
    else:
        input("You can't afford that!")

def print_shop_menu(variables, seed_data):
    shop_string_format = "{:<15}{:^9}{:^13}{:^13}"

    show_stats(variables)
    print("What do you wish to buy?")
    print(shop_string_format.format("Seed", "Price", "Days to Grow", "Crop Price"))
    print_border_line(48, "-", "-")

    x = 0
    for seed in seed_data:
        x += 1

        seed_info = seed_data[seed]

        name = seed_info["name"]
        name_display = f"{x}) {name}"
        price = seed_info["price"]
        growth_time = seed_info["growth_time"]  
        crop_price = seed_info["crop_price"]

        print(shop_string_format.format(name_display, price, growth_time, crop_price))
    
    print()
    print("0) Leave")
    print_border_line(48, "-", "-")

def in_shop(variables, farm_data, seed_data):
    print_shop_menu(variables, seed_data)
    choice = try_choice()

    if choice == "0":
        in_town(variables, farm_data, seed_data)
    elif choice == "1":
        buy_seeds(variables, seed_data["Lettuce"])
        in_shop(variables, farm_data, seed_data)
    elif choice == "2":
        buy_seeds(variables, seed_data["Potato"])
        in_shop(variables, farm_data, seed_data)
    elif choice == "3":
        buy_seeds(variables, seed_data["Cauliflower"])
        in_shop(variables, farm_data, seed_data)
    else:
        throw_error()
        in_shop(variables, farm_data, seed_data)
#endregion


#region Farm

def use_energy(variables):
    if variables["energy"] == 0:
        input("You have no energy left.")
        return False
    variables["energy"] -= 1

def draw_farm(farm_data, farm_size, player_position):
    rows = farm_size[0]
    columns = farm_size[1]

    for row in range(rows):
        print("+" + "-----+" * 5)

        #region name row
        print("|", end="")
        for column in range(columns):
            tile_data = farm_data[row][column]

            if tile_data == None:
                print_string = " " * 5
            else:
                print_string = list(tile_data)[0]

            print(f"{print_string:^5}|" , end="")
        print()
        #endregion

        #region position row
        print("|", end="")
        for column in range(columns):
            if [row, column] == player_position:
                print_string = "X"
            else:
                print_string = " " * 5
            print(f"{print_string:^5}|", end="")
        print()
        #endregion

        #region quantity row
        print("|", end="")
        for column in range(columns):
            tile_data = farm_data[row][column]
            try:
                key = list(tile_data)[0]
                quantity = tile_data[key]
                print_string = quantity
                print(f"{print_string:^5}|" , end="")
            except:
                print_string = " " * 5
                print(f"{print_string:^5}|" , end="")
        #endregion

        print()
    print("+" + "-----+" * 5)


def print_farm_menu(variables, farm_data):
    draw_farm(farm_data, (5,5), variables["position"])

    print(f"Energy: {variables["energy"]}")
    print("[WASD] Move")
    player_row = variables["position"][0]
    player_column = variables["position"][1]
    current_tile = farm_data[player_row][player_column]
    if current_tile == None and variables["seed_bag"]:   #Checks if the player is on an empty plot and has seeds
        print("P)lant seed")
    elif current_tile != None:
        for seed_name, remaining_growth_time in current_tile.items():
            if remaining_growth_time == 0:
                print("H)arvest")
    print("R)eturn to Town")


def move_player(variables, farm_data, seed_data, choice):
    if choice == "W":
        movement = (-1, 0)
    elif choice == "S":
        movement = (1, 0)
    elif choice == "A":
        movement = (0, -1)
    elif choice == "D":
        movement = (0, 1)

    player_row, player_column = variables["position"][0], variables["position"][1]
    new_player_row, new_player_column = player_row + movement[0], player_column + movement[1]

    if new_player_row < 0 or new_player_row > 4 or new_player_column < 0 or new_player_column > 4:
        input("You can't go that way.")
    elif use_energy(variables) == False:
        in_farm(variables, farm_data, seed_data)
    else:
        variables["position"] = [new_player_row, new_player_column]


def print_planting_menu(variables, seed_data):
    plant_string_format = "{:15}{:^13}{:^13}{:^13}"
    seed_bag = variables["seed_bag"]

    print("What do you wish to plant?")
    print_border_line(50, "-", "-")
    print(plant_string_format.format("    Seed", "Days to Grow", "Crop Price", "Available"))
    print_border_line(50, "-", "-")

    x = 0
    for seed_name, quantity in seed_bag.items():
        x += 1
        name_display = f"{x}) {seed_name}"

        seed_info = seed_data[seed_name]

        growth_time = seed_info["growth_time"]
        crop_price = seed_info["crop_price"]
      
        print(plant_string_format.format(name_display, growth_time, crop_price, quantity))
    
    print()
    print("0) Leave")
    print_border_line(50, "-", "-")


def plant_seed(variables, farm_data, seed_data):
    print_planting_menu(variables, seed_data)
    
    choice = try_choice()
    list_of_available_seeds = list(variables["seed_bag"].keys())

    try:
        choice = int(choice) - 1 #Subtract 1 to match the index of the seed bag
    except IndexError:
        input(f"You only have {len(list_of_available_seeds)} seeds to pick from.")
        plant_seed(variables, farm_data, seed_data)
    except:
        throw_error()
        plant_seed(variables, farm_data, seed_data)

    selected_seed = list_of_available_seeds[choice]
    selected_seed_data = seed_data[selected_seed]
    plant_id = selected_seed_data["id"]
    plant_remaining_growth_time = selected_seed_data["growth_time"]
    
    player_row, player_column = variables["position"]
    farm_data[player_row][player_column] = {plant_id: plant_remaining_growth_time}
    variables["seed_bag"][selected_seed] -= 1
    in_farm(variables, farm_data, seed_data)


def in_farm(variables, farm_data, seed_data):
    print_farm_menu(variables, farm_data)
    choice = try_choice().upper()
    current_tile = farm_data[variables["position"][0]][variables["position"][1]]

    if choice == "W" or choice == "S" or choice =="A" or choice == "D":
        move_player(variables, farm_data, seed_data, choice)
        in_farm(variables, farm_data, seed_data)
    elif choice == "P":
        if not current_tile == None:
            input("You can't plant seeds here.")
            in_farm(variables, farm_data, seed_data)
        else:
            if not variables["seed_bag"]:
                input("You have no seeds.")
                in_farm(variables, farm_data, seed_data)
            else:
                if use_energy(variables) == False:
                    in_farm(variables, farm_data, seed_data)
                plant_seed(variables, farm_data, seed_data)
    elif choice == "R":
        in_town(variables, farm_data, seed_data)
    else:
        throw_error()
        in_farm(variables, farm_data, seed_data)
#endregion

def show_stats(variables):
    day = variables["day"]
    energy = variables["energy"]
    money = variables["money"]
    seed_bag = variables["seed_bag"]

    print_border_line(50, "+", "-")
    print_formatted_line((f"Day: {day} Energy: {energy} Money: ${money}"), 50, "|")

    #region print seed bag
    if not seed_bag:
        print_formatted_line("You have no seeds.", 50, "|")
    else:
        print_formatted_line("Your seeds:", 50, "|")
        for seed in seed_bag:
            print_formatted_line(f"    {seed + ":":<13} {seed_bag[seed]:<5}", 50, "|")
    #endregion

    print_border_line(50, "+", "-")

def end_day(variables, farm_data, seed_data):
    variables["day"] += 1
    variables["energy"] = 10
    variables["position"] = [2, 2]

    x = 0
    for row in farm_data:
        y = 0
        for column in row:
            y += 1
            if column == None:
                continue
            for seed_name, remaining_growth_time in column.items():  
                if seed_name == "HSE":
                    continue        
                if remaining_growth_time > 0:
                    print(x, y)
                    farm_data[x][y - 1] = {seed_name: remaining_growth_time - 1}
        x += 1
    in_town(variables, farm_data, seed_data)


#region Save and Load functions
def save_game(variables, farm_data):
    with open ("save_game.txt", "w") as save_file:
        for key in variables:
            save_file.write(f"{variables[key]}\n")
        
        for element in farm_data:
            save_file.write(f"{element}\n")

def reformat_position(position):
    fixed_position = []
    x = 0
    fixed_position = position.replace("[", "").replace("]", "").replace(" ", "").split(",")
    return [int(fixed_position[0]), int(fixed_position[1])]

def reformat_seed_bag(seed_bag):
    bag = {}
    x = 0
    fixed_seed_bag = seed_bag.replace("{", "").replace("}", "").replace("'", "").replace(" ", "").split(",")

    try:    #Try in case there are no seeds in the save file
        for element in fixed_seed_bag:
            element = element.split(":")
            name = element[0]
            quantity = int(element[1])
            bag[name] = quantity
    except:
        return None
    
    return bag

def load_save_data(variables, farm_data):
    try:
        with open ("save_game.txt", "r") as save_file:

            variables["day"] = int(save_file.readline().strip())

            variables["energy"] = int(save_file.readline().strip())

            variables["money"] = int(save_file.readline().strip())

            variables["position"] = reformat_position(save_file.readline().strip())

            variables["seed_bag"] = reformat_seed_bag(save_file.readline().strip())

            farm = []
            new_farm = []
            for line in save_file:
                line = line.replace("[", "").replace("]", "").replace(" ", "")
                farm.append(line.strip())
            for element in farm:
                split_element = element.split(",")
                new_farm.append(split_element)
            x = 0
            for row in new_farm:
                y = 0
                for column in row:
                    if column == "None":
                        new_farm[x][y] = None
                    else:
                        column = column.replace("{", "").replace("}", "").replace("'", "").replace(" ", "").split(":")
                        try:
                            quantity = int(column[1])
                        except:
                            quantity = None
                        new_farm[x][y] = {column[0]: quantity}
                    y += 1
                x += 1  
            farm_data = new_farm
    except FileNotFoundError:
        input("No save game found.")
        return 
    except:
        input("Save file is corrupt.")
        return
              
    return farm_data
    
#endregion


#region Start Menu
def print_start_menu():
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


def main(variables, farm_data, seed_data):
    print_start_menu()
    choice = try_choice()

    if choice == "0":
        exit()
    elif choice == "1":
        in_town(variables, farm_data, seed_data)
    elif choice == "2":
        decision = load_save_data(variables, farm_data)
        if decision == None:
            main(variables, farm_data, seed_data)
            
        farm_data = decision
        in_town(variables, farm_data, seed_data)
    else:
        throw_error()
        main(variables, farm_data, seed_data)
#endregion


main(player_variables, farm_layout, seed_list)