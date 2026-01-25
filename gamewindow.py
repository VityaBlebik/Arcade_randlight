import arcade
import random
import time

from hero import Hero
from car import Car

screen_width = 1600
screen_height= 900
secreen_title = "Простая отрисовка изображения"


class Game(arcade.Window):
    def __init__(self, width, height, title,):
        super().__init__(width, height, title, fullscreen=False)
        self.game_width = width
        self.game_height = height
        self.texture = arcade.load_texture("images/background.png")
        self.setup()

    def setup(self):
        self.interval0 = 2
        self.interval1 = 3
        self.hero_list = arcade.SpriteList()
        self.horizontal_car_list = arcade.SpriteList()
        self.vertical_car_list = arcade.SpriteList()

        self.hero = Hero(self.game_width // 2, self.game_height // 2)  
        self.hero_list.append(self.hero)

        self.start_game_time = time.time()
        self.start_game_interval = float(str(random.uniform(1, 2))[:4])


        self.start_game_flag = False

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.game_width, self.game_height))
        self.hero_list.draw()
        self.horizontal_car_list.draw()
        self.vertical_car_list.draw()
    
    def on_update(self, dt):
        self.hero_list.update()
        self.horizontal_car_list.update(dt)
        self.vertical_car_list.update(dt)
        self.make_car()
    
    def make_car(self):
        if self.start_game_flag:
            self.make_car_end_time = time.time()
            if self.make_car_end_time - self.make_car_start_time >= self.make_car_interval:
                self.place = 0              #  позже random.choice(0, 1)
                if self.place == 0:
                    car = Car(350, self.height // 2, self.place)
                    self.horizontal_car_list.append(car)
                else:
                    car = Car(350, self.height // 2, self.place)
                    self.vertical_car_list.append(car)
        else:
            self.add_car_time = time.time()
            if self.add_car_time - self.start_game_time >= self.start_game_interval:
                self.place = 0              #  позже random.choice(0, 1)
                print("first")
                car = Car(350, self.height // 2, self.place)
                if self.place == 0:
                    self.horizontal_car_list.append(car)
                else:
                    self.vertical_car_list.append(car)
                self.start_game_flag = True
                self.make_car_start_time = time.time()
                self.make_car_interval = random.uniform(self.interval0, self.interval1)

                

    
if __name__ == "__main__":
    game = Game(screen_width, screen_height, secreen_title)
    arcade.run()
