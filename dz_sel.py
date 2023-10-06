import arcade
import arcade.sound

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "q"

CHARACTER_SCALE = 0.5
CHARACTER_JUMP_SPEED = 30
CHARACTER_MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def on_draw(self):
        arcade.start_render()

    def on_key_press(self, key, modifiers):
        arcade.play_sound(self.sound)
        self.jump_sound = arcade.sound(":resources/sounds/jump2.wav")
        self.character = None
        self.k_list = None
        self.enemy_list = None

        self.physics_engine = None


    def setup(self):
        self.character = arcade.Sprite(":resources:images/enemies/slimeBlock.png")
        self.character.center_x = 100
        self.character.center_y = 500

        self.k_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        for i in range(10):
            korobka = arcade.Sprite(":resources:images/tiles/boxCrate_double.png")
            korobka.center_x = i * 100 + 40
            korobka.center_y = 40
            self.k_list.append(korobka)

        for i in range(5):
            enemy = arcade.Sprite(":resources:images/enemies/slimePurple.png")
            enemy.center_x = i * 300 + 5
            enemy.center_y = 170
            self.enemy_list.append(enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.character, self.k_list, gravity_constant=1.0)

    def on_draw(self):
        arcade.start_render()

        self.k_list.draw()
        self.enemy_list.draw()
        self.character.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

        coins_hit_list = arcade.check_for_collision_with_list(
            self.character, self.k_list)

        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()

        enemies_hit_list = arcade.check_for_collision_with_list(
            self.character, self.enemy_list)

        if enemies_hit_list:
            arcade.close_window()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.character.change_y = CHARACTER_JUMP_SPEED
                if key == arcade.key.SPACE:
                    arcade.sound()
        elif key == arcade.key.LEFT:
            self.character.change_x = -CHARACTER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.character.change_x = CHARACTER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.character.change_x = 0


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()