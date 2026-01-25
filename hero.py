import arcade

screen_width = 1600
screen_height= 900


class Hero(arcade.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        
        # Основные характеристики
        self.scale = 1.0
        self.speed = 300
        self.health = 3
        
        # Загрузка текстур
        self.texture = arcade.load_texture("images/hero.png")
        
        # Жёстко ставим персонажа в центр экрана (лучше передавать позицию в __init__)
        self.center_x = start_x
        self.center_y = start_y
        
    def update(self, dt):
        """ Перемещение персонажа """
        self.center_x += 50 * dt
        print(dt)
        self.center_y += 50 * dt
        
        # Ограничение в пределах экрана
        self.center_x = max(self.width/2, min(screen_width - self.width/2, self.center_x))
        self.center_y = max(self.height/2, min(screen_height - self.height/2, self.center_y))