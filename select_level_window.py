import arcade

from arcade.gui import UIManager,  UITextureButton
from pyglet.graphics import Batch
from gamewindow import Game_View

class Menu_View(arcade.View):
    def __init__(self, width, height):
        super().__init__()
        self.background_color = (11, 158, 36)
        self.menu_width = width
        self.menu_height = height

        self.menu_manager = UIManager()
        self.menu_manager.enable()
        self.select_level_window_text = arcade.Text(text="Выбор уровня", x=self.menu_width // 2, y=self.menu_height - 150, color=arcade.color.WHITE, width=400, font_size=60, anchor_x="center", anchor_y="center")
        self.background_texture = arcade.load_texture("images/carh.png")

    def on_draw(self):
        self.clear()
        # arcade.draw_rect_filled(arcade.XYWH(self.menu_width // 2, 0, self.menu_width, 500), (80, 207, 16))
        # arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(self.menu_width // 2, self.menu_height // 2, 600, 400))
        self.select_level_window_text.draw()
        # self.menu_manager.draw()
            
       
    
    def go_to_select_level(self, event=None):
        self.window.show_view(Game_View(1600, 900))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(Game_View(1600, 900) ) 

    def on_hide_view(self):
        pass
    #тоже выключить музыку

    def quit_from_game(self, event=None):
        window.close()

if __name__ == "__main__":
    window = arcade.Window(1600, 900, "Игра", fullscreen=False)
    window.show_view(Menu_View(1600, 900))
    arcade.run()
