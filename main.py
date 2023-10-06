import arcade

WIN_WIDTH = 800
WIN_HEIGHT = 640
BACKGROUND_COLOR = arcade.csscolor.DIM_GRAY
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = arcade.csscolor.RED
MOVE_SPEED = 7
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 32
PLAYER_COLOR = arcade.csscolor.INDIANRED
JUMP_POWER = 20
GRAVITY = 2

class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.texture = arcade.make_soft_square_texture(PLAYER_WIDTH, PLAYER_COLOR, outer_alpha=255)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0

class Platform(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.texture = arcade.make_soft_square_texture(PLATFORM_WIDTH, PLATFORM_COLOR, outer_alpha=255)
        self.center_x = x
        self.center_y = y

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIN_WIDTH, WIN_HEIGHT, "Platformer with Arcade")

        self.player = None
        self.platform_list = None
        self.physics_engine = None

        arcade.set_background_color(BACKGROUND_COLOR)

    def setup(self):
        self.player = Player(50, 50)
        self.platform_list = arcade.SpriteList()

        level = [
            "-------------------------",
            "-                       -",
            "-                       -",
            "-    ---                -",
            "-      ---              -",
            "-          ---          -",
            "-                 ---   -",
            "-                       -",
            "-       ---             -",
            "-     ---               -",
            "-                       -",
            "-  ---                  -",
            "                        -",
            "-                       -",
            "-------------------------"
        ]

        x = y = 0
        for row in level:
            for col in row:
                if col == "-":
                    platform = Platform(x + PLATFORM_WIDTH / 2, y + PLATFORM_HEIGHT / 2)
                    self.platform_list.append(platform)
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platform_list, gravity_constant=GRAVITY
        )

    def on_draw(self):
        arcade.start_render()
        self.platform_list.draw()
        self.player.draw()

    def update(self, delta_time):
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -MOVE_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVE_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_POWER

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

if __name__ == "__main__":
    window = GameWindow()
    window.setup()
    arcade.run()
