import arcade

# Задаём размер окна
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Простая отрисовка изображения"

class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        # Основные характеристики
        self.scale = 1.0
        self.speed = 300
        self.health = 3
        
        # Загрузка текстур
        self.idle_texture = arcade.load_texture("images/hero.png")
        self.texture = self.idle_texture
        
        # Жёстко ставим персонажа в центр экрана (лучше передавать позицию в __init__)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        
    def update(self, delta_time):
        """ Перемещение персонажа """
        self.center_x += 50 * delta_time
        self.center_y += 50 * delta_time
        
        # Ограничение в пределах экрана
        self.center_x = max(self.width/2, min(SCREEN_WIDTH - self.width/2, self.center_x))
        self.center_y = max(self.height/2, min(SCREEN_HEIGHT - self.height/2, self.center_y))

class MyGame(arcade.Window):
    def __init__(self, width, height, title,):
        super().__init__(width, height, title, fullscreen=True)
        self.w = width
        self.h = height
        self.texture = arcade.load_texture("images/background.png")
        self.setup()

    def setup(self):
        self.hero_list = arcade.SpriteList()
        # Загружаем текстуру (изображение)
        self.hero = Hero()
        self.hero_list.append(self.hero)

    def on_draw(self):
        self.clear()

        # Отрисовываем изображение во весь экран
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.w // 2, self.h // 2, self.w, self.h))
        self.hero_list.draw()
    
    def on_update(self, dt):
        self.hero_list.update()


    
if __name__ == "__main__":
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()