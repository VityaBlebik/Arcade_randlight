import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Моя Игра"

BACKGROUND_COLOR = arcade.color.GREEN
BUTTON_COLOR = arcade.color.BLUE
TEXT_COLOR = arcade.color.WHITE

class Button:
    def __init__(self, center_x, center_y, width, height, text):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        
        self.left = center_x - width / 2
        self.right = center_x + width / 2
        self.bottom = center_y - height / 2
        self.top = center_y + height / 2
        
    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, 
                                    self.width, self.height, 
                                    BUTTON_COLOR)
        
        arcade.draw_text(self.text, self.center_x, self.center_y,
                        TEXT_COLOR, 20,
                        anchor_x="center", anchor_y="center",
                        font_name="Arial")
        
    def check_click(self, x, y):
        return (self.left < x < self.right and 
                self.bottom < y < self.top)


class MyGame(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        button_width = 200
        button_height = 50
        start_y = SCREEN_HEIGHT // 2
        
        self.level_button = Button(
            SCREEN_WIDTH // 2, 
            start_y + 80, 
            button_width, 
            button_height, 
            "Выбор уровня"
        )
        
        self.settings_button = Button(
            SCREEN_WIDTH // 2, 
            start_y, 
            button_width, 
            button_height, 
            "Настройки"
        )
        
        self.exit_button = Button(
            SCREEN_WIDTH // 2, 
            start_y - 80, 
            button_width, 
            button_height, 
            "Выход"
        )
        
    def setup(self):
        pass
        
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(BACKGROUND_COLOR)
        
        arcade.draw_text("Моя Игра", 
                        SCREEN_WIDTH // 2, 
                        SCREEN_HEIGHT - 100,
                        arcade.color.WHITE, 40,
                        anchor_x="center", anchor_y="center",
                        font_name="Arial", bold=True)
        
        self.level_button.draw()
        self.settings_button.draw()
        self.exit_button.draw()
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.level_button.check_click(x, y):
                print("Нажата кнопка: Выбор уровня")
                
            elif self.settings_button.check_click(x, y):
                print("Нажата кнопка: Настройки")
                
            elif self.exit_button.check_click(x, y):
                print("Нажата кнопка: Выход")
                arcade.close_window()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
