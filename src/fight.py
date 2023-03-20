import curses
import math
import time
import json
import random
from enemy import Enemy, create_enemy
from hud import Window



def fight(stdscr, rows, cols, p, e):
    stdscr.erase()
    stdscr.refresh()
    hrows = rows // 2
    hcols = cols // 2
    
    #won = True  # False: Lost | True: Win

    p_y = 4
    e_y = 4

    player_win = Window("fight", p_y, 12, hrows-4, hcols-30, "")
    player_win.clear_window()

    #player_win.win.hline(player_win.height//2, 1, "-", player_win.width-2)
    player_win.win.refresh()

    enemy_win = Window("fight", e_y, hcols+18, hrows-4, hcols-30, "")
    enemy_win.clear_window()

    #enemy_win.win.hline(enemy_win.height//2 , 1, "-", player_win.width-2)
    enemy_win.win.refresh()

    # player = player_win.win
    # enemy = enemy_win.win

    def draw_hud(win, entity):
        hheight = win.height//2
        hwidth = win.width//2

        # Info
        win.win.addstr(2, hwidth - (len(entity.name)//2) - 2, f"< {entity.name} >")
        win.win.move(3, hwidth + 12)
        win.win.clrtoeol()
        
        win.win.addstr(3, hwidth + 12, f"{entity.hp}/{entity.maxhp}")
        win.win.addstr(4, 2, f"|{win.draw_hp_bar(entity)}|")

        win.win.hline((enemy_win.height//2)-1 , 1, "-", player_win.width-2)

        # Stats
        entity_class_label = entity.entity_class
        win.win.addstr(7, hwidth - (len(entity_class_label)//2), f"{entity_class_label}")
        
        win.win.addstr(9, hwidth-8, f"STR: {entity.sum_strength}")
        win.win.addstr(11, hwidth-8, f"DEX: {entity.sum_dexterity}")
        win.win.addstr(13, hwidth-8, f"INT: {entity.sum_intelligence}")

        win.win.addstr(9, (hwidth+8)-7, f"STA: {entity.sum_stamina}")
        win.win.addstr(11, (hwidth+8)-7, f"DEF: {entity.sum_defense}")
        win.win.addstr(13, (hwidth+8)-7, f"LUK: {entity.sum_luck}")

        win.win.border()
        win.win.refresh()


    def redraw_battle():
        player_win.win.redrawwin()
        draw_hud(player_win, p)
        enemy_win.win.redrawwin()
        draw_hud(enemy_win, e)
        player_win.win.refresh()
        enemy_win.win.refresh()

    def move_animation(win, y, x, delay):
        win.current_x = x
        win.current_y = y 
        
        win.win.mvwin(y, x)
        
        stdscr.erase()
        stdscr.refresh()
        redraw_battle()

        win.win.refresh()
        time.sleep(delay)

    # def attack_animation(win, y, x, delay):
    #     player_win.win.mvwin(y, x)

    #     stdscr.erase()
    #     stdscr.refresh()
    #     redraw_battle()

    #     win.refresh()
    #     time.sleep(delay)
    

    def player_attack_animation(dmg=False): # player = player_win.win
        time.sleep(0.5)

        move_animation(player_win, p_y, 7+10, 0.05)
        move_animation(player_win, p_y, 35+10, 0.05)
        move_animation(player_win, p_y, 34+10, 0.1)

        # move_animation(player_win, p_y, player_win.current_x+8, 0.05)
        # move_animation(player_win, p_y, player_win.current_x+28, 0.05)
        # move_animation(player_win, p_y, player_win.current_x-4, 0.1)


    def player_attack_recall_animation():
        
        move_animation(player_win, p_y, 10+10, 0.1)
        move_animation(player_win, p_y, 6+10, 0.1)
        move_animation(player_win, p_y, player_win.x, 0.1)
        # move_animation(player_win.win, p_y, player_win.x, 0.1)

        # move_animation(player_win, p_y, player_win.current_x-10, 0.1)
        # move_animation(player_win, p_y, player_win.current_x-8, 0.1)
        # move_animation(player_win, p_y, player_win.x, 0.1)

    def enemy_attack_animation(dmg=False):
        # enemy = enemy_win.win
        
        time.sleep(0.5)

        move_animation(enemy_win, e_y, enemy_win.x-7, 0.05)
        move_animation(enemy_win, e_y, enemy_win.x-35, 0.05)
        move_animation(enemy_win, e_y, enemy_win.x-33, 0.1)
        

    def enemy_attack_recall_animation():

        move_animation(enemy_win, e_y, enemy_win.x-10, 0.1)
        move_animation(enemy_win, e_y, enemy_win.x-6, 0.1)
        move_animation(enemy_win, e_y, enemy_win.x, 0.1)
        # move_animation(enemy, e_y, enemy_win.x-0, 0.1)

    def take_dmg_animation(win, critical_hit=False):
        # entity = entity.win

        # if critical_hit:
        #     win.attron(curses.A_REVERSE)
        #     win.refresh()
        move_animation(win, win.current_y+1, win.current_x, 0.05)
        # if critical_hit:
        #     stdscr.attron(curses.A_REVERSE)
        #     stdscr.refresh()
        move_animation(win, win.current_y-3, win.current_x, 0.1)
        # if critical_hit:
        #     stdscr.attron(curses.A_REVERSE)
        #     stdscr.refresh()
        move_animation(win, win.current_y+2, win.current_x, 0.1)
        # if critical_hit:
        #     win.attron(curses.A_REVERSE)
        #     win.refresh()
    
    def evade_animation(win):
        if win is enemy_win:
            move_animation(win, win.current_y, win.current_x+3, 0.05)
            move_animation(win, win.current_y, win.current_x-3, 0.1)
        
        elif win is player_win:
            move_animation(win, win.current_y, win.current_x-3, 0.05)
            move_animation(win, win.current_y, win.current_x+3, 0.1)


    def dmg_crit_animation(win1, win2):
        # entity = entity.win
        
        move_animation(win1, 6, win1.x, 0.05)
        move_animation(win2, 6, win2.x, 0.05)
        move_animation(win1, 2, win1.x, 0.1)
        move_animation(win2, 6, win2.x, 0.05)
        move_animation(win1, 4, win1.x, 0.1)
        move_animation(win2, 6, win2.x, 0.05)
    
    def calc_def(attacker):
        defense = ((p.sum_defense) // (e.entity_lvl))

        if attacker.entity_class == "Scout":
            if defense >= 25:
                defense = 25
        
        elif attacker.entity_class == "Scout":
            if defense >= 50:
                defense = 50

        return math.floor(defense)

    def calc_crit():
        crit = ((p.sum_luck * 5) // (e.entity_lvl*2))

        return math.ceil(crit)

    def negate_dmg(attacker_win, defender_win, attacker, defender):
        if attacker.entity_class == 'Mage':
            return False
        
        if defender.entity_class == 'Mage':
            return False
            
        if defender.entity_class == 'Scout':
            if random.randrange(1, 100) <= 50:
                evade_animation(defender_win)
                time.sleep(0.5)
                
                return True
            else:
                return False
        
        elif defender.entity_class == 'Warrior':
            if random.randrange(1, 100) <= 25:
                attacker.hp -= math.floor(attacker.hp*0.15)
                # player_attack_recall_animation()
                # evade_animation(defender_win)
                take_dmg_animation(attacker_win, False)
                time.sleep(0.5)

                return True
            else:
                return False


    def deal_dmg(attacker, defender):
        global critical_hit_bool

        match attacker.entity_class:
            case 'Warrior':
                atk_stat = attacker.sum_strength
                def_stat = defender.sum_strength//2
            case 'Mage':
                atk_stat = attacker.sum_intelligence
                def_stat = defender.sum_intelligence//2
            case 'Scout':
                atk_stat = attacker.sum_dexterity
                def_stat = defender.sum_dexterity//2

        atk_stat_final = atk_stat - def_stat
        
        if (atk_stat_final) <= 0:
            atk_stat_final = 1
        
        dmg = random.randrange(math.floor(0.7*attacker.dmg) * (1 + (atk_stat_final // 10)), math.floor(1.3*attacker.dmg) * (1 + (atk_stat_final // 10)))

        if random.randint(1, 100) <= calc_crit():  # Calculating critical hit => (double damage)
            dmg = dmg * 2
            critical_hit_bool = True

        if attacker.entity_class == 'Warrior' or attacker.entity_class == 'Scout':
            dmg = dmg*(1-(calc_def(attacker)//100))
        
        defender.hp -= dmg
        
    
   
        
        
        

    # setup
    draw_hud(player_win, p)
    draw_hud(enemy_win, e)

    in_fight_bool = True
    player_turn_bool = True
    critical_hit_bool = False

    while in_fight_bool:
        
        if player_turn_bool:  # Player
            player_attack_animation()
            
            if not negate_dmg(player_win, enemy_win, p, e):
                deal_dmg(p, e)
                take_dmg_animation(enemy_win, critical_hit_bool)
                player_attack_recall_animation()
            else:
                player_attack_recall_animation()            
            
            critical_hit_bool = False
            player_turn_bool = False

        elif not player_turn_bool:  # Enemy
            enemy_attack_animation()
            
            if not negate_dmg(enemy_win, player_win, e, p):
                deal_dmg(e, p)
                take_dmg_animation(player_win, critical_hit_bool)
                enemy_attack_recall_animation()
            else:
                enemy_attack_recall_animation()
            
            critical_hit_bool = False
            player_turn_bool = True
    
        if e.hp <= 0:  # enemy died
            won = True
            in_fight_bool = False

        if p.hp <= 0:  # player died
            won = False
            in_fight_bool = False

        time.sleep(0.7)

       

    return won