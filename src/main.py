import os
import curses
import random
import json
import logging
import math
import time

from curses import wrapper
from curses.textpad import Textbox, rectangle
from perlin_noise import PerlinNoise

from player import Player
from hud import Window, Menu
from camera import Camera
from items import Weapon, Armor, Food
from tile import Tile


def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    hrows = (rows // 2)
    hcols = (cols // 2)

    stdscr.clear()
    curses.curs_set(False)

    global player_name
    global player_race
    global player_class

    def game(player_name, player_race, player_class):
        stdscr.clear()
        LOADING_LABEL = "Generating terrain..."
        stdscr.addstr(rows // 2, (cols // 2) - 9, LOADING_LABEL)
        stdscr.refresh()

        CAM_WIDTH = 161
        CAM_HEIGHT = 35
        GAME_X = 600 + 1
        GAME_Y = 600
        CAM_X = GAME_X // 2 - CAM_WIDTH // 2
        CAM_Y = GAME_Y // 2 - CAM_HEIGHT // 2

        cam = Camera(CAM_WIDTH, CAM_HEIGHT, CAM_X, CAM_Y)

        OCTAVE = 26  # random.randrange(25, 30)

        noise = PerlinNoise(octaves=OCTAVE, seed=random.randrange(0, 100000000))  # random.randrange(0, 100000)

        map = [[noise([i / (GAME_X * 0.2), j / (GAME_Y * 1.7)]) for j in range(GAME_X)] for i in range(GAME_Y)]

        # curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
        # BLUE_AND_YELLOW = curses.color_pair(1)

        game_pad = curses.newpad(GAME_Y, GAME_X)
        # player_win = curses.newwin(CAM_HEIGHT, CAM_WIDTH, 1, 0)
        stdscr.refresh()
        curses.curs_set(False)

        map = [[noise([i / GAME_X, j / GAME_Y]) for j in range(GAME_X)] for i in range(GAME_Y)]

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
                    case other:
                        game_pad.addstr(i, j, f"{map[i][j][0]}")

        # Item Generation
        with open('Items.json', 'r') as f:
            item_list = json.load(f)

        items_world = []
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
                                        Weapon(map, game_pad, i, j, weapon_arr[0], weapon_arr[1], weapon_arr[2],
                                               weapon_arr[3], weapon_arr[4]))

                                # Armor creation
                                case 1:
                                    # print(f"#{i + 1} - Armor\n")
                                    armor_arr = [item for item in
                                                 item_list["armor"][random.randrange(len(item_list["armor"]))].values()]
                                    items_world.append(
                                        Armor(map, game_pad, i, j, armor_arr[0], armor_arr[1], armor_arr[2],
                                              armor_arr[3], armor_arr[4], armor_arr[5]))

                                # Food creation
                                case 2:
                                    # print(f"#{i + 1} - Food\n")
                                    food_arr = [item for item in
                                                item_list["food"][random.randrange(len(item_list["food"]))].values()]
                                    items_world.append(
                                        Food(map, game_pad, i, j, food_arr[0], food_arr[1], food_arr[2], food_arr[3]))

        stdscr.nodelay(True)

        # player setup
        #player_name = "Player"
        player_class = "Warrior"  # Warrior, Hunter, Assassin
        p = Player(GAME_X // 2, GAME_Y // 2, player_name, player_race, player_class, 1, 100, 100, 5, 10, 52, 20, game_pad, map)

        # inventory setup
        inv = Window("inv", 1, 162, 25, 46, "Inventory")
        inv.print_inv(p)

        # stats setup
        stats = Window("stats", 26, 162, 11, 46, "Stats", p)
        # stats.create_window()

        # HLine under game window
        stdscr.hline(CAM_HEIGHT + 1, 75, 9472, (CAM_WIDTH // 2) + 7)

        # info-menu setup
        infomenu = Window("info", 36, 0, 15, 75, "")

        stats.print_stats(p)

        # setting up global variables for game loops
        in_game_bool = True
        description_bool = False
        item_deletion_bool = False
        quantity_bool = False

        def return_item_letter():
            for index, item in enumerate(p.inv_lst, start=1):
                if index == inv.highlight:
                    return inv.ABC[index - 1]

        def print_description_infomenu():
            infomenu.clear_window()
            infomenu.delete_info()
            infomenu.print_info(f"[Up / Down] - Select | [z] - Confirm | [c] - Cancel", False)
            for _ in range(11):
                infomenu.print_info(f"", False)
            infomenu.print_info(
                f"Choose for description: {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}",
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
            infomenu.print_info(f"[Up / Down] - Increment / Decrement | [z] - Confirm | [c] - Cancel", False)
            for _ in range(11):
                infomenu.print_info(f"", False)
            infomenu.print_info(
                f"Quantity of {return_item_letter()}) {p.inv_lst[inv.highlight - 1][0].name}: {inv.quantity_index}x",
                False)

        def item_deletion_quantity():
            infomenu.delete_info()
            print_deletion_infomenu_quantity()
            quantity_bool = True
            inv.item_quantity_load(p)

            while quantity_bool:
                try:
                    key = stdscr.getkey()
                    match key:
                        case "KEY_UP" | "KEY_Right":
                            if inv.quantity_index >= inv.max_quantity:
                                inv.quantity_index = inv.min_quantity
                            else:
                                inv.quantity_index += 1
                            print_deletion_infomenu_quantity()

                        case "KEY_DOWN" | "KEY_RIGHT":
                            if inv.quantity_index <= inv.min_quantity:
                                inv.quantity_index = inv.max_quantity
                            else:
                                inv.quantity_index -= 1
                            print_deletion_infomenu_quantity()

                        case "z":
                            quantity_bool = False
                            item_deletion_bool = False

                            item_deletion_confirmation()
                            return True

                        case "c":
                            quantity_bool = False
                            inv.print_inv(p)
                            infomenu.clear_window()
                            infomenu.restore_info()
                            infomenu.clear_buffer()
                            # break

                except:
                    pass

        def item_deletion_confirmation():
            infomenu.delete_info()
            print_deletion_infomenu_confirmation()
            del_confirmation = True

            while del_confirmation:
                try:
                    key = stdscr.getkey()
                    match key:
                        case "y":
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
                        case "n":
                            del_confirmation = False
                            inv.print_inv(p)
                            print_deletion_infomenu()
                            return False
                except:
                    pass

        def description():
            describing = True
            inv.highlight = 1

            infomenu.fill_buffer()

            print_description_infomenu()

            inv.print_inv(p, describing)
            while describing:
                try:

                    key = stdscr.getkey()

                    match key:
                        case "KEY_UP" | "KEY_LEFT":
                            if inv.highlight <= 1:
                                inv.highlight = len(p.inv_lst)
                            else:
                                inv.highlight -= 1
                            inv.print_inv(p, describing)
                            print_description_infomenu()

                        case "KEY_DOWN" | "KEY_RIGHT":
                            if inv.highlight >= len(p.inv_lst):
                                inv.highlight = 1
                            else:
                                inv.highlight += 1
                            inv.print_inv(p, describing)
                            print_description_infomenu()

                        case "z":
                            describing = False
                            infomenu.restore_info()
                            infomenu.clear_buffer()

                            if infomenu.info_array[
                                0] != '----------------------------------------------------------------------':
                                infomenu.print_info(
                                    f'----------------------------------------------------------------------')
                            match p.inv_lst[inv.highlight - 1][
                                0].__class__.__name__:  # getting class name of the object
                                case "Armor":
                                    infomenu.print_info(f'„{p.inv_lst[inv.highlight - 1][0].desc}“')
                                    infomenu.print_info(f'Def: {p.inv_lst[inv.highlight - 1][0].defense}')
                                    infomenu.print_info(
                                        f'{p.inv_lst[inv.highlight - 1][0].name} ({p.inv_lst[inv.highlight - 1][0].lvl})')
                                    infomenu.print_info(
                                        f'----------------------------------------------------------------------')
                                    inv.print_inv(p)
                                case "Weapon":
                                    infomenu.print_info(f'„{p.inv_lst[inv.highlight - 1][0].desc}“')
                                    infomenu.print_info(f'Dmg: {p.inv_lst[inv.highlight - 1][0].dmg}')
                                    infomenu.print_info(
                                        f'{p.inv_lst[inv.highlight - 1][0].name} ({p.inv_lst[inv.highlight - 1][0].lvl})')
                                    infomenu.print_info(
                                        f'----------------------------------------------------------------------')
                                    inv.print_inv(p)
                                case "Food":
                                    infomenu.print_info(f'„{p.inv_lst[inv.highlight - 1][0].desc}“')
                                    infomenu.print_info(f'Reg: {p.inv_lst[inv.highlight - 1][0].reg}')
                                    infomenu.print_info(f'{p.inv_lst[inv.highlight - 1][0].name}')
                                    infomenu.print_info(
                                        f'----------------------------------------------------------------------')
                                    inv.print_inv(p)

                        case "c":
                            describing = False
                            inv.print_inv(p)
                            infomenu.clear_window()
                            infomenu.restore_info()
                            infomenu.clear_buffer()
                            # break
                except:
                    pass

        def item_deletion():
            item_deletion = True

            inv.highlight = 1

            infomenu.fill_buffer()

            print_deletion_infomenu()

            inv.print_inv(p, item_deletion)
            while item_deletion:
                try:

                    key = stdscr.getkey()

                    match key:
                        case "KEY_UP" | "KEY_LEFT":
                            if inv.highlight <= 1:
                                inv.highlight = len(p.inv_lst)
                            else:
                                inv.highlight -= 1
                            inv.print_inv(p, item_deletion)
                            print_deletion_infomenu()

                        case "KEY_DOWN" | "KEY_RIGHT":
                            if inv.highlight >= len(p.inv_lst):
                                inv.highlight = 1
                            else:
                                inv.highlight += 1
                            inv.print_inv(p, item_deletion)
                            print_deletion_infomenu()

                        case "z":
                            if p.inv_lst[inv.highlight - 1][1] == 1:
                                if item_deletion_confirmation():
                                    item_deletion = False
                            else:
                                if item_deletion_quantity():
                                    item_deletion = False

                        case "c":
                            item_deletion = False
                            inv.print_inv(p)
                            infomenu.clear_window()
                            infomenu.restore_info()
                            infomenu.clear_buffer()
                            break

                except:
                    pass

        # game loop variables
        # in_game_bool = True
        # description = False
        # item_deletion = False

        while in_game_bool:
            try:
                key = stdscr.getkey()

                match key:
                    #  ---------------------------- MOVEMENT ---------------------------------------------------

                    case "KEY_LEFT":
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

                    case "KEY_RIGHT":
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

                    case "KEY_UP":
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

                    case "KEY_DOWN":
                        move_cam = p.move_down(map, GAME_Y)
                        if not p.can_down(map, GAME_Y):
                            infomenu.print_info(f"*You hit the wall*")
                        # Debuging:
                        else:
                            pass
                            # infomenu.print_info(f"*You moved down*")
                        # end
                        if p.y > CAM_HEIGHT // 2 and move_cam and CAM_Y <= GAME_Y - CAM_HEIGHT - 1:
                            CAM_Y += 1

                    #  ---------------------------- ACTION ------------------------------------------------------

                    case "g":
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

                    case "i":
                        if len(p.inv_lst) > 0:

                            description()
                        else:
                            infomenu.print_info(f"You have no items to describe!")

                    case "d":
                        if len(p.inv_lst) > 0:

                            item_deletion()
                        else:
                            infomenu.print_info(f"You have no items to delete!")

                    #  ---------------------------- SPECIAL -----------------------------------------------------

                    case "q":
                        in_game_bool = False
                        main_loop = False

                    case "o":
                        infomenu.print_info(len(infomenu.info_array))

                    case _:
                        infomenu.print_info(f"{key}")

            except:
                pass

            game_pad.refresh(CAM_Y, CAM_X, 1, 1, CAM_HEIGHT, CAM_WIDTH)

    player_name = ""
    player_race = ""

    def character_race_scene():
        # Clear window
        stdscr.clear()
        # Create character panels and making their borders
        label = "What race are you?"
        stdscr.addstr(hrows - 16, hcols - (len(label) // 2), label)
        # Window creation for race select
        race_select = Menu(10, 20, 5, 20)
        race_select.win.addstr("Hello")
        # adding races to select
        #race_select.add_menu_label("Human", "Elf", "Org")
        # printing select on the screen
        #race_select.print_menu(1, 1, 0, 0, 1)
        stdscr.refresh()



        char_race = True
        while char_race:
            try:
                key = stdscr.getkey()

                if key == "z":
                    game(player_name, "Human", "Warrior")

            except:
                pass




    def character_name_scene():
        # Clear window
        stdscr.clear()
        stdscr.refresh()
        # Create character panels and making their borders
        label = "What is your name, hero?"
        stdscr.addstr(hrows - 16, hcols - (len(label) // 2), label)
        rectangle(stdscr, hrows - 14, hcols - 11, hrows - 12, hcols + 11)
        stdscr.refresh()
        name_prompt = Window("char", hrows - 13, hcols - 9, 1, 20, "")
        name_prompt.win.clear()

        query = curses.textpad.Textbox(name_prompt.win)
        # character_win = Window("char", hrows-10, hcols-40, 20, 40, "Character")
        # character_img_win = Window("char_img", hrows-10, hcols + 20, 20, 40, "")
        # character_win.clear_window()
        # character_img_win.clear_window()

        char_naming = True
        while char_naming:
            try:
                query.edit()
                gather = query.gather()
                if gather != "":
                    player_name = gather
                    #char_naming = False
                    #game(player_name, "Goblin", "Warrior")
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
        rectangle(stdscr, hrows - 10, hcols - 25, hrows + 2, hcols + 25)

    def createButton1(color):
        word = "New Game"
        stdscr.addstr(hrows - 8, hcols - (len(word)//2), word)
        stdscr.attroff(curses.color_pair(101))

    def createButton2(color):
        word = "Load Game"
        stdscr.addstr(hrows - 6, hcols - (len(word)//2), word)
        stdscr.attroff(curses.color_pair(101))
        #rectangle(stdscr, 24, 97, 27, 114)

    def createButton3(color):
        word = "Quit"
        stdscr.addstr(hrows - 0, hcols - (len(word)//2) - 2, word)
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
        try:
            stdscr.clear()
            print_logo()


            stdscr.addstr(rows - 2, cols - 14, f"X = Exit")
            stdscr.addstr(rows - 2, cols - 27, f"Z = Select")
            colorPick()

            key = stdscr.getkey()

            if key == "KEY_UP":
                if select < 1:
                    select = 2
                    colorPick()
                    stdscr.refresh()
                else:
                    select -= 1
                    colorPick()
                    stdscr.refresh()
            elif key == "KEY_DOWN":
                if select > 1:
                    select = 0
                    colorPick()
                    stdscr.refresh()
                else:
                    select += 1
                    colorPick()
                    stdscr.refresh()
            elif key == "z" and select == 0:
                character_name_scene()

            elif key == "z" and select == 2:
                in_game_bool = False
                main_loop = False

            elif key == "x":
                main_loop = False

            elif key == "KEY_RESIZE":
                rows, cols = stdscr.getmaxyx()
                hrows = (rows // 2)
                hcols = (cols // 2)
                curses.resize_term(rows, cols)


                continue

        except:
            pass


if __name__ == '__main__':
    try:
        wrapper(main)
    except curses.error:
        pass
        # wrapper(main)
