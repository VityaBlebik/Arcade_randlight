import arcade
import json

from select_level_window import Select_level_View
from arcade.gui import UIManager,  UITextureButton, UISlider

class Menu_View(arcade.View):
    def __init__(self, width, height):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY
        self.menu_width = width
        self.menu_height = height
        self.settings_open = False

        self.menu_manager = UIManager()
        self.menu_manager.enable()
        self.settings_manager = UIManager()
        self.menuwindow_text = arcade.Text(text="Главное меню", x=self.menu_width // 2, y=self.menu_height - 150, color=arcade.color.WHITE, width=400, font_size=90, anchor_x="center", anchor_y="center")
        
        self.settings_music_slider =  UISlider(x=self.menu_width // 2 - 100, y=self.menu_height // 2 + 200 , width=300, height=25, min_value=0, max_value=100, step=1, value=25)
        self.settings_music_slider.on_change = self.update_settings_music_slider
        self.settings_manager.add(self.settings_music_slider)

        self.settings_sound_slider =  UISlider(x=self.menu_width // 2 - 100, y=self.menu_height // 2 , width=300, height=25, min_value=0, max_value=100, step=1, value=25)
        self.settings_sound_slider.on_change = self.update_settings_sound_slider
        self.settings_manager.add(self.settings_sound_slider)

        self.settings_music_slider_text = arcade.Text(text=f"Громкость музыки: 25", x=self.menu_width // 2 + 50, y=self.menu_height - 150, color=arcade.color.WHITE, width=400, font_size=20, anchor_x="center", anchor_y="center")
        self.settings_sound_slider_text = arcade.Text(text=f"Громкость звука: 25", x=self.menu_width // 2 + 50, y=self.menu_height - 350, color=arcade.color.WHITE, width=400, font_size=20, anchor_x="center", anchor_y="center")

        self.settings_exit_texture = arcade.load_texture("images/button_exit.png")
        self.settings_exit_button = UITextureButton(x=self.menu_width // 2 + 320, y=self.menu_height // 2 + 310, widht=40, height=40, texture=self.settings_exit_texture) 
        self.settings_exit_button.on_click = self.open_settings
        self.settings_manager.add(self.settings_exit_button)

        self.select_level_texture = arcade.load_texture("images/button.png")
        self.select_level_button = UITextureButton(x=self.menu_width // 2 - 250, y=self.menu_height // 2 + 100, widht=500, height=100, texture=self.select_level_texture, text="Выбор уровня") 
        self.select_level_button.on_click = self.go_to_select_level
        self.menu_manager.add(self.select_level_button)

        self.settings_button = UITextureButton(x=self.menu_width // 2 - 250, y=self.menu_height // 2 - 50, widht=500, height=100, texture=self.select_level_texture, text="Настройки") 
        self.settings_button.on_click = self.open_settings
        self.menu_manager.add(self.settings_button)

        self.quit_button = UITextureButton(x=self.menu_width // 2 - 250, y=self.menu_height // 2 - 200, widht=500, height=100, texture=self.select_level_texture, text="Выход") 
        self.quit_button.on_click = self.quit_from_game
        self.menu_manager.add(self.quit_button)
        
        self.background_texture = arcade.load_texture("images/carh.png")

        self.background_music = arcade.load_sound("sounds/menu_music.mp3")
        self.click_sound = arcade.load_sound("sounds/menu_sound.wav")

    def on_draw(self):
        self.clear()
        arcade.draw_rect_filled(arcade.XYWH(self.menu_width // 2, 0, self.menu_width, 500), (80, 207, 16))
        arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(self.menu_width // 2, self.menu_height // 2, 600, 400))
        self.menuwindow_text.draw()
        self.menu_manager.draw()
        self.menu_manager.enable()
        if self.settings_open == True:
            arcade.draw_rect_filled(arcade.XYWH(self.menu_width // 2, self.menu_height // 2, 720, 700), (11, 158, 36))
            self.settings_music_slider_text.draw()
            self.settings_sound_slider_text.draw()
            self.settings_manager.enable()
            self.settings_manager.draw()
            self.menu_manager.disable()
        else:
            self.settings_manager.disable()

    def open_settings(self, event=None):
        arcade.play_sound(self.click_sound, volume=int(self.settings_sound_slider_text.text.split()[-1]) / 100)
        if not self.settings_open:
            self.settings_open = True
        else:
            self.settings_open = False
            volumes = {"music_volume":int(self.settings_music_slider_text.text.split()[-1]), "sound_volume":int(self.settings_sound_slider_text.text.split()[-1])}
            with open('volumes.json', 'w') as f:
                json.dump(volumes, f)

    def on_update(self, dt):
        self.background_player.volume = int(self.settings_music_slider_text.text.split()[-1]) / 100

    def update_settings_music_slider(self, event):
        # arcade.play_sound(self.click_sound, volume=int(self.settings_sound_slider_text.text.split()[-1]) / 100)
        volume_value = int(event.new_value)
        self.settings_music_slider_text.text = f"Громкость музыки: {volume_value}"
    
    def update_settings_sound_slider(self, event):
        arcade.play_sound(self.click_sound, volume=int(self.settings_sound_slider_text.text.split()[-1]) / 100)
        volume_value= int(event.new_value)
        self.settings_sound_slider_text.text = f"Громкость звука: {volume_value}"
    
    def go_to_select_level(self, event=None):
        self.menu_manager.disable()
        arcade.play_sound(self.click_sound, volume=int(self.settings_sound_slider_text.text.split()[-1]) / 100)
        self.window.show_view(Select_level_View(1600, 900))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.PAGEUP:
            self.window.show_view(Select_level_View(1600, 900)) 

    def on_hide_view(self):
        arcade.stop_sound(self.background_player)

    def on_show_view(self):
        self.background_player = arcade.play_sound(self.background_music, int(self.settings_music_slider_text.text.split()[-1]) / 100, loop=True)

    def quit_from_game(self, event=None):
        self.window.close()
