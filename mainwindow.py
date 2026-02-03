import arcade
from menuwindow import Menu_View

if __name__ == "__main__":
    window = arcade.Window(1600, 900, "Game", fullscreen=True)
    window.show_view(Menu_View(1600, 900))
    arcade.run()