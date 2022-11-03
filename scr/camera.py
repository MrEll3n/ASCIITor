import curses
from curses.textpad import Textbox, rectangle

class Camera:
    def __init__(self, cam_width, cam_height, cam_x, cam_y):
        self.cam_width = cam_width
        self.cam_height = cam_height
        self.cam_x = cam_x
        self.cam_y = cam_y

    def move_left(self):
        self.cam_x -= 1
    
    def move_right(self):
        self.cam_x += 1
    
    def move_up(self):
        self.cam_y -= 1
    
    def move_down(self):
        self.cam_y += 1