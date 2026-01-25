import arcade
from hero import Hero


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
        self.hero_list = arcade.SpriteList()
        # Загружаем текстуру (изображение)
        self.hero = Hero(self.game_width // 2, self.game_height // 2)
        self.hero_list.append(self.hero)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.game_width, self.game_height))
        self.hero_list.draw()
    
    def on_update(self, dt):
        self.hero_list.update()


    
if __name__ == "__main__":
    game = Game(screen_width, screen_height, secreen_title)
    arcade.run()