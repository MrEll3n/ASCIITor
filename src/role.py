import curses
from curses.textpad import Textbox, rectangle


class Role:
    def __init__(self, name, stamina, strength, dexterity, intelligence, defense, luck):
        self.name = name
        self.stamina = stamina
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.defense = defense
        self.luck = luck
