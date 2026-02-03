import arcade
import json
from pyglet.graphics import Batch

import game_db as db
from arcade.gui import UIManager,  UITextureButton
from gamewindow import Game_View

class Select_level_View(arcade.View):
    def __init__(self, width, height):
        super().__init__()
        self.background_color = (11, 158, 36)
        self.select_level_width = width
        self.select_level_height = height
        db.start()

        self.batch = Batch()
        self.select_level_manager = UIManager()
        self.select_level_manager.enable()

        self.select_level_window_text = arcade.Text(text="Выбор уровня", x=self.select_level_width // 2, y=self.select_level_height - 150, color=arcade.color.WHITE, width=400, font_size=60, anchor_x="center", anchor_y="center")

        self.texts = []

        self.exit_texture = arcade.load_texture("images/button_exit.png")
        self.exit_button = UITextureButton(x=self.select_level_width - 40, y=self.select_level_height - 40, widht=40, height=40, texture=self.exit_texture) 
        self.exit_button.on_click = self.exit_to_menu
        self.select_level_manager.add(self.exit_button)

        for i in range(1, 4):
            time = db.get_time(i)
            if time == None:
                time = (0.0,)
            text = arcade.Text(text=f"{time[0]}", x=400 * i, y=350, color=arcade.color.WHITE, width=200, font_size=20, anchor_x="center", anchor_y="center", batch=self.batch)
            self.texts.append(text)

        for i in range(1, 4):
            self.level_texture = arcade.load_texture("images/button_level.png")
            self.level_button = UITextureButton(x=400 * i - 100, y=400, widht=200, height=200, texture=self.level_texture, text=f"{i} Уровень")
            self.level_button.on_click = lambda event, lvl=i: self.open_level(lvl)
            self.select_level_manager.add(self.level_button)

    def on_draw(self):
        self.clear()
        self.select_level_window_text.draw()
        self.select_level_manager.draw()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(Game_View(1600, 900) ) 
            
    def exit_to_menu(self, event=None):
        from menuwindow import Menu_View
        self.window.show_view(Menu_View(1600, 900))

    def on_show_view(self):
        pass

    def on_hide_view(self):
        pass
    #тоже выключить музыку
    
    def open_level(self, level, event=None):
        with open(f"level_settings/level{level}.json") as f:
            self.level_settings = json.load(f)
        self.window.show_view(Game_View(1600, 900, self.level_settings)) 

if __name__ == "__main__":
    window = arcade.Window(1600, 900, "Игра", fullscreen=False)
    window.show_view(Select_level_View(1600, 900))
    arcade.run()
