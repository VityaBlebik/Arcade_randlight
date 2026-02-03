import arcade
import random
import time
from arcade.gui import UIManager,  UITextureButton
from pyglet.graphics import Batch

import game_db as db

from hero import Hero
from car import Car
from light import Light


screen_width = 1600
screen_height= 900
secreen_title = "Простая отрисовка изображения"


class Game_View(arcade.View):
    def __init__(self, width, height):
        super().__init__()
        self.game_width = width
        self.game_height = height
        self.texture = arcade.load_texture("images/background.png")
        db.start()
        self.pause = False
        self.setup()

    def setup(self):
        self.all_pause_time = 0
        self.pause_time = 0
        self.paused = False
        self.start_timer_limit = 10
        self.interval0 = 1
        self.interval1 = 3
        self.difficulty_speed = 0
        self.health = 3
        self.hero_speed = 20
        self.no_damage_time = 1
        self.car_speed0 = 50
        self.car_speed1 = 65
        self.start_game_interval0 = 2
        self.start_game_interval1 = 4

        self.batch = Batch()
        self.dead = False

        self.hero_list = arcade.SpriteList()
        self.horizontal_car_list = arcade.SpriteList()
        self.vertical_car_list = arcade.SpriteList()

        self.hero = Hero(self.game_width // 2, self.game_height // 2, self.hero_speed, self.health, self.no_damage_time)  
        self.hero_list.append(self.hero)

        self.start_game_time = time.time()
        self.start_game_interval = float(str(random.uniform(self.start_game_interval0,  self.start_game_interval1))[:4])
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

        self.pause_manager = UIManager()
        self.pause_manager.enable()
        self.pause_text = arcade.Text(text="ПАУЗА", x=self.game_width // 2, y=self.game_height - 150, color=arcade.color.WHITE, width=400, font_size=90, anchor_x="center", anchor_y="center")

        self.death_manager = UIManager()
        self.death_manager.enable()
        self.death_text = arcade.Text(text="СМЕРТЬ", x=self.game_width // 2, y=self.game_height - 150, color=(105, 100, 100), width=400, font_size=90, anchor_x="center", anchor_y="center")

        self.restart_texture = arcade.load_texture("images/button.png")
        self.restart_button = UITextureButton(x=self.game_width // 2 - 250, y=self.game_height // 2 + 100, widht=500, height=100, texture=self.restart_texture, text="Заново")
        self.restart_button.on_click = self.restart
        self.death_manager.add(self.restart_button)

        self.exit_texture = arcade.load_texture("images/button.png")
        self.exit_button = UITextureButton(x=self.game_width // 2 - 250, y=self.game_height // 2 - 100, widht=500, height=100, texture=self.exit_texture, text="Выйти")
        self.exit_button.on_click = self.exit_to_menu
        self.death_manager.add(self.exit_button)

        self.continue_texture = arcade.load_texture("images/button.png")
        self.continue_button = UITextureButton(x=self.game_width // 2 - 250, y=self.game_height // 2 + 100, widht=500, height=100, texture=self.continue_texture, text="Продолжить")
        self.continue_button.on_click = self.change_pause
        self.pause_manager.add(self.continue_button)

        self.exit_texture = arcade.load_texture("images/button.png")
        self.exit_button = UITextureButton(x=self.game_width // 2 - 250, y=self.game_height // 2 - 100, widht=500, height=100, texture=self.exit_texture, text="Выйти")
        self.exit_button.on_click = self.exit_to_menu
        self.pause_manager.add(self.exit_button)

        self.horizantal_light_texture = arcade.load_texture("images/light_h.png")
        self.horizontal_light_button = UITextureButton(x=self.game_width // 2 - 142, y=self.game_height // 2 - 100, width=42, height=200) 
        self.horizontal_light_button.on_click = self.horizontal_light.change_status
        self.light_manager.add(self.horizontal_light_button)
        
        self.vertical_light_texture = arcade.load_texture("images/light_v.png")
        self.vertical_light_button =  UITextureButton(x=self.game_width // 2 - 100, y=self.game_height // 2 + 98, width=200, height=42)
        self.vertical_light_button.on_click = self.vertical_light.change_status
        self.light_manager.add(self.vertical_light_button)
            
        self.game_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса
        self.game_camera.zoom = 2.0  

        self.updated_hearts = arcade.SpriteList()
        self.hearts = arcade.SpriteList()
        self.heart_texture = arcade.load_texture("images/heart.png")
        for heart in range(self.hero.health):
            heart = arcade.Sprite(center_x=50 + heart, center_y=self.game_height - 50)
            heart.texture = self.heart_texture
            self.hearts.append(heart)
        
        self.time_text = arcade.Text(text=f"Время: {0}", x=80, y=50, color=arcade.color.WHITE, width=200, font_size=20, anchor_x="center", anchor_y="center")

    def on_draw(self):
        self.clear()
        self.game_camera.use()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.game_width, self.game_height))
        self.hero_list.draw()
        self.horizontal_car_list.draw()
        self.vertical_car_list.draw()
        self.horizontal_light_list.draw()
        self.vertical_light_list.draw()
        arcade.draw_rect_filled(arcade.rect.XYWH(175, self.game_height // 2, 350, 900), arcade.color.BLACK)
        arcade.draw_rect_filled(arcade.rect.XYWH(self.game_width - 175, self.game_height // 2, 350, 900), arcade.color.BLACK)
        for car in self.horizontal_car_list:
            car.countdown.draw()
        for car in self.vertical_car_list:
            car.countdown.draw()
        self.gui_camera.use()
        self.hearts.draw()
        self.time_text.draw()
        if self.paused and not self.dead:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.game_width // 2, self.game_height // 2, 800, 800), (68, 202, 100, 158))
            self.pause_text.draw()
            self.pause_manager.enable()
            self.pause_manager.draw()
        else:
            self.pause_manager.disable()
        if self.dead:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.game_width // 2, self.game_height // 2, 800, 800), (28, 27, 27, 170))
            self.death_text.draw()
            self.death_manager.enable()
            self.death_manager.draw()
        else:
            self.death_manager.disable()
             
        
    def on_update(self, dt):
        if not self.paused:
            self.dt = dt
            self.hero_physics_engine.update()
            self.hero.update(dt)
            self.hero.update_animation(dt)
            self.make_car()
            self.check_collisions()
            self.check_timers()
            self.horizontal_car_list.update(dt)
            self.vertical_car_list.update(dt)
            self.death()
            self.time_text.text = f"Время: {int(time.time() - self.start_game_time - self.all_pause_time)}"
        self.difficulty_grow()
        self.hearts = arcade.SpriteList()
        for i in range(self.hero.health):
            heart = arcade.Sprite(center_x=50 + i * 50, center_y=self.game_height - 50)
            heart.texture = self.heart_texture
            self.hearts.append(heart)

    def check_timers(self):
        for i, car in enumerate(self.horizontal_car_list):
             if car.have_timer == False:
                car.timer_limit = min(25, self.start_timer_limit + i * 2)
                car.have_timer = True
        for i, car in enumerate(self.vertical_car_list):
            if car.have_timer == False:
                car.timer_limit = min(25, self.start_timer_limit + i * 2)
                car.have_timer = True

        for car in self.horizontal_car_list:
            if car.drive == False and car.timer_start == False:
                car.timer()
        for car in self.vertical_car_list:
            if car.drive == False and car.timer_start == False:
                car.timer()

    def check_collisions(self):
            #  Проверки горизонтальной линии
            for car in self.horizontal_car_list:
                if car.center_x > self.game_width - 350 + car.width:
                    car.remove_from_sprite_lists()

            for car in range(len(self.horizontal_car_list) - 1): #  тут обратный список, потому что машины добавляются справа налево в self.horizontal_car_list
                car1 = self.horizontal_car_list[car + 1]
                car2 = self.horizontal_car_list[car]
                if arcade.check_for_collision(car1, car2):  
                    car1.drive = False
                    #and car2.center_x - car2.width // 2 - car1.center_x + car1.width // 2 >= 10
                elif car2.center_x - car2.width // 2 - car1.center_x + car1.width // 2 >= 20:
                # elif not arcade.check_for_collision(car1, car2): #КОРОЧЕ ЕСЛИ ДАЖЕ МАШИНА ДАЛЕКО ВПЕРЕДИ, ТО ЕСЛИ СВЕТОФОР ВЫКЛЮЧЕН ИЗ-ЗА TRUE ТУТ СТОПАЕТСЯ МАШИНА
                    car1.drive = True

            if self.horizontal_light.status == -1:
                drive_horizontal_light = False
            else:
                drive_horizontal_light = True
            self.stop_cars_by_horizontal_light = arcade.check_for_collision_with_list(self.horizontal_light, self.horizontal_car_list)
            for stop_car_by_horizontal_light in self.stop_cars_by_horizontal_light:
                    stop_car_by_horizontal_light.drive = drive_horizontal_light 
                    if stop_car_by_horizontal_light.center_x + stop_car_by_horizontal_light.width // 2 > self.horizontal_light.center_x:
                        stop_car_by_horizontal_light.drive = True

            #  Проверки вертикальной линии

            for car in self.vertical_car_list:
                if car.center_y < - car.width:
                    car.remove_from_sprite_lists()

            for car in range(len(self.vertical_car_list) - 1): #  тут обратный список, потому что машины добавляются снизу вверх в self.vertical_car_list
                car1 = self.vertical_car_list[car + 1]
                car2 = self.vertical_car_list[car]
                if arcade.check_for_collision(car1, car2):  
                    car1.drive = False
                elif car1.center_y - car1.height // 2 - car2.center_y + car2.height // 2 >= 10:
                    car1.drive = True

            if self.vertical_light.status == -1:
                drive_vertical_light = False
            else:
                drive_vertical_light = True
            self.stop_cars_by_vertical_light = arcade.check_for_collision_with_list(self.vertical_light, self.vertical_car_list)
            for stop_car_by_vertical_light in self.stop_cars_by_vertical_light:
                    stop_car_by_vertical_light.drive = drive_vertical_light
                    if stop_car_by_vertical_light.center_y - stop_car_by_vertical_light.height // 2 < self.vertical_light.center_y:
                        stop_car_by_vertical_light.drive = True
        
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
        if key == arcade.key.ESCAPE:
            self.change_pause()
        if key == arcade.key.Z:
            self.zooming()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.hero.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.hero.change_x = 0
        if key == arcade.key.Z:
            self.zooming()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.zooming()
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.zooming()

    def zooming(self):
        if self.game_camera.zoom == 1.0:
            self.game_camera.zoom = 2.0
            self.light_manager.clear()
            self.horizontal_light_button = UITextureButton(x=self.game_width // 2 - 142, y=self.game_height // 2 - 100, width=42, height=200) 
            self.horizontal_light_button.on_click = self.horizontal_light.change_status
            self.vertical_light_button =  UITextureButton(x=self.game_width // 2 - 100, y=self.game_height // 2 + 98, width=200, height=42, texture=self.vertical_light_texture)
            self.vertical_light_button.on_click = self.vertical_light.change_status
            self.light_manager.add(self.vertical_light_button)
            self.light_manager.add(self.horizontal_light_button)
        else:
            self.game_camera.zoom = 1.0
            self.light_manager.clear()
            self.horizontal_light_button = UITextureButton(x=self.game_width // 2 - 71, y=self.game_height // 2 - 50, width=21, height=100) 
            self.horizontal_light_button.on_click = self.horizontal_light.change_status
            self.vertical_light_button =  UITextureButton(x=self.game_width // 2 - 50, y=self.game_height // 2 + 49, width=100, height=21, texture=self.vertical_light_texture)
            self.vertical_light_button.on_click = self.vertical_light.change_status
            self.light_manager.add(self.vertical_light_button)
            self.light_manager.add(self.horizontal_light_button)
    
    def make_car(self):
        if self.start_game_flag:
            self.make_car_end_time = time.time()
            if self.make_car_end_time - self.make_car_start_time >= self.make_car_interval:
                self.make_car_interval = random.uniform(self.interval0, self.interval1)
                self.make_car_start_time = time.time()
                self.place = random.choice([0, 1])
                if self.place == 0: #  горизонталь
                    car = Car(290, self.game_height // 2 + random.randint(-20, 20), self.place, self.car_speed0, self.car_speed1, self.difficulty_speed)
                    self.horizontal_car_list.append(car)
                else: #  вертикаль
                    car = Car(self.game_width // 2 + random.randint(-20, 20), self.game_height + 60, self.place, self.car_speed0, self.car_speed1, self.difficulty_speed)
                    self.vertical_car_list.append(car)
        else:
            self.add_car_time = time.time()
            if self.add_car_time - self.start_game_time >= self.start_game_interval:
                self.place = random.choice([0, 1])
                if self.place == 0: #  горизонталь
                    car = Car(290, self.game_height // 2 + random.randint(-20, 20), self.place, self.car_speed0, self.car_speed1, self.difficulty_speed)
                    self.horizontal_car_list.append(car)
                else: #  вертикаль
                    car = Car(self.game_width // 2 + random.randint(-20, 20), self.game_height + 60, self.place, self.car_speed0, self.car_speed1, self.difficulty_speed)
                    self.vertical_car_list.append(car)
                self.start_game_flag = True
                self.make_car_start_time = time.time()
                self.make_car_interval = random.uniform(self.interval0, self.interval1)
    
    def on_hide_view(self):
        pass
    #  ну тут типа музыку стопать

    def death(self):
        if self.hero.health == 0:
            self.dead = True
            self.paused = True

    def difficulty_grow(self):
        if not self.paused:
            if time.time() - self.start_game_time - self.all_pause_time >= 90:
                self.start_timer_limit = 7
                self.interval0 = 3
                self.interval1 = 4
                self.difficulty_speed = 15
            # elif

    
    def change_pause(self, event=None):
        if not self.dead:
            if not self.paused:
                self.paused = True
                self.pause_time = time.time()
            else:
                self.paused = False
                self.all_pause_time += time.time() - self.pause_time
    
    def exit_to_menu(self, event=None):
        from menuwindow import Menu_View
        self.window.show_view(Menu_View(1600, 900))
    
    def restart(self, event=None):
        self.setup()
                
if __name__ == "__main__":
    window = arcade.Window(1600, 900, "Игра", fullscreen=False)
    window.show_view(Game_View(1600, 900))
    arcade.run()
