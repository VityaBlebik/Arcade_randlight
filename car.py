import arcade
import random


screen_width = 1600
screen_height= 900


class Car(arcade.Sprite):
    def __init__(self, start_x, start_y, place):
        super().__init__()

        self.center_x = start_x
        self.center_y = start_y
        self.place = place
        # Основные характеристики
        self.speed = 50#random.randint(10, 25)
        self.drive = True
        
        # Загрузка текстур
        if self.place == 0:
            self.texture = arcade.load_texture("images/carh.png")
        else:
            self.texture = arcade.load_texture("images/carv.png")
        
        
        
    def update(self, dt):
        """ Перемещение машины """
        if self.drive == True:
            if self.place == 0:
                self.center_x += self.speed  * dt
            else:
                self.center_y -= self.speed * dt
        
        # Ограничение в пределах экрана
        # self.center_x = max(self.width/2, min(screen_width - self.width/2, self.center_x))
        # self.center_y = max(self.height/2, min(screen_height - self.height/2, self.center_y))
        