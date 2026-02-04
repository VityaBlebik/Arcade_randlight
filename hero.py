import arcade
import time


class Hero(arcade.Sprite):
    def __init__(self, start_x, start_y, speed, health, no_damage_time):
        super().__init__()
        
        self.no_damage_time = no_damage_time
        self.speed = speed
        self.health = health
        self.damage_no = True
        self.default_texture = arcade.load_texture("images/hero.png")
        self.texture = self.default_texture
        self.center_x = start_x
        self.center_y = start_y
        self.texture_change_time = 0
        self.current_texture = 0
        self.walk_textures = []
        self.is_walking = False
        self.damage_no_timer_start = 0

        for i in range(0, 5):
            texture = arcade.load_texture(f"images/hero{i}.png")
            self.walk_textures.append(texture)
        
    def update(self, dt):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.is_walking = self.change_x != 0 or self.change_y != 0
        if self.change_x < 0:
            self.scale_x = -1
        else:
            self.scale_x = 1
        
    def update_animation(self, delta_time: float = 1/60):
        """ Обновление анимации """
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= 0.13:
                self.texture_change_time = 0
                self.current_texture += 1
                self.texture = self.walk_textures[self.current_texture % len(self.walk_textures)]
        else:
            self.texture = self.default_texture

    def get_damage(self):
        if self.damage_no:
            self.damage_no_timer_start = time.time()
            self.damage_no = False
            self.health -= 1
        self.damage_no_timer_end = time.time()
        if self.damage_no_timer_end - self.damage_no_timer_start >= self.no_damage_time:
            self.damage_no = True
