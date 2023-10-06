import arcade
import pymunk
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'Light'

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width,height, title)

        self.space = pymunk.Space()
        self.space.gravity = (0, -900)
        self.shapes = []
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()

        for shape in self.shapes:
            pos_x = shape.body.position.x
            pos_y = shape.body.position.y
            arcade.draw_circle_filled(pos_x, pos_y, shape.radius, arcade.color.ROSE)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
            mass = 1
            radius = 20
            moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
            body = pymunk.Body(mass, moment)
            body.position = x, y
            shape = pymunk.Circle(body, radius, (0, 0))
            self.space.add(body, shape)
            self.shapes.append(shape)

    def update(self, delta_time: float):
            self.space.step(delta_time)

if __name__ == "__main__":
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()