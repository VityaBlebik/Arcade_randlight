import arcade
import random
import time

screen_width = 1600
screen_height= 900


class Car(arcade.Sprite):
    def __init__(self, start_x, start_y, place):
        super().__init__()

        self.center_x = start_x
        self.center_y = start_y
        self.place = place
        # Основные характеристики
        self.speed = random.randint(40, 55)
        self.drive = True
        self.timer_start = False
        self.have_timer = False
        self.drive_nonstop = False
        self.timer_limit = 0
        
        # Загрузка текстур
        if self.place == 0:
            self.texture = arcade.load_texture("images/carh.png")
        else:
            self.texture = arcade.load_texture("images/carv.png")
        
        
        
    def update(self, dt):
        if self.drive == True:
            if self.place == 0:
                self.center_x += self.speed  * dt
            else:
                self.center_y -= self.speed * dt
        self.timer()

    def timer(self):
        if self.timer_start == False:
            self.timer_start = True
            self.countdown_start = time.time()
        if self.drive == False:
            self.countdown_end = time.time()
            if self.countdown_end - self.countdown_start >= self.timer_limit:
                self.drive_nonstop == True
                self.timer_limit = 0
        else:
            self.timer_limit -= self.countdown_end - self.countdown_start
            self.timer_start = False
            self.countdown_start = 0
            self.countdown_end = 0
        