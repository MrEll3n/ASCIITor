import curses
import json
import random
from curses.textpad import Textbox, rectangle


class Enemy:
    def __init__(self, name, enemy_class, enemy_lvl, dmg, stamina, intelligence, strength, dexterity, defense, luck, game_pad, map):
        #self.x = x
        #self.y = y
        self.name = name
        self.entity_class = enemy_class
        self.entity_lvl = enemy_lvl

        self.dmg = dmg

        self.sum_stamina = stamina
        self.sum_strength = strength
        self.sum_dexterity = dexterity
        self.sum_intelligence = intelligence
        self.sum_defense = defense
        self.sum_luck = luck

        self.maxhp = self.sum_stamina * 4 * (self.entity_lvl+1)
        self.hp = self.maxhp

        #self.floor = ""
        self.game_pad = game_pad
        self.map = map

        #self.floor = self.get_floor(self.map, 0, 0, 1)
        #self.draw_player(self.map, 0, 0)

def create_enemy(lvl, gap_bool=False):
    if gap_bool:
        if lvl == 1:
            pool = [lvl, lvl+1]
        elif lvl > 1:
            pool = [lvl-1, lvl, lvl+1]
    else:
        pool = [lvl]
    
    result = pool[random.randrange(len(pool))]


    with open('Enemies.json', 'r') as f:
        enemy_list = json.load(f)

    enemy = enemy_list[str(result)][random.randrange(len(enemy_list[str(result)]))]
    return enemy