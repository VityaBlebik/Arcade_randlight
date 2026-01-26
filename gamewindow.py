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
        super().__init__(width, height, title, fullscreen=True)
        self.game_width = width
        self.game_height = height
        self.texture = arcade.load_texture("images/background.png")
        self.setup()

    def setup(self):
        self.interval0 = 2
        self.interval1 = 4
        self.hero_list = arcade.SpriteList()
        self.horizontal_car_list = arcade.SpriteList()
        self.vertical_car_list = arcade.SpriteList()

        self.hero = Hero(self.game_width // 2, self.game_height // 2)  
        self.hero_list.append(self.hero)

        self.start_game_time = time.time()
        self.start_game_interval = float(str(random.uniform(1, 2))[:4])
        self.start_game_flag = False
        self.hero_walls = arcade.SpriteList()
        self.hero_walls.append(arcade.SpriteSolidColor(1, 100, center_x=self.game_width // 2 - 50, center_y=self.game_height // 2, color=(0, 0, 0, 0))) # левая
        self.hero_walls.append(arcade.SpriteSolidColor(1, 100, center_x=self.game_width // 2 + 50, center_y=self.game_height // 2, color=(0, 0, 0, 0))) # правая
        self.hero_walls.append(arcade.SpriteSolidColor(100, 1, center_x=self.game_width // 2 , center_y=self.game_height // 2 + 50, color=(0, 0, 0, 0))) # верхняя
        self.hero_walls.append(arcade.SpriteSolidColor(100, 1, center_x=self.game_width // 2, center_y=self.game_height // 2 - 50, color=(0, 0, 0, 0))) # нижняя
        
        self.hero_physics_engine = arcade.PhysicsEngineSimple(self.hero, self.hero_walls)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.game_width, self.game_height))
        self.hero_list.draw()
        self.horizontal_car_list.draw()
        self.vertical_car_list.draw()
        arcade.draw_rect_filled(arcade.rect.XYWH(175, screen_height // 2, 350, 900), arcade.color.BLACK)
        arcade.draw_rect_filled(arcade.rect.XYWH(screen_width - 175, screen_height // 2, 350, 900), arcade.color.BLACK)
    
    def on_update(self, dt):
        self.hero_physics_engine.update()
        self.horizontal_car_list.update(dt)
        self.vertical_car_list.update(dt)
        self.make_car()
    

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.hero.change_y = self.hero.speed
        elif key == arcade.key.S:
            self.hero.change_y = -self.hero.speed
        elif key == arcade.key.A:
            self.hero.change_x = -self.hero.speed
        elif key == arcade.key.D:
           self.hero.change_x = self.hero.speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.hero.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.hero.change_x = 0
    
    def make_car(self):
        if self.start_game_flag:
            self.make_car_end_time = time.time()
            if self.make_car_end_time - self.make_car_start_time >= self.make_car_interval:
                self.make_car_interval = random.uniform(self.interval0, self.interval1)
                self.make_car_start_time = time.time()
                self.place = 0#random.choice([0, 1])
                if self.place == 0: #  горизонталь
                    car = Car(290, screen_height // 2 + random.randint(-20, 20), self.place)
                    self.horizontal_car_list.append(car)
                else: #  вертикаль
                    car = Car(800 + random.randint(-20, 20), screen_height + 60, self.place)
                    self.vertical_car_list.append(car)
        else:
            self.add_car_time = time.time()
            if self.add_car_time - self.start_game_time >= self.start_game_interval:
                self.place = 0#random.choice([0, 1])
                if self.place == 0: #  горизонталь
                    car = Car(290, screen_height // 2 + random.randint(-20, 20), self.place)
                    self.horizontal_car_list.append(car)
                else: #  вертикаль
                    car = Car(800 + random.randint(-20, 20), screen_height + 60, self.place)
                    self.vertical_car_list.append(car)
                self.start_game_flag = True
                self.make_car_start_time = time.time()
                self.make_car_interval = random.uniform(self.interval0, self.interval1)

                

    
if __name__ == "__main__":
    game = Game(screen_width, screen_height, secreen_title)
    arcade.run()
