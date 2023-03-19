import json
import random
import curses
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

    def equip_item(self, p):
        if not (p.entity_class in self.classes):
            return "class"

        if not p.entity_lvl >= self.lvl:
            return "lvl"

        self.is_equiped = True
        return True

    def unequip_item(self):
        if not self.is_equiped:
            return False

        self.is_equiped = False
        return True

    def is_item_in_wear(self, p):
        if len(p.wear_lst) == 0:
            return False

        for item in p.wear_lst:
            if item.wear == self.wear:
                return True
        else:
            return False
    
    def eat_food(self, p):
        p.hp += self.reg
        diff = p.maxhp - p.hp
        if diff < 0:
            p.hp = p.maxhp
            return self.reg + diff
        else:
            return self.reg

    

class Weapon(Item):
    def __init__(self, item_id, map_arr, game_pad, x, y, name, desc,
                 lvl, dmg, weight, classes, wear, stackable,
                 strength, stamina, dexterity, intelligence, luck, defense):

        self.strength = strength
        self.stamina = stamina
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.luck = luck

        self.defense = defense

        self.id = item_id
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
        self.classes = classes
        self.is_equiped = False
        self.wear = wear
        self.stackable = stackable

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_item(self.map, 0, 0)


class Armor(Item):
    def __init__(self, item_id, map_arr, game_pad, x, y, name, desc,
                 lvl, defense, weight, classes, wear, stackable,
                 strength, stamina, dexterity, intelligence, luck, dmg):

        self.strength = strength
        self.stamina = stamina
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.luck = luck

        self.dmg = dmg

        self.id = item_id
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
        self.classes = classes
        self.is_equiped = False
        self.wear = wear
        self.stackable = stackable

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_item(self.map, 0, 0)


class Food(Item):
    def __init__(self, item_id, map_arr, game_pad, x, y, name, desc, reg, weight, stackable):
        self.id = item_id
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.reg = reg
        self.weight = weight
        self.char = "F"
        self.map = map_arr
        self.game_pad = game_pad
        self.stackable = stackable
        self.is_equiped = None

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_item(self.map, 0, 0)

# Debugging -------------------------------------------------------------------


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

    # for object in items_world:
    #     print(f"{object.name} - {object.char}")
