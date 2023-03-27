import os
import curses
import random
import json
import logging
import math
import time

from curses import wrapper
from curses.textpad import Textbox, rectangle
import curses.panel
from perlin_noise import PerlinNoise

from player import Player
from hud import Window, Menu
import hud
from camera import Camera
from items import Weapon, Armor, Food
from race import Race
from role import Role
from enemy import Enemy, create_enemy
import fight


game_menu_bool = False
in_game_bool = False
main_loop = False
char_naming = False
char_race = False
char_role = False
char_confirm = False

def main(stdscr):
    global game_menu_bool
    global in_game_bool
    global main_loop
    global char_naming
    global char_race
    global char_role
    global char_confirm
    global in_fight
    global rows, cols
    
    rows, cols = stdscr.getmaxyx()
    hrows = (rows // 2)
    hcols = (cols // 2)

    stdscr.clear()
    curses.curs_set(False)

    #player_name = ""
    #player_race = ""

    def game(player_name, player_race, player_role, stats_sum):
        global game_menu_bool
        global in_game_bool
        global main_loop
        global char_naming
        global char_race
        global char_role
        global char_confirm
        global rows, cols
        
        stdscr.clear()
        LOADING_LABEL = "Generating terrain..."
        stdscr.addstr((rows // 2), (cols // 2) - 9, LOADING_LABEL)
        stdscr.refresh()

        CAM_WIDTH = cols-47 #161
        CAM_HEIGHT = rows-16#35
        GAME_X = 600 + 1
        GAME_Y = 600 + 1
        CAM_X = GAME_X // 2 - CAM_WIDTH // 2
        CAM_Y = GAME_Y // 2 - CAM_HEIGHT // 2

        cam = Camera(CAM_WIDTH, CAM_HEIGHT, CAM_X, CAM_Y)

        OCTAVE = 26  # random.randrange(25, 30)

        noise = PerlinNoise(octaves=OCTAVE, seed=random.randrange(0, 100000000))  # random.randrange(0, 100000)

        #map = [[noise([i / (GAME_X * 0.2), j / (GAME_Y * 1.7)]) for j in range(GAME_X)] for i in range(GAME_Y)]

        # curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
        # BLUE_AND_YELLOW = curses.color_pair(1)

        game_pad = curses.newpad(GAME_Y, GAME_X)
        # player_win = curses.newwin(CAM_HEIGHT, CAM_WIDTH, 1, 0)
        stdscr.refresh()
        curses.curs_set(False)

        map = [[noise([(i / GAME_X), (j / GAME_Y)*0.8]) for j in range(GAME_X)] for i in range(GAME_Y)]

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] < -0.5:
                    map[i][j] = [".", "b"]  # " "
                elif -0.5 <= map[i][j] < -0.4:
                    map[i][j] = [".", "b"]  # .
                elif -0.4 <= map[i][j] < -0.3:
                    map[i][j] = [" ", "b"]  # .
                elif -0.3 <= map[i][j] < -0.2:
                    map[i][j] = [" ", "b"]  # -
                elif -0.2 <= map[i][j] < -0.1:
                    map[i][j] = [" ", "b"]  # -
                elif -0.1 <= map[i][j] < 0:
                    map[i][j] = [" ", "b"]  # =
                elif 0 <= map[i][j] < 0.1:
                    map[i][j] = ["ˏ", "b"]  # +
                elif 0.1 <= map[i][j] < 0.2:
                    map[i][j] = [":", "b"]  # *
                elif 0.2 <= map[i][j] < 0.3:
                    map[i][j] = ["#", "b"]  # #
                elif 0.3 <= map[i][j] < 0.4:
                    map[i][j] = [" ", "b"]  # %
                elif 0.4 <= map[i][j] < 0.5:
                    map[i][j] = [" ", "b"]  # @
                elif map[i][j] > 0.5:
                    map[i][j] = [" ", "b"]  # @


        os.system("")
        for i in range(len(map)):
           for j in range(len(map[i]) - 1):
               match map[i][j][0]:
                   case ".":
                       game_pad.addstr(i, j, f"{map[i][j][0]}", curses.A_DIM)
                   case ":":
                       game_pad.addstr(i, j, f"{map[i][j][0]}")
                   case "#":
                       game_pad.addstr(i, j, f"{map[i][j][0]}", curses.A_PROTECT)
                   case _:
                       game_pad.addstr(i, j, f"{map[i][j][0]}")

        # Item Generation
        with open('Items.json', 'r') as f:
            item_list = json.load(f)

        items_world = []
        id_counter = 0

        for i in range(len(map)):
            for j in range(len(map[i]) - 1):
                if map[i][j][1] == "b":
                    if map[i][j][0] == " " or map[i][j][0] == "." or map[i][j][0] == ":" or map[i][j][0] == "W":
                        if random.randrange(0, 5000) < 1:
                            match random.randrange(0, 3):
                                # Weapon creation
                                case 0:
                                    # print(f"#{i + 1} - Weapon\n")
                                    weapon_arr = [item for item in item_list["weapons"][
                                        random.randrange(len(item_list["weapons"]))].values()]
                                    items_world.append(
                                        Weapon(id_counter, map, game_pad, i, j, weapon_arr[0], weapon_arr[1], weapon_arr[2],
                                               weapon_arr[3], weapon_arr[4], weapon_arr[5], weapon_arr[6], weapon_arr[7],
                                               weapon_arr[8], weapon_arr[9], weapon_arr[10], weapon_arr[11], weapon_arr[12], weapon_arr[13]))

                                # Armor creation
                                case 1:
                                    # print(f"#{i + 1} - Armor\n")
                                    armor_arr = [item for item in
                                                 item_list["armor"][random.randrange(len(item_list["armor"]))].values()]
                                    items_world.append(
                                        Armor(id_counter, map, game_pad, i, j, armor_arr[0], armor_arr[1], armor_arr[2],
                                              armor_arr[3], armor_arr[4], armor_arr[5], armor_arr[6], armor_arr[7], armor_arr[8],
                                              armor_arr[9], armor_arr[10], armor_arr[11], armor_arr[12], armor_arr[13]))

                                # Food creation
                                case 2:
                                    # print(f"#{i + 1} - Food\n")
                                    food_arr = [item for item in
                                                item_list["food"][random.randrange(len(item_list["food"]))].values()]
                                    items_world.append(
                                        Food(id_counter, map, game_pad, i, j, food_arr[0], food_arr[1], food_arr[2], food_arr[3],
                                             food_arr[4]))
                            id_counter += 1

        stdscr.addstr(rows // 2 + 1, (cols // 2) - 9, "still debuging...")
        
        stdscr.move(rows // 2 + 1, (cols // 2) - 9)
        stdscr.clrtoeol()
        stdscr.move(rows // 2, (cols // 2) - 9)
        stdscr.clrtoeol()
        

        stdscr.refresh()

        stdscr.nodelay(True)

        # player setup
        #player_name = "Player"
        #player_role = "Warrior"  # Warrior, Hunter, Assassin
        player_lvl = 1
        #player_stamina = 20
        #player_intelligence = 1
        #player_strength = 5
        #player_dexterity = 1
        #player_defense = 5
        #player_luck = 5
        player_carry = 20

        p = Player(GAME_X // 2, GAME_Y // 2, player_name, player_race, player_role, player_lvl, stats_sum[3], stats_sum[1], stats_sum[0], stats_sum[2], stats_sum[4], stats_sum[5], player_carry, game_pad, map)

        # inventory setup
        inv = Window("inv", 0, cols-46, 25, 46, "Inventory")
        inv.print_inv(p)

        # stats setup
        stats = Window("stats", 25, cols-46, 12, 46, "Stats", p)
        # stats.create_window()

        # outline
        stdscr.hline(0, 1, '-', cols-47) #  9472
        stdscr.vline(1, 0, '|', rows-16)
        stdscr.addstr(0, 0, '+')

        # info-menu setup
        infomenu = Window("info", rows-15, 0, 15, cols-46, "")

        stats.print_stats(p)

        # setting up global variables for game loops
        in_game_bool = True
        description_bool = False
        item_deletion_bool = False
        quantity_bool = False

        def redraw_hud():
            stdscr.hline(0, 1, '-', cols-47) #  9472
            stdscr.vline(1, 0, '|', rows-16)
            stdscr.addstr(0, 0, '+')
            stdscr.refresh
            infomenu.redraw()
            stats.redraw()
            inv.redraw()

        def return_item_letter():
            for index, item in enumerate(p.inv_lst, start=1):
                if index == inv.highlight:
                    return inv.ABC[index - 1]

        def equip(item):
            infomenu.print_info(f"You successfully equiped {p.inv_lst[inv.highlight - 1][0].name}")
            item.equip_item(p)

        def unequip(item):
            infomenu.print_info(f"You successfully unequiped {p.inv_lst[inv.highlight - 1][0].name}")
            item.unequip_item()
        
        def use(food):
            if p.hp != p.maxhp:
                if food[1] > 1:
                    food[1] -= 1
                    
                    infomenu.print_info(f"You have healed {food[0].eat_food(p)} HP.")

                elif food[1] == 1:
                    infomenu.print_info(f"You have healed {food[0].eat_food(p)} HP.")
                    index = p.inv_lst.index(food)
                    del p.inv_lst[index]

            else:
                infomenu.print_info(f"You can't eat right now, you're in good condition!")


        def print_equip_infomenu():
            infomenu.clear_window()
            infomenu.delete_info()
            infomenu.print_info(f"[Up / Down] - Select | [z] - Confirm | [c] - Cancel", False)
            for _ in range(11):
                infomenu.print_info(f"", False)
            infomenu.print_info(
                f"Choose to equip/use: {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}",
                False)

        def print_description_infomenu():
            infomenu.clear_window()
            infomenu.delete_info()
            infomenu.print_info(f"[Up / Down] - Select | [z] - Confirm | [c] - Cancel", False)
            for _ in range(11):
                infomenu.print_info(f"", False)
            infomenu.print_info(
                f"Choose to describe: {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}",
                False)

        def print_deletion_infomenu():
            infomenu.clear_window()
            infomenu.delete_info()
            infomenu.print_info(f"[Up / Down] - Select | [z] - Confirm | [c] - Cancel", False)
            for _ in range(11):
                infomenu.print_info(f"", False)
            infomenu.print_info(f"Delete: {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}?", False)

        def print_deletion_infomenu_confirmation():
            infomenu.clear_window()
            infomenu.delete_info()
            infomenu.print_info(f"[y] - Yes | [n] - No", False)
            for _ in range(11):
                infomenu.print_info(f"", False)
            infomenu.print_info(
                f"Are you sure, you want to delete {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}?",
                False)

        def print_deletion_infomenu_quantity():
            infomenu.clear_window()
            infomenu.delete_info()
            infomenu.print_info("[Up / Down] - Increment / Decrement | [z] - Confirm | [c] - Cancel", False)
            for _ in range(11):
                infomenu.print_info("", False)
            infomenu.print_info(
                f"Quantity of {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}: {inv.quantity_index}x",
                False)

        def item_deletion_quantity():
            infomenu.delete_info()
            print_deletion_infomenu_quantity()
            quantity_bool = True
            inv.item_quantity_load(p)

            while quantity_bool:

                key = stdscr.getch()
                match key:
                    case curses.KEY_UP | curses.KEY_Right:
                        if inv.quantity_index >= inv.max_quantity:
                            inv.quantity_index = inv.min_quantity
                        else:
                            inv.quantity_index += 1
                        print_deletion_infomenu_quantity()

                    case curses.KEY_DOWN | curses.KEY_RIGHT:
                        if inv.quantity_index <= inv.min_quantity:
                            inv.quantity_index = inv.max_quantity
                        else:
                            inv.quantity_index -= 1
                        print_deletion_infomenu_quantity()

                    case 122: #  z
                        quantity_bool = False
                        item_deletion_bool = False

                        item_deletion_confirmation()
                        return True

                    case 99: #  c
                        quantity_bool = False
                        inv.print_inv(p)
                        infomenu.clear_window()
                        infomenu.restore_info()
                        infomenu.clear_buffer()
                        # break
                    
                    case curses.KEY_RESIZE:
                        infomenu.redraw()
                        stats.redraw()
                        inv.redraw()


        def item_deletion_confirmation():
            infomenu.delete_info()
            print_deletion_infomenu_confirmation()
            del_confirmation = True

            while del_confirmation:

                key = stdscr.getch()
                match key:
                    case 121: #  y
                        infomenu.clear_window()
                        infomenu.restore_info()
                        infomenu.clear_buffer()
                        infomenu.print_info(f"You successfully deleted {p.inv_lst[inv.highlight - 1][0].name}")

                        if p.inv_lst[inv.highlight - 1][1] > inv.quantity_index:
                            p.inv_lst[inv.highlight - 1][1] -= inv.quantity_index
                        else:
                            del p.inv_lst[inv.highlight - 1]
                        del_confirmation = False
                        inv.print_inv(p)
                        return True
                    case 110: #  n
                        del_confirmation = False
                        inv.print_inv(p)
                        print_deletion_infomenu()
                        return False
                    
                    case curses.KEY_RESIZE:
                        infomenu.redraw()
                        stats.redraw()
                        inv.redraw()


        def description():
            describing = True
            inv.highlight = 1

            infomenu.fill_buffer()

            print_description_infomenu()

            inv.print_inv(p, describing)
            while describing:


                key = stdscr.getch()

                match key:
                    case curses.KEY_UP | curses.KEY_LEFT:
                        if inv.highlight <= 1:
                            inv.highlight = len(p.inv_lst)
                        else:
                            inv.highlight -= 1
                        inv.print_inv(p, describing)
                        print_description_infomenu()

                    case curses.KEY_DOWN | curses.KEY_RIGHT:
                        if inv.highlight >= len(p.inv_lst):
                            inv.highlight = 1
                        else:
                            inv.highlight += 1
                        inv.print_inv(p, describing)
                        print_description_infomenu()

                    case 122: #  z
                        describing = False
                        infomenu.restore_info()
                        infomenu.clear_buffer()
                        line = '-'.ljust(infomenu.width-5, '-')

                        if infomenu.info_array[
                            0] != line.ljust(infomenu.width-2):
                            infomenu.print_info(line)
                        match p.inv_lst[inv.highlight - 1][
                            0].__class__.__name__:  # getting class name of the object
                            case "Armor":
                                infomenu.print_info(f'„{p.inv_lst[inv.highlight - 1][0].desc}“')
                                infomenu.print_info(f'DEF: {p.inv_lst[inv.highlight - 1][0].defense}')
                                infomenu.print_info(f'Dedicated for: {p.inv_lst[inv.highlight - 1][0].classes}')
                                infomenu.print_info(
                                    f'{p.inv_lst[inv.highlight - 1][0].name} [{p.inv_lst[inv.highlight-1][0].id}] ({p.inv_lst[inv.highlight - 1][0].lvl})')
                                infomenu.print_info(line)
                                inv.print_inv(p)
                            case "Weapon":
                                infomenu.print_info(f'„{p.inv_lst[inv.highlight - 1][0].desc}“')
                                infomenu.print_info(f'Dmg: {p.inv_lst[inv.highlight - 1][0].dmg}')
                                infomenu.print_info(f'Dedicated for: {p.inv_lst[inv.highlight - 1][0].classes}')
                                infomenu.print_info(
                                    f'{p.inv_lst[inv.highlight - 1][0].name} ({p.inv_lst[inv.highlight - 1][0].lvl})')
                                infomenu.print_info(line)
                                inv.print_inv(p)
                            case "Food":
                                infomenu.print_info(f'„{p.inv_lst[inv.highlight - 1][0].desc}“')
                                infomenu.print_info(f'Reg: {p.inv_lst[inv.highlight - 1][0].reg}')
                                infomenu.print_info(f'{p.inv_lst[inv.highlight - 1][0].name}')
                                infomenu.print_info(line)
                                inv.print_inv(p)
                            
                        inv.print_inv(p)

                    case 99: #  c
                        describing = False
                        inv.print_inv(p)
                        infomenu.clear_window()
                        infomenu.restore_info()
                        infomenu.clear_buffer()
                        # break
                    
                    case curses.KEY_RESIZE:
                        infomenu.redraw()
                        stats.redraw()
                        inv.redraw()


        def item_deletion():
            item_deletion = True

            inv.highlight = 1

            infomenu.fill_buffer()

            print_deletion_infomenu()

            inv.print_inv(p, item_deletion)
            while item_deletion:


                key = stdscr.getch()

                match key:
                    case curses.KEY_UP | curses.KEY_LEFT:
                        if inv.highlight <= 1:
                            inv.highlight = len(p.inv_lst)
                        else:
                            inv.highlight -= 1
                        inv.print_inv(p, item_deletion)
                        print_deletion_infomenu()

                    case curses.KEY_DOWN | curses.KEY_RIGHT:
                        if inv.highlight >= len(p.inv_lst):
                            inv.highlight = 1
                        else:
                            inv.highlight += 1
                        inv.print_inv(p, item_deletion)
                        print_deletion_infomenu()

                    case 122: #  y
                        if p.inv_lst[inv.highlight - 1][1] == 1:
                            if item_deletion_confirmation():
                                item_deletion = False
                        else:
                            if item_deletion_quantity():
                                item_deletion = False

                    case 99: #  c
                        item_deletion = False
                        inv.print_inv(p)
                        infomenu.clear_window()
                        infomenu.restore_info()
                        infomenu.clear_buffer()
                        break
                        
                    case curses.KEY_RESIZE:
                        infomenu.redraw()
                        stats.redraw()
                        inv.redraw()


        def equip_item():
            item_equip = True

            inv.highlight = 1

            infomenu.fill_buffer()

            print_equip_infomenu()

            inv.print_inv(p, item_equip)
            while item_equip:


                key = stdscr.getch()

                match key:
                    case curses.KEY_UP | curses.KEY_LEFT:
                        if inv.highlight <= 1:
                            inv.highlight = len(p.inv_lst)
                        else:
                            inv.highlight -= 1
                        inv.print_inv(p, item_equip)
                        print_equip_infomenu()

                    case curses.KEY_DOWN | curses.KEY_RIGHT:
                        if inv.highlight >= len(p.inv_lst):
                            inv.highlight = 1
                        else:
                            inv.highlight += 1
                        inv.print_inv(p, item_equip)
                        print_equip_infomenu()

                    case 122: #  z
                        item_equip = False
                        item = p.inv_lst[inv.highlight - 1][0]
                        food = p.inv_lst[inv.highlight - 1]

                        infomenu.clear_window()
                        infomenu.restore_info()
                        infomenu.clear_buffer()

                        if item.__class__.__name__ == "Weapon" or item.__class__.__name__ == "Armor":
                            # infomenu.print_info(f"a1")
                            if not item.is_equiped: #  if not equiped
                                # infomenu.print_info(f"a2")
                                if item.is_item_in_wear(p): #  is in p.wear_lst
                                    # infomenu.print_info(f"a3")
                                    for list_item in p.wear_lst:
                                        if list_item.wear == item.wear:
                                            # infomenu.print_info(f"a4")
                                            list_item.unequip_item()
                                            p.unwear_item(list_item)                                    

                                match item.equip_item(p):
                                    case "class":
                                        infomenu.print_info(f"Item isn't suited for you!")
                                    case "lvl":
                                        infomenu.print_info(f"You can't equip item with higher lvl than you!")
                                    case True:
                                        # infomenu.print_info(f"a5.1")
                                        p.wear_item(item)
                                        # infomenu.print_info(f"a5.2")
                                        infomenu.print_info(f"You successfully equiped {p.inv_lst[inv.highlight - 1][0].name}")
                                        # infomenu.print_info(f"a5.3")
                                        p.calculate_stats()
                                        # infomenu.print_info(f"a5.4")
                                        inv.print_inv(p)
                                        # infomenu.print_info(f"a5.5")

                            else:  # if True
                                # infomenu.print_info(f"b1")
                                unequip(item)
                                p.unwear_item(item)
                                #infomenu.print_info(f"You successfully unequiped {p.inv_lst[inv.highlight - 1][0].name}")
                                p.calculate_stats()
                                #inv.print_inv(p)
                        else:
                            # infomenu.print_info(f"c1")
                            # infomenu.print_info(f"{food}")
                            use(food)


                        # infomenu.print_info(f"end")
                        inv.print_inv(p)
                        stats.print_stats(p)
                        break

                    case 99: #  c
                        item_equip = False
                        inv.print_inv(p)
                        infomenu.clear_window()
                        infomenu.restore_info()
                        infomenu.clear_buffer()
                        break

                    case curses.KEY_RESIZE:
                        infomenu.redraw()
                        stats.redraw()
                        inv.redraw()


        def panel_menu():
            global game_menu_bool
            global in_game_bool
            global main_loop
            global char_naming
            global char_race
            global char_role
            global char_confirm
            global hrows, hcols


            #stdscr.erase()
            #game_pad.erase()

            panel_menu = Menu(10, 21, (rows//2)-5, (cols//2)-10)
            panel_menu.win.border()
            panel_menu.print_menu_adv()
            panel_menu.highlight = 1

            panel_child = curses.panel.new_panel(panel_menu.win)
            panel_child.top()

            panel_menu.win.refresh()
            panel_menu.print_menu_adv()
            panel_menu.win.refresh()

            game_menu_bool = True
            while game_menu_bool:

                key = stdscr.getch()
                match key:
                    case 99: #  c
                        game_menu_bool = False
                        redraw_hud()
                        #game_pad.refresh()

                    case 122: #  z
                        match panel_menu.highlight:
                            case 1:
                                pass # TODO: add game saving

                            case 2:
                                pass # TODO: add Guide

                            case 3:
                                game_menu_bool = False
                                in_game_bool = False
                                main_loop = False
                                char_naming = False
                                char_race = False
                                char_role = False
                                char_confirm = False

                    case curses.KEY_UP:
                        if panel_menu.highlight <= 1:
                            panel_menu.highlight = 3
                        else:
                            panel_menu.highlight -= 1
                        panel_menu.print_menu_adv()
                        panel_menu.win.refresh()

                    case curses.KEY_DOWN:
                        if panel_menu.highlight >= 3:
                            panel_menu.highlight = 1
                        else:
                            panel_menu.highlight += 1
                        panel_menu.print_menu_adv()
                        panel_menu.win.refresh()
                    
                    case curses.KEY_RESIZE:
                        game_menu_bool = False
                        infomenu.redraw()
                        stats.redraw()
                        inv.redraw()
                        #game_pad.refresh()
                        # panel_menu.win.redraw()

        def game_over_fce():
            global in_game_bool
            global char_naming
            global char_race
            global char_role
            global char_confirm
            global game_over

            game_over = True
            while game_over:
                hud.game_over(stdscr, p, rows, cols)

                key = stdscr.getch()
                if key != -1:
                    in_game_bool = False
                    char_naming = False
                    char_race = False
                    char_role = False
                    char_confirm = False
                    game_over = False

        # game loop variables
        # in_game_bool = True
        # description = False
        # item_deletion = False

        while in_game_bool:
            if p.hp <= 0:
               game_over_fce()
            
            
            key = stdscr.getch()

            match key:
                #  ---------------------------- MOVEMENT ---------------------------------------------------

                case curses.KEY_LEFT:
                    move_cam = p.move_left(map)
                    if not p.can_left(map):
                        infomenu.print_info("*You hit the wall*")
                    # Debuging:
                    else:
                        pass
                        # infomenu.print_info("*You moved left*")
                        # end
                    if not p.x >= GAME_X - (CAM_WIDTH // 2) - 1 and CAM_X > 0 and move_cam:
                        CAM_X -= 1

                case curses.KEY_RIGHT:
                    move_cam = p.move_right(map, GAME_X)
                    if not p.can_right(map, GAME_X):
                        infomenu.print_info(f"*You hit the wall*")
                    # Debuging:
                    else:
                        pass
                        # infomenu.print_info(f"*You moved right*")
                        # end
                    if p.x > CAM_WIDTH // 2 and move_cam and CAM_X <= GAME_X - CAM_WIDTH - 2:
                        CAM_X += 1

                case curses.KEY_UP:
                    move_cam = p.move_up(map)
                    if not p.can_up(map):
                        infomenu.print_info(f"*You hit the wall*")
                    # Debuging:
                    else:

                #game_pad.refresh(CAM_Y, CAM_X, 1, 1, CAM_HEIGHT, CAM_WIDTH)
                        pass
                        # infomenu.print_info(f"*You moved up*")
                        # end
                    if not p.y >= GAME_Y - (CAM_HEIGHT // 2) - 1 and CAM_Y > 0 and move_cam:
                        CAM_Y -= 1

                case curses.KEY_DOWN:
                    move_cam = p.move_down(map, GAME_Y)
                    if not p.can_down(map, GAME_Y):
                        infomenu.print_info(f"*You hit the wall*")
                    # Debuging:
                    else:
                        pass
                        # infomenu.print_info(f"*You moved down*")
                    # end
                    if p.y > CAM_HEIGHT // 2 and move_cam and CAM_Y <= GAME_Y - CAM_HEIGHT - 2:
                        CAM_Y += 1

                #  ---------------------------- ACTION ------------------------------------------------------

                case 103: #  g
                    match p.pickup_item(map, items_world, 0, 0):
                        case "yes":
                            inv.print_inv(p)
                            infomenu.print_info(f"You picked up {p.inv_lst[0][0].name}")
                        case "overcarried":
                            infomenu.print_info(f"You're overloaded!")
                        case "no_item":
                            infomenu.print_info(f"There is no item under you!")
                        case "working":
                            infomenu.print_info(f"Working!!")
                        case "error":
                            infomenu.print_info(f"Error!!")

                case 105: #  i
                    if len(p.inv_lst) > 0:

                        description()
                    else:
                        infomenu.print_info(f"You have no items to describe!")

                case 100: #  d
                    if len(p.inv_lst) > 0:

                        item_deletion()
                    else:
                        infomenu.print_info(f"You have no items to delete!")
                
                case 101: #  e
                    if len(p.inv_lst) > 0:
                        
                        equip_item()

                    else:
                        infomenu.print_info(f"You have no items to equip!")
                
                case 114: #  r
                    p.hp -= 1
                    stats.print_stats(p)

                #  ---------------------------- SPECIAL -----------------------------------------------------

                case 113: #  q
                    panel_menu()
                    
                # case 111: #  o
                    # infomenu.print_info(len(infomenu.info_array))

                case 102: #  f
                    enemy_stats = create_enemy(p.entity_lvl, True)
                    e = Enemy(enemy_stats['name'], enemy_stats['class'], enemy_stats['lvl'],
                            enemy_stats['dmg'], enemy_stats['sta'], enemy_stats['int'],
                            enemy_stats['str'], enemy_stats['dex'], enemy_stats['def'],
                            enemy_stats['luc'], game_pad, map)

                    result = fight.fight(stdscr, rows, cols, p, e)

                    if not result:  # When GameOver                      
                        game_over_fce()

                    else:  # When Won
                        stdscr.erase()
                        stdscr.refresh()
                        stats.print_stats(p)
                        redraw_hud()
                    
                    del e
                
                case curses.KEY_RESIZE:
                    rows, cols = stdscr.getmaxyx()
                    hrows = (rows // 2)
                    hcols = (cols // 2)
                    curses.resize_term(rows, cols)
                    
                    redraw_hud()


                case _:
                #    infomenu.print_info(f"{key}")
                    pass

            game_pad.refresh(CAM_Y, CAM_X, 1, 1, CAM_HEIGHT, CAM_WIDTH)
                    

    
    def character_creation_confirm():
        global stats_sum
        global char_confirm
        
        stdscr.erase()
        
        #Setting up label
        label = "Is this you?"
        stdscr.addstr(hrows - 8, hcols - (len(label) // 2), label)
        stdscr.refresh()

        #Menu setting
        conf_win = Window("menu_stats", hrows-6, hcols-22, 14, 44, f"{player_name}")
        conf_win.win.border()

        #Stats
        conf_win.win.addstr(1, 2, f"Name: {player_name}")
        conf_win.win.addstr(2, 2, f"Race: {player_race}")
        conf_win.win.addstr(3, 2, f"Class: {player_role}")

        conf_win.win.addstr(1, 25, "Race")
        conf_win.win.addstr(1, 30, "Role")
        conf_win.win.addstr(1, 35, "Base")
        conf_win.print_stats_label(2, 22)
        conf_win.print_race_stats(2, 27, race_highlight, race_values)
        conf_win.print_role_stats(2, 32, role_highlight, role_values)
        
        
        stats_sum = conf_win.stats_sum(race_values, role_values, race_highlight, role_highlight)
        conf_win.print_summer_stats(2, 37, stats_sum)

        conf_win.win.refresh()
        #conf_win.win.addstr(f"Name: {}")


        char_confirm = True
        while char_confirm:

            key = stdscr.getch()

            match key:
                case 122: #  z
                    game(player_name, player_race, player_role, stats_sum)

                case 99: #  c
                    character_race_scene()
                    stdscr.erase()
                    stdscr.refresh()
                    char_confirm = False
            
            #stats_menu.print_stats_label("STR", "INT", "DEX", "STA", "DEF", "LUC",)


    
    def character_role_scene(stats_menu):
        global char_role
        global role_highlight
        global player_role
        global role_values
        
        # Load from Roles.json
        with open('roles.json', 'r') as f:
            roles_json = json.load(f)

        # creating lists for races
        roles_instances = []
        roles_names = []

        # filling lists with race data
        for item in roles_json['roles']:
            roles_instances.append(Role(item['name'], item['stamina'], item['strength'], item['dexterity'], item['intelligence'], item['defense'], item['luck']))
            roles_names.append(item['name'])

        # Setting up label
        label = "What is your profession?"
        stdscr.addstr(hrows - 8, hcols - (len(label) // 2), label)
        stdscr.refresh()

        # Menu setting
        role_select = Menu(7, 11, hrows+1, hcols-15-5)
        role_select.win.border()
        #stats_menu = Window("menu_stats", hrows-13, hcols+4, 14, 22, "Character stats")
        #stats_menu.win.border

        # Filling the global role_highlight variable
        role_highlight = role_select.highlight

        # adding labels into menu
        role_select.add_menu_label(*roles_names)

        # printing select on the screen
        role_select.print_menu(1, 1, 0, 1)
        role_select.win.refresh()
        stats_menu.print_role_stats(2, 10, role_highlight, roles_instances)

        char_role = True
        while char_role:

            key = stdscr.getch()

            match key:
                case 122: #  z
                    
                    role_highlight = role_select.highlight
                    
                    player_role = roles_names[role_highlight]
                    
                    role_values = roles_instances
                    character_creation_confirm()

                    #game(player_name, player_race, player_role)

                case 99: #  c
                    role_select.win.clear()
                    role_select.win.refresh()
                    del role_select
                    stats_menu.del_stats_values(2, 10)
                    stdscr.refresh()
                    char_role = False
                case curses.KEY_UP:
                    if role_select.highlight <= 0:
                        role_select.highlight = len(role_select.menu_arr)-1
                    else:
                        role_select.highlight -= 1
                    role_select.print_menu(1, 1, 0, 1)
                    role_select.win.refresh()
                    stats_menu.print_role_stats(2, 10, role_select.highlight, roles_instances)

                case curses.KEY_DOWN:
                    if role_select.highlight >= len(role_select.menu_arr)-1:
                        role_select.highlight = 0
                    else:
                        role_select.highlight += 1
                    role_select.print_menu(1, 1, 0, 1)
                    role_select.win.refresh()
                    stats_menu.print_role_stats(2, 10, role_select.highlight, roles_instances)
            
            #stats_menu.print_stats_label("STR", "INT", "DEX", "STA", "DEF", "LUC",)


        #game(player_name, player_race, "Warrior")

    def character_race_scene():
        global char_race
        global race_highlight
        global player_race
        global race_values

        # Clear window
        stdscr.erase()

        # Load from RRaces.json
        with open('races.json', 'r') as f:
            races_json = json.load(f)

        # creating lists for races
        races_instances = []
        races_names = []

        # filling lists with race data
        for item in races_json['races']:
            races_instances.append(Race(item['name'], item['stamina'], item['strength'], item['dexterity'], item['intelligence'], item['defense'], item['luck']))
            races_names.append(item['name'])

        stdscr.refresh()

        # Window creation for race select
        race_select = Menu(7, 11, hrows-6, hcols-15-5)
        race_select.win.border()
        stats_menu = Window("menu_stats", hrows-6, hcols-5+4, 14, 22, "Character stats")
        stats_menu.win.border()

        # Filling the global race_highlight variable
        race_highlight = race_select.highlight 

        # adding races to select
        race_select.add_menu_label(*races_names)

        # printing select on the screen
        race_select.print_menu(1, 1, 0, 1)
        race_select.win.refresh()
        stats_menu.clear_window()
        stats_menu.print_race_stats(2, 7, race_highlight, races_instances)
        stats_menu.print_stats_label(2, 2)



        char_race = True
        while char_race:

            stdscr.move(hrows - 8, 0)
            stdscr.clrtoeol()
            
            # Create character panels and making their borders
            label = "What race are you?"
            stdscr.addstr(hrows - 8, hcols - (len(label) // 2), label)
            stdscr.refresh()
            
            key = stdscr.getch()

            match key:
                case 122:
                    
                    race_highlight = race_select.highlight
                    player_race = races_names[race_highlight]
                    race_values = races_instances

                    character_role_scene(stats_menu)
                    continue
                
                case 99:
                    character_name_scene()

                case curses.KEY_UP:
                    if race_select.highlight <= 0:
                        race_select.highlight = len(race_select.menu_arr)-1
                    else:
                        race_select.highlight -= 1
                    race_select.print_menu(1, 1, 0, 1)
                    race_select.win.refresh()
                    stats_menu.print_race_stats(2, 7, race_select.highlight, races_instances)
                    stats_menu.print_stats_label(2, 2)

                case curses.KEY_DOWN:
                    if race_select.highlight >= len(race_select.menu_arr)-1:
                        race_select.highlight = 0
                    else:
                        race_select.highlight += 1
                    race_select.print_menu(1, 1, 0, 1)
                    race_select.win.refresh()
                    stats_menu.print_race_stats(2, 7, race_select.highlight, races_instances)
                    stats_menu.print_stats_label(2, 2)

    def character_name_scene():
        global char_naming
        global player_name

        # Clear window
        stdscr.erase()
        stdscr.refresh()
        # Create character panels and making their borders
        label = "What is your name, hero?"
        stdscr.addstr(hrows - 5, hcols - (len(label) // 2)+1, label)
        rectangle(stdscr, hrows - 3, hcols - 11, hrows - 1, hcols + 11)
        stdscr.refresh()
        name_prompt = Window("char", hrows - 2, hcols - 9, 1, 11, "")
        name_prompt.win.erase()

        query = curses.textpad.Textbox(name_prompt.win)
        query.stripspaces = True

        char_naming = True
        while char_naming:
            try:
                query.edit()
                gather = query.gather()
                alphanumeric_chars = [char for char in gather if char.isalnum()]
                reform_gather = ''.join(alphanumeric_chars)
                
                if reform_gather:
                    player_name = reform_gather.strip("123456789")
                    char_naming = False

            except:
                stdscr.addstr("neco je spatne")

        character_race_scene()

    def print_logo():
        f = open("logo.txt", "r")
        logo_y = rows // 2
        for i in range(8):
            stdscr.addstr(i+2, hcols - 23, f.readline())
        f.close()

    curses.init_pair(100, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(101, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(102, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(103, curses.COLOR_WHITE, curses.COLOR_GREEN)

    def createMenuBorder():
        rectangle(stdscr, 11, hcols - 25, 23, hcols + 25) #  hrows - 10 hrows + 2

    def createButton1(color):
        word = "New Game"
        stdscr.addstr(13, hcols - (len(word)//2), word) #  hrows - 8
        stdscr.attroff(curses.color_pair(101))

    def createButton2(color):
        word = "Load Game"
        stdscr.addstr(15, hcols - (len(word)//2), word) #  hrows - 6
        stdscr.attroff(curses.color_pair(101))
        #rectangle(stdscr, 24, 97, 27, 114)

    def createButton3(color):
        word = "Quit"
        stdscr.addstr(21, hcols - (len(word)//2) - 2, word) #  hrows - 0
        stdscr.attroff(curses.color_pair(101))
        #rectangle(stdscr, 32, 97, 35, 114)



    select = 0

    def colorPick():
        createMenuBorder()
        if select == 0:
            stdscr.attron(curses.color_pair(101))
            createButton1(101)
            createButton2(100)
            createButton3(100)
        elif select == 1:
            createButton1(100)
            stdscr.attron(curses.color_pair(101))
            createButton2(101)
            createButton3(100)
        elif select == 2:
            createButton1(100)
            createButton2(100)
            stdscr.attron(curses.color_pair(101))
            createButton3(101)

    main_loop = True
    while main_loop:

        stdscr.erase()
        print_logo()


        stdscr.addstr(rows - 2, cols - 14, f"X = Exit")
        stdscr.addstr(rows - 2, cols - 27, f"Z = Select")
        colorPick()

        key = stdscr.getch()

        match key:
            case curses.KEY_UP:
                if select < 1:
                    select = 2
                    colorPick()
                    stdscr.refresh()
                else:
                    select -= 1
                    colorPick()
                    stdscr.refresh()

            case curses.KEY_DOWN:
                if select > 1:
                    select = 0
                    colorPick()
                    stdscr.refresh()
                else:
                    select += 1
                    colorPick()
                    stdscr.refresh()
            
            case 122:
                if select == 0:
                    character_name_scene()
                elif select == 2:
                    in_game_bool = False
                    main_loop = False
            
            case 119:
                main_loop = False

            case curses.KEY_RESIZE:
                rows, cols = stdscr.getmaxyx()
                hrows = (rows // 2)
                hcols = (cols // 2)
                curses.resize_term(rows, cols)


                continue

if __name__ == '__main__':
    try:
        wrapper(main)
    except curses.error:
        time.sleep(1)
        os.system('cls')
        print("\n WARNING: The game has crashed, probably due to small window resolution!")
        print("          Resize the terminal and try again. \n")
        wrapper(main)
