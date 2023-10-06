import arcade

# движение камеры подсмотрела
TILE_SCALING = 0.5
PLAYER_SCALING = 1
ENEMY_SCALING = 0.2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'platformer'
SPRITE_SIZE = 128
GRID_SIZE = SPRITE_SIZE * TILE_SCALING

VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

MOVEMENT_SPEED = 5
JUMP_SPEED = 23
GRAVITY = 1.1


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.wall_list = None
        self.enemy1 = None
        self.enemy3 = None
        self.enemy2 = None
        self.enemy_list = None
        self.coin_list = None
        self.score = 0
        self.player_sprite = None
        self.physics_engine = None
        self.end_of_map = 0
        self.game_over = False
        self.win = False
        self.camera = None
        self.gui_camera = None

    def setup(self):
        self.enemy_list = arcade.SpriteList()

        self.enemy1 = arcade.Sprite(':resources:images/tiles/bomb.png', ENEMY_SCALING)
        self.enemy2 = arcade.Sprite(':resources:images/tiles/bomb.png', ENEMY_SCALING)
        self.enemy3 = arcade.Sprite(':resources:images/tiles/bomb.png', ENEMY_SCALING)

        self.enemy1.center_x = 500
        self.enemy1.center_y = 100
        self.enemy2.center_x = 1900
        self.enemy2.center_y = 100
        self.enemy3.center_x = 2500
        self.enemy3.center_y = 100

        self.enemy_list.append(self.enemy2)
        self.enemy_list.append(self.enemy1)
        self.enemy_list.append(self.enemy3)
        # с листом врагов отказалась работать коллизия((
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png',
                                           PLAYER_SCALING)
        self.player_sprite.center_x = 196
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite)

        map_name = ':resources:/tiled_maps/map.json'
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.end_of_map = self.tile_map.width * GRID_SIZE
        self.wall_list = self.tile_map.sprite_lists['Platforms']
        self.coin_list = self.tile_map.sprite_lists['Coins']
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        walls = [self.wall_list]

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, walls, gravity_constant=GRAVITY)
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pan_camera_to_user()

        self.game_over = False

    def on_draw(self):
        self.camera.use()
        self.clear()
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.gui_camera.use()
        if self.game_over:
            arcade.draw_text('Game Over', 200, 200, arcade.color.BLACK, 30)
        if self.win:
            arcade.draw_text('You Win', 200, 200, arcade.color.BLACK, 30)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        if self.player_sprite.right >= self.end_of_map:
            self.game_over = True
        if self.player_sprite.center_y <= 100:
            self.game_over = True
        if not self.game_over:
            self.physics_engine.update()
        if arcade.check_for_collision(self.player_sprite, self.enemy1) == True:
            self.game_over = True
        if arcade.check_for_collision(self.player_sprite, self.enemy2) == True:
            self.game_over = True
        if arcade.check_for_collision(self.player_sprite, self.enemy3) == True:
            self.game_over = True
        coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1
        if self.score == 4:
            self.win = True
        self.pan_camera_to_user(panning_fraction=0.12)

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_center = screen_center_x, screen_center_y
        self.camera.move_to(user_center, panning_fraction)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()

