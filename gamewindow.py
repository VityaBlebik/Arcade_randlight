import arcade

from pyglet.graphics import Batch

DEFAULT_FONT_SIZE = 40
SCREEN_TITLE = "Rosetta Stone"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, lines, colors, font_size):
        super().__init__(width, height, title)
        self.batch = Batch()
        ...

    def on_draw(self):
        self.clear()
        ...


def setup_game(width=600, height=400, title="Rosetta", lines=None, colors=None, font_size=40):
    lines = lines or ["Ροζέτα Στόουν", "Rosetta stone", "حجر رشيد"]
    colors = colors or [[255, 3, 62], [153, 102, 204], [164, 198, 57]]

    game = MyGame(width, height, title, lines, colors, font_size)
    return game


def main():
    setup_game(
        600, 400, SCREEN_TITLE, ["Ροζέτα Στόουν", "Rosetta stone", "حجر رشيد"],
        [[255, 3, 62], [153, 102, 204], [164, 198, 57]], DEFAULT_FONT_SIZE
    )
    arcade.run()


if __name__ == "__main__":
    main()