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
        self.speed = random.randint(10, 25)
        self.health = 3
        
        # Загрузка текстур
        if self.place == 0:
            self.texture = arcade.load_texture("images/carh1.png")
        else:
            self.texture = arcade.load_texture("images/carv1.png")
        
        
        
    def update(self, dt):
        """ Перемещение машины """
        if self.place == 0:
            self.center_x += 50 * dt
        else:
            self.center_y -= 50 * dt
        
        # Ограничение в пределах экрана
        # self.center_x = max(self.width/2, min(screen_width - self.width/2, self.center_x))
        # self.center_y = max(self.height/2, min(screen_height - self.height/2, self.center_y))
        