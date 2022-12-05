import json
import random
import os



class Item:
    def get_floor(self, map_arr, offset_x, offset_y, remember_bool):
        if remember_bool == 1:
            self.floor = str(map_arr[self.y + offset_y][self.x + offset_x][0])
            return self.floor
        elif remember_bool == 0:
            return str(map_arr[self.y + offset_y][self.x + offset_x][0])

    def draw_item(self, map_arr, offset_x, offset_y):
        map_arr[self.y + offset_y][self.x + offset_x] = [self.char, "i"]
        self.game_pad.addstr(self.y + offset_y, self.x + offset_x, f"{self.char}")

    def draw_floor(self, map_arr, offset_x, offset_y):
        map_arr[self.y + offset_y][self.x + offset_x][0] = [self.floor, "b"]
        if self.floor == ".":
            self.game_pad.addstr(self.y + offset_y, self.x + offset_x, f"{self.floor}", curses.A_DIM)
        else:
            self.game_pad.addstr(self.y + offset_y, self.x + offset_x, f"{self.floor}")


class Weapon(Item):
    def __init__(self, map_arr, game_pad, x, y, name, desc, lvl, dmg, weight):
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.dmg = dmg
        self.weight = weight
        self.char = "("
        self.map = map_arr
        self.game_pad = game_pad

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_item(self.map, 0, 0)

        #print(f"Weapon: {self.name}\n"
        #      f"desc: {self.desc}\n"
        #      f"lvl: {self.lvl}\n"
        #      f"dmg: {self.dmg}\n"
        #      f"character: {self.char}\n"
        #      f"pos: {self.x}, {self.y}\n")
        #print("---------------------------\n")


class Armor(Item):
    def __init__(self, map_arr, game_pad, x, y, name, desc, lvl, defense, weight):
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.defense = defense
        self.weight = weight
        self.char = "T"
        self.map = map_arr
        self.game_pad = game_pad

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_item(self.map, 0, 0)

        #print(f"Armor: {self.name}\n"
        #      f"desc: {self.desc}\n"
        #      f"lvl: {self.lvl}\n"
        #      f"defense: {self.defense}\n"
        #      f"character: {self.char}\n"
        #      f"pos: {self.x}, {self.y}\n")
        #print("---------------------------\n")


class Food(Item):
    def __init__(self, map_arr, game_pad, x, y, name, desc, reg, weight):
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.reg = reg
        self.weight = weight
        self.char = "F"
        self.map = map_arr
        self.game_pad = game_pad

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_item(self.map, 0, 0)

        #print(f"Food: {self.name}\n"
        #      f"desc: {self.desc}\n"
        #      f"regen: {self.reg}\n"
        #      f"character: {self.char}\n"
        #      f"pos: {self.x}, {self.y}\n")
        #print("---------------------------\n")


# Debugging
if __name__ == "__main__":
    os.system("cls")
    with open('Items.json', 'r') as f:
        item_list = json.load(f)
    # print(item_list["weapons"][0]["name"])

    items_world = []
    for i in range(0, 100):
        if random.randrange(0, 100) < 1:
            match random.randrange(0, 3):
                # Weapon creation
                case 0:
                    print(f"#{i + 1} - Weapon\n")
                    weapon_arr = [item for item in
                                  item_list["weapons"][random.randrange(len(item_list["weapons"]))].values()]
                    items_world.append(Weapon(i, 0, weapon_arr[0], weapon_arr[1], weapon_arr[2], weapon_arr[3]))

                # Armor creation
                case 1:
                    print(f"#{i + 1} - Armor\n")
                    armor_arr = [item for item in
                                 item_list["armor"][random.randrange(len(item_list["armor"]))].values()]
                    items_world.append(Armor(i, 0, armor_arr[0], armor_arr[1], armor_arr[2], armor_arr[3]))

                # items_world.append(items.Armor())

                # Food creation
                case 2:
                    print(f"#{i + 1} - Food\n")
                    food_arr = [item for item in
                                item_list["food"][random.randrange(len(item_list["food"]))].values()]
                    items_world.append(Food(i, 0, food_arr[0], food_arr[1], food_arr[2]))
                # items_world.append(items.Weapon())

    #for object in items_world:
    #    print(f"{object.name} - {object.char}")
