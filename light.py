import arcade
class Light(arcade.Sprite):
    def __init__(self, place, status, center_x, center_y):
        super().__init__()
        self.place = place
        self.status = status
        self.center_x = center_x
        self.center_y = center_y
        self.change_texture(self.status, self.place)
    
    def change_status(self, event):
        self.status *= -1
        self.change_texture(self.status, self.place)
    
    def change_texture(self, status, place):
        if status == 1:
            if place == 0:
                self.texture =  arcade.load_texture("images/light_greenh.png")
            else:
                self.texture =  arcade.load_texture("images/light_greenv.png")
        else:
            if place == 0:
                 self.texture =  arcade.load_texture("images/light_redh.png")
            else:       
                 self.texture = arcade.load_texture( "images/light_redv.png")
