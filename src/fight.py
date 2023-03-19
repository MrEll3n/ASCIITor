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

    player_win = Window("fight", p_y, 0, rows-8, hcols-20, "")
    player_win.clear_window()

    #player_win.win.hline(player_win.height//2, 1, "-", player_win.width-2)
    player_win.win.refresh()

    enemy_win = Window("fight", e_y, hcols+20, rows-8, hcols-20, "")
    enemy_win.clear_window()

    #enemy_win.win.hline(enemy_win.height//2 , 1, "-", player_win.width-2)
    enemy_win.win.refresh()

    player = player_win.win
    enemy = enemy_win.win

    def draw_hud(win, entity):
        hheight = win.height//2
        hwidth = win.width//2

        # Middle card
        win.win.addstr(hheight + 2, hwidth - (len(entity.name)//2) - 2, f"< {entity.name} >")
        win.win.move(hheight + 3, hwidth + 12)
        win.win.clrtoeol()
        
        win.win.addstr(hheight + 3, hwidth + 12, f"{entity.hp}/{entity.maxhp}")
        win.win.addstr(hheight + 4, 2, f"|{win.draw_hp_bar(entity)}|")

        # Bottom card
        win.win.addstr(hheight + 8, hwidth-8, f"STR: {entity.sum_strength}")
        win.win.addstr(hheight + 10, hwidth-8, f"DEX: {entity.sum_dexterity}")
        win.win.addstr(hheight + 12, hwidth-8, f"INT: {entity.sum_intelligence}")

        win.win.addstr(hheight + 8, (hwidth+8)-7, f"STA: {entity.sum_stamina}")
        win.win.addstr(hheight + 10, (hwidth+8)-7, f"DEF: {entity.sum_defense}")
        win.win.addstr(hheight + 12, (hwidth+8)-7, f"LUK: {entity.sum_luck}")

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
        win.mvwin(y, x)

        stdscr.erase()
        stdscr.refresh()
        redraw_battle()

        win.refresh()
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

        move_animation(player, p_y, 7, 0.05)
        move_animation(player, p_y, 35, 0.05)
        move_animation(player, p_y, 34, 0.1)
        

    def player_attack_recall_animation():
        
        move_animation(player, p_y, 10, 0.1)
        move_animation(player, p_y, 6, 0.1)
        move_animation(player, p_y, 2, 0.1)
        move_animation(player, p_y, 0, 0.1)

    def enemy_attack_animation(dmg=False):
        # enemy = enemy_win.win
        
        time.sleep(0.5)

        move_animation(enemy, e_y, enemy_win.x-7, 0.05)
        move_animation(enemy, e_y, enemy_win.x-35, 0.1)
        move_animation(enemy, e_y, enemy_win.x-34, 0.1)
        

    def enemy_attack_recall_animation():

        move_animation(enemy, e_y, enemy_win.x-10, 0.1)
        move_animation(enemy, e_y, enemy_win.x-6, 0.1)
        move_animation(enemy, e_y, enemy_win.x-2, 0.1)
        move_animation(enemy, e_y, enemy_win.x-0, 0.1)

    def take_dmg_animation(win, critical_hit):
        # entity = entity.win
        if critical_hit:
            stdscr.attron(curses.A_REVERSE)
            stdscr.refresh()
        move_animation(win.win, 5, win.x, 0.05)
        # if critical_hit:
        #     stdscr.attron(curses.A_REVERSE)
        #     stdscr.refresh()
        move_animation(win.win, 3, win.x, 0.1)
        # if critical_hit:
        #     stdscr.attron(curses.A_REVERSE)
        #     stdscr.refresh()
        move_animation(win.win, 4, win.x, 0.1)
        if critical_hit:
            stdscr.attron(curses.A_REVERSE)
            stdscr.refresh()

        
    
    def dmg_crit_animation(win1, win2):
        # entity = entity.win
        
        move_animation(win1.win, 6, win1.x, 0.05)
        move_animation(win2.win, 6, win2.x, 0.05)
        move_animation(win1.win, 2, win1.x, 0.1)
        move_animation(win2.win, 6, win2.x, 0.05)
        move_animation(win1.win, 4, win1.x, 0.1)
        move_animation(win2.win, 6, win2.x, 0.05)
    
    def calc_def():
        defense = ((p.sum_defense) // (e.entity_lvl))

        return math.floor(defense)

    def calc_crit():
        crit = ((p.sum_luck * 5) // (e.entity_lvl*2))

        return math.ceil(crit)

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
            dmg = dmg*(1-(calc_def()//100))
        
        defender.hp -= dmg
        
    
    def negate_dmg(attacker, defender):
        match attacker.entity_class:
            case 'Warrior':
                negate_stat = defender.sum_strength
            case 'Mage':
                negate_stat = defender.sum_intelligence
            case 'Scout':
                negate_stat = defender.sum_dexterity

    # setup
    draw_hud(player_win, p)
    draw_hud(enemy_win, e)

    in_fight_bool = True
    player_turn_bool = True
    critical_hit_bool = False

    while in_fight_bool:
        
        if player_turn_bool:
            player_attack_animation()
            
            deal_dmg(p, e)
            stdscr.attron(curses.A_REVERSE)
            # stdscr.refresh()
            take_dmg_animation(enemy_win, critical_hit_bool)
            player_attack_recall_animation()
            
            critical_hit_bool = False
            player_turn_bool = False

        elif not player_turn_bool:
            enemy_attack_animation()
            
            deal_dmg(e, p)
            take_dmg_animation(player_win, critical_hit_bool)
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