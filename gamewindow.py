import arcade
import random
import time
from arcade.gui import UIManager,  UITextureButton

from hero import Hero
from car import Car
from light import Light

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
        self.interval0 = 3
        self.interval1 = 7
        self.hero_list = arcade.SpriteList()
        self.horizontal_car_list = arcade.SpriteList()
        self.vertical_car_list = arcade.SpriteList()

        self.hero = Hero(self.game_width // 2, self.game_height // 2)  
        self.hero_list.append(self.hero)

        self.start_game_time = time.time()
        self.start_game_interval = float(str(random.uniform(2, 4))[:4])
        self.start_game_flag = False

        self.hero_walls = arcade.SpriteList()
        self.hero_walls.append(arcade.SpriteSolidColor(1, 100, center_x=self.game_width // 2 - 50, center_y=self.game_height // 2, color=(0, 0, 0, 0))) # левая
        self.hero_walls.append(arcade.SpriteSolidColor(1, 100, center_x=self.game_width // 2 + 50, center_y=self.game_height // 2, color=(0, 0, 0, 0))) # правая
        self.hero_walls.append(arcade.SpriteSolidColor(100, 1, center_x=self.game_width // 2 , center_y=self.game_height // 2 + 50, color=(0, 0, 0, 0))) # верхняя
        self.hero_walls.append(arcade.SpriteSolidColor(100, 1, center_x=self.game_width // 2, center_y=self.game_height // 2 - 50, color=(0, 0, 0, 0))) # нижняя
        
        self.hero_physics_engine = arcade.PhysicsEngineSimple(self.hero, self.hero_walls)

        self.horizontal_light = Light(0, 1, self.game_width // 2 - 60, self.game_height // 2)
        self.horizontal_light_list = arcade.SpriteList()
        self.horizontal_light_list.append(self.horizontal_light)

        self.vertical_light = Light(1, 1, self.game_width // 2, self.game_height // 2 + 60)
        self.vertical_light_list = arcade.SpriteList()
        self.vertical_light_list.append(self.vertical_light)

        self.light_manager = UIManager()
        self.light_manager.enable()

        self.horizantal_light_texture = arcade.load_texture("images/light_h.png")
        self.horizontal_light_button = UITextureButton(x=self.game_width // 2 - 71, y=self.game_height // 2 - 50, width=21, height=100, texture=self.horizantal_light_texture)
        self.horizontal_light_button.on_click = self.horizontal_light.change_status
        self.light_manager.add(self.horizontal_light_button)
        
        self.vertical_light_texture = arcade.load_texture("images/light_v.png")
        self.vertical_light_button =  UITextureButton(x=self.game_width // 2 - 50, y=self.game_height // 2 + 49, width=100, height=21, texture=self.vertical_light_texture)
        self.vertical_light_button.on_click = self.vertical_light.change_status
        self.light_manager.add(self.vertical_light_button)
        
        
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.game_width, self.game_height))
        self.hero_list.draw()
        self.horizontal_car_list.draw()
        self.vertical_car_list.draw()
        self.horizontal_light_list.draw()
        self.vertical_light_list.draw()
        self.light_manager.draw()
        arcade.draw_rect_filled(arcade.rect.XYWH(175, screen_height // 2, 350, 900), arcade.color.BLACK)
        arcade.draw_rect_filled(arcade.rect.XYWH(screen_width - 175, screen_height // 2, 350, 900), arcade.color.BLACK)
    
    def on_update(self, dt):
        self.dt = dt
        self.hero_physics_engine.update()
        self.horizontal_car_list.update(dt)
        self.vertical_car_list.update(dt)
        self.make_car()
        self.check_collisions()

    
    def check_collisions(self):
            #  Проверки горизонтальной линии
            for car in self.horizontal_car_list:
                if car.center_x > self.game_width - 350 + car.width:
                    car.remove_from_sprite_lists()

            if self.horizontal_light.status == -1:
                drive_horizontal_light = False
            else:
                drive_horizontal_light = True
            self.stop_cars_by_horizontal_light = arcade.check_for_collision_with_list(self.horizontal_light, self.horizontal_car_list)
            for stop_car_by_horizontal_light in self.stop_cars_by_horizontal_light:
                    stop_car_by_horizontal_light.drive = drive_horizontal_light
                    if stop_car_by_horizontal_light.center_x + stop_car_by_horizontal_light.width // 2 > self.horizontal_light.center_x - self.horizontal_light.width // 2 + 5:
                        stop_car_by_horizontal_light.drive = True
            
            for car in range(len(self.horizontal_car_list) - 1): #  тут обратный список, потому что машины добавляются справа налево в self.horizontal_car_list
                car1 = self.horizontal_car_list[car + 1]
                car2 = self.horizontal_car_list[car]
                if arcade.check_for_collision(car1, car2):  
                    car1.drive = False
                elif not arcade.check_for_collision(car1, car2) and car2.center_x - car2.width // 2 - car1.center_x + car1.width // 2 >= 10 and drive_horizontal_light == True:
                    car1.drive = True

            #  Проверки вертикальной линии

            for car in self.vertical_car_list:
                if car.center_y < - car.width - 10:
                    car.remove_from_sprite_lists()

            if self.vertical_light.status == -1:
                drive_vertical_light = False
            else:
                drive_vertical_light = True
            self.stop_cars_by_vertical_light = arcade.check_for_collision_with_list(self.vertical_light, self.vertical_car_list)
            for stop_car_by_vertical_light in self.stop_cars_by_vertical_light:
                    stop_car_by_vertical_light.drive = drive_vertical_light
                    if stop_car_by_vertical_light.center_y - stop_car_by_vertical_light.height // 2 < self.vertical_light.center_y + self.vertical_light.height // 2 - 5:
                        stop_car_by_vertical_light.drive = True
            
            for car in range(len(self.vertical_car_list) - 1): #  тут обратный список, потому что машины добавляются снизу вверх в self.vertical_car_list
                car1 = self.vertical_car_list[car + 1]
                car2 = self.vertical_car_list[car]
                if arcade.check_for_collision(car1, car2):  
                    car1.drive = False
                elif not arcade.check_for_collision(car1, car2) and car1.center_y - car1.height // 2 - car2.center_y + car2.height // 2 >= 10 and drive_vertical_light == True:
                    car1.drive = True

            if arcade.check_for_collision_with_lists(self.hero, [self.horizontal_car_list, self.vertical_car_list]):
                self.hero.get_damage()

            for car in self.horizontal_car_list:
                removed_cars = arcade.check_for_collision_with_list(car, self.vertical_car_list)
                if len(removed_cars) > 0:
                    self.hero.get_damage()
                    for removed_car in removed_cars:
                        removed_car.remove_from_sprite_lists()
                    car.remove_from_sprite_lists()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.hero.change_y = self.hero.speed * self.dt
        elif key == arcade.key.S:
            self.hero.change_y = -self.hero.speed * self.dt
        elif key == arcade.key.A:
            self.hero.change_x = -self.hero.speed * self.dt
        elif key == arcade.key.D:
           self.hero.change_x = self.hero.speed * self.dt

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
                    car = Car(self.game_width // 2 + random.randint(-20, 20), screen_height + 60, self.place)
                    self.vertical_car_list.append(car)
                self.start_game_flag = True
                self.make_car_start_time = time.time()
                self.make_car_interval = random.uniform(self.interval0, self.interval1)

                

    
if __name__ == "__main__":
    game = Game(screen_width, screen_height, secreen_title)
    arcade.run()
