import arcade
import time


class Hero(arcade.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        
        self.speed = 40
        self.health = 3
        self.damage_no = True
        self.texture = arcade.load_texture("images/hero.png")
        self.center_x = start_x
        self.center_y = start_y
        
    def update(self, dt):
        """ Перемещение персонажа """
        self.center_x += self.change_x
        self.center_y += self.change_y

    def get_damage(self):
        if self.damage_no:
            self.damage_no_timer_start = time.time()
            self.damage_no = False
            self.health -= 1
        self.damage_no_timer_end = time.time()
        if self.damage_no_timer_end - self.damage_no_timer_start >= 5:
            self.damage_no = True
        
