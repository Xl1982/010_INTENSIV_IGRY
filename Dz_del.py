import arcade
import time
import arcade.gui
from arcade.experimental.lights import Light, LightLayer
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Игрушка"
SPRITE_SCALING_PLAYER = 1
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING_PLAYER)

#cветик
VIEWPORT_MARGIN = 200
AMBIENT_COLOR = (10, 10, 10)



DEAD_ZONE=0.1
RIGHT_FACING=0
LEFT_FACING=1
DISTANCE_TO_CHANGE_TEXTURE=20

TILE_SCALING = 0.5

#монеточка
COIN_COUNT = 1



#гравитация
GRAVITY = 2000

DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

PLAYER_FRICTION = 9
WALL_FRICTION = 99
DYNAMIC_ITEM_FRICTION = 99

PLAYER_MASS = 2.0

PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600
PLAYER_MOVE_FORCE_ON_GROUND = 8000
PLAYER_JUMP_IMPULSE = 1800



class MenuView(arcade.View):
    def on_show_view(self):
        self.set_mouse_visible = True
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.GRAY)
        self.v_box = arcade.gui.UIBoxLayout()
        start_button = arcade.gui.UIFlatButton(text="Начать игру", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Выход", width=200)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_click_start
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()
    def on_click_start(self, event):
        game_view = GameView()
        self.window.show_view(game_view)
        self.manager.disable()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()
class PlayerSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = SPRITE_SCALING_PLAYER
        main_path =":resources:images/animated_characters/male_person/malePerson"
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.x_odometer = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -DEAD_ZONE and self.character_face_direction ==RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction ==LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        is_on_ground = physics_engine.is_on_ground(self)
        self.x_odometer += dx
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class GameOverView(arcade.View):
    def on_show_view(self):
        self.set_mouse_visible = True
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.v_box = arcade.gui.UIBoxLayout()
        over_button = arcade.gui.UIFlatButton(text="Вы проиграли - кликните для выхода в меню!", width=2000)
        self.v_box.add(over_button.with_space_around(bottom=20))
        over_button.on_click = self.on_click_over
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
    def on_draw(self):
        self.clear()
        self.manager.draw()


    def on_click_over(self, event):
        game_view = MenuView()
        self.window.show_view(game_view)

class GameWinView(arcade.View):
        def on_show_view(self):

            arcade.set_background_color(arcade.color.GLAUCOUS)

        def on_draw(self):
            self.clear()
            arcade.draw_text("Вы выиграли - кликните для выхода в меню!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.WHITE, 30, anchor_x="center", )

        def on_mouse_press(self, _x, _y, _button, _modifiers):
            game_view = MenuView()
            self.window.show_view(game_view)



class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.background_sprite_list = None
        self.view_left = 0
        self.view_bottom = 0
        self.light_layer = None
        self.player_light = None
        self.set_mouse_visible = False
        self.manager = arcade.gui.UIManager()
        self.manager.disable()
        self.health = 100
        self.score = 0
        self.player = None
        self.money = arcade.sound.load_sound(":resources:sounds/coin5.wav")
        self.death = arcade.sound.load_sound(":resources:sounds/gameover2.wav")
        self.jump = arcade.sound.load_sound(":resources:sounds/jump1.wav")
        self.coin_list = None
        self.enemy_list = None
        self.game_over = False
        self.player_sprite = PlayerSprite()
        self.player_list = None
        self.left_pressed = False
        self.right_pressed = False
        self.physics_engine = None
        self.enemy = None
        self.enemy_list = None
        self.game = True


    def on_show_view(self):
        self.setup()

    def setup(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.score = 0
        self.health = 100
        self.background_sprite_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()

        arcade.set_background_color(arcade.color.BABY_BLUE)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.box_list = arcade.SpriteList(use_spatial_hash=True)
        coordinate_list = [[512, 350], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                                               TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)

        coordinate_list = [[450, 350], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)

        coordinate_list = [[650, 500], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)

        coordinate_list = [[710, 500], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)
        coordinate_list = [[770, 500], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)
        coordinate_list = [[230, 160], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)

        coordinate_list = [[290, 160], ]
        for coordinate in coordinate_list:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                TILE_SCALING)
            box.position = coordinate
            self.wall_list.append(box)

        for x in range(0, 600, 95):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 SPRITE_SCALING_PLAYER)
            wall.center_x = 1
            wall.center_y = x
            self.wall_list.append(wall)

        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING_PLAYER)
            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=GRAVITY)
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/gold_1.png",
                                 scale=0.8)
            coin.center_x = 770
            coin.center_y = 570
            self.coin_list.append(coin)
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/gold_1.png",
                                 scale=0.8)
            coin.center_x = 500
            coin.center_y = 420
            self.coin_list.append(coin)
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/gold_1.png",
                                 scale=0.8)
            coin.center_x = 250
            coin.center_y = 230
            self.coin_list.append(coin)
        enemy = arcade.Sprite(":resources:images/enemies/bee.png", scale=0.8)

        enemy.bottom = 150
        enemy.left = SPRITE_SIZE * 2.7
        enemy.change_x = 2
        self.enemy_list.append(enemy)

        grid_y = 1
        self.player_list = arcade.SpriteList()
        self.player_sprite.center_x = 150
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        self.player_list.append(self.player_sprite)

        sprite = arcade.Sprite(":resources:images/backgrounds/stars.png")
        sprite.position = 550, 500
        self.background_sprite_list.append(sprite)

        radius = 150
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(0, 0, radius, color, mode)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.view_left = 0
        self.view_bottom = 0
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.light_layer.set_background_color(arcade.color.BLACK)
        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITY)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.enemy_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="enemy")


        def item_hit_handler(player, item_sprite, _arbiter, _space, _data):
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("player", "item", post_handler=item_hit_handler)

        def enemy_hit_handler(player, enemy, _arbiter, _space, _data):
           t = time.time()
           if time.time() - t <=1:
               t = time.time()
               self.health -= 1

        self.physics_engine.add_collision_handler("player", "enemy", post_handler=enemy_hit_handler)

    def on_draw(self):
        self.clear()
        with self.light_layer:
            self.background_sprite_list.draw()
            self.coin_list.draw()
            self.wall_list.draw()
            self.box_list.draw()
            self.enemy_list.draw()
            self.player_list.draw()
        self.light_layer.draw(ambient_color=AMBIENT_COLOR)
        arcade.draw_text("Нажмите SPACE чтобы вкл/выкл свет",
                         250 + self.view_left, 40 + self.view_bottom,
                         arcade.color.WHITE, 20)

        score_text = f"Монеты: {self.score}"
        arcade.draw_text(score_text,
                         start_x=10,
                         start_y=10,
                         color=arcade.csscolor.WHITE,
                         font_size=18)
        health_text = f"Жизни: {self.health} % "
        arcade.draw_text(health_text,
                         start_x=10,
                         start_y=40,
                         color=arcade.csscolor.RED,
                         font_size=18)
    def on_resize(self, width, height):

        self.light_layer.resize(width, height)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            if self.physics_engine.is_on_ground(self.player_sprite):
                impulse = (0, PLAYER_JUMP_IMPULSE)
                arcade.sound.play_sound(self.jump)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
        elif key == arcade.key.SPACE:
            if self.player_light in self.light_layer:
                self.light_layer.remove(self.player_light)
            else:
                self.light_layer.add(self.player_light)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


    def on_update(self, delta_time):

            if self.game:
                self.player_light.position = self.player_sprite.position
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
                for coin in hit_list:
                    self.score += 1
                    coin.remove_from_sprite_lists()
                    arcade.sound.play_sound(self.money)
                if self.left_pressed and not self.right_pressed:
                    force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
                    self.physics_engine.apply_force(self.player_sprite, force)
                    self.physics_engine.set_friction(self.player_sprite, 0)
                elif self.right_pressed and not self.left_pressed:
                    force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
                    self.physics_engine.apply_force(self.player_sprite, force)
                    self.physics_engine.set_friction(self.player_sprite, 0)
                else:
                    self.physics_engine.set_friction(self.player_sprite, 1.0)
                self.physics_engine.step()
                if self.health == 1:
                    self.player_sprite.center_x = 150
                    self.player_sprite.center_y = SPRITE_SIZE * 1 + SPRITE_SIZE / 2


            if self.health == 0:
                    arcade.sound.play_sound(self.death)
                    game_over = GameOverView()
                    self.window.show_view(game_over)
                    return


            if len(self.coin_list) == 0:
                view = GameWinView()
                self.window.show_view(view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()