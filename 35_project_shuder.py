import math
import arcade
import arcade.sound
from config import *
from arcade import load_texture
import random
import arcade.gui
import time
import math
print("d")
from array import array # для работы с массивами
from dataclasses import dataclass
import arcade
import arcade.gl # подмодуль для работы с open Gl



PARTICLE_COUNT = 1000 # колличество частиц
MIN_FADE_TIME = 0.25
MAX_FADE_TIME = 3.5

@dataclass
class Burst: # класс всплеска частиц
    buffer: arcade.gl.Buffer # вершинный массив объекта для отрисовки
    vao: arcade.gl.geometry # время начала всплеска
    start_time: float # Время начала всплеска

class ParticleBurstApp:
    def __init__(self, context):
        self.ctx = context # функции для графики
        self.burst_list = [] # всплески все, список

        # Load shaders
        self.program = self.ctx.load_program(
            vertex_shader="vertex_shader_v1.glsl",
            fragment_shader="fragment_shader.glsl",
        )
        self.ctx.enable_only(self.ctx.BLEND)

    def emit_burst(self, x, y): #функция для создания всплеска

        def _gen_initial_data(initial_x, initial_y):  # функция для генерации начальных данных для частиц
            for i in range(PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi)
                speed = abs(random.gauss(0, 9)) * 0.01
                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed
                red = random.uniform(0.1, 1.0)
                green = random.uniform(0, red)
                blue = 0
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)

                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        # Transform mouse coordinates to OpenGL coordinates
        x2 = x / SCREEN_WIDTH * 2. - 1.
        y2 = y / SCREEN_HEIGHT * 2. - 1.

        initial_data = _gen_initial_data(x2, y2)
        buffer = self.ctx.buffer(data=array('f', initial_data))

        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         '2f 2f 3f f',
                                                         ['in_pos', 'in_vel', 'in_color', 'in_fade_rate'])
        vao = self.ctx.geometry([buffer_description])
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)

    def draw(self):
        for burst in self.burst_list:
            self.program['time'] = time.time() - burst.start_time
            burst.vao.render(self.program, mode=self.ctx.POINTS)

    def update(self):
        temp_list = self.burst_list.copy()
        for burst in temp_list:
            if time.time() - burst.start_time > MAX_FADE_TIME:
                self.burst_list.remove(burst)




class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="START", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        start_button.on_click = self.start_game

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)

        )

    def start_game(self, _):
        game_view = GameplayView()
        game_view.setup()
        self.window.show_view(game_view)



    def on_show(self): # эту фунцкцию мы запускаем при показе этого экрана
        arcade.set_background_color(arcade.color.AMAZON)
        self.ui_manager.enable()

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.draw()

    def on_hide_view(self):
        self.ui_manager.disable()


class BulletSprite(arcade.SpriteSolidColor):
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.center_y < -100:
            self.remove_from_sprite_lists()


class PlayerSprite(arcade.Sprite):
   def __init__(self):
       super().__init__()

       self.scale = SPRITE_SCALING_PLAYER

       main_path = ":resources:images/animated_characters/female_person/femalePerson"

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


class GameOverView(arcade.View):
   def __init__(self, message):
        super().__init__()
        self.message = message

   def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

   def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.message, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x='center')
        arcade.draw_text('Для перезапуска нажмите R', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                         arcade.color.WHITE, font_size=20, anchor_x='center')

   def on_key_press(self, key, modifiers: int):
        if key == arcade.key.R:
            game_view = GameplayView()
            game_view.setup()
            self.window.show_view(game_view)




   def pymunk_moved(self, physics_engine, dx, dy, d_angle):
       if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
           self.character_face_direction = LEFT_FACING
       elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
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


class GameplayView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.bullet_list = None
        self.item_list = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False  # <-- Добавлено для прыжка
        arcade.set_background_color(arcade.color.AMAZON)
        self.physics_engine = None
        self.moving_sprites_list = None
        self.particle_burst = ParticleBurstApp(self.window.ctx)

        self.background_music = arcade.sound.load_sound('barbariki.mp3')
        self.background_music_sound = arcade.sound.play_sound(self.background_music, 0.1)

    def check_game_over(self):
        """Проверка условий победы и поражения"""
        if len(self.item_list) == 0:
            self.end_game('Победа')
            arcade.sound.stop_sound(self.background_music_sound)

    def end_game(self, message):
        """Закончить игру сообщением"""
        game_over_view = GameOverView(message)
        self.window.show_view(game_over_view)
        arcade.sound.stop_sound(self.background_music_sound)

    def setup(self):
       self.player_list = arcade.SpriteList()
       self.bullet_list = arcade.SpriteList()
       map_name = ":resources:/tiled_maps/pymunk_test_map.json"
       tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)
       print(tile_map.sprite_lists)
       self.wall_list = tile_map.sprite_lists["Platforms"]
       self.item_list = tile_map.sprite_lists["Dynamic Items"]
       self.player_sprite = PlayerSprite()

       self.player_sprite.center_x = SPRITE_SIZE + SPRITE_SIZE / 2
       self.player_sprite.center_y = SPRITE_SIZE + SPRITE_SIZE / 2
       self.player_list.append(self.player_sprite)
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
       self.physics_engine.add_sprite_list(self.item_list,
                                           friction=DYNAMIC_ITEM_FRICTION,
                                           collision_type="item")

       def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
           bullet_sprite.remove_from_sprite_lists()

       self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

       def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
           bullet_sprite.remove_from_sprite_lists()
           item_sprite.remove_from_sprite_lists()
           self.particle_burst.emit_burst(item_sprite.center_x, item_sprite.center_y)

       self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)
       self.moving_sprites_list = tile_map.sprite_lists['Moving Platforms']
       self.physics_engine.add_sprite_list(self.moving_sprites_list,
                                           body_type=arcade.PymunkPhysicsEngine.KINEMATIC)



       def player_item_collision_handler(player_sprite, item_sprite, _arbiter, _space, _data):
           item_sprite.remove_from_sprite_lists()
           self.end_game('Поражение')


       self.physics_engine.add_collision_handler('player', 'item', post_handler=player_item_collision_handler)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:  # <-- Добавлено для прыжка
            self.up_pressed = True


    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:  # <-- Добавлено для прыжка
            self.up_pressed = False

    def on_update(self, delta_time):
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

        if self.up_pressed and self.physics_engine.is_on_ground(self.player_sprite):
            force = (0, PLAYER_JUMP_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.up_pressed = False

        self.physics_engine.step()
        self.particle_burst.update()
        self.check_game_over()

    def on_draw(self):
       self.clear()
       self.wall_list.draw()
       self.item_list.draw()
       self.bullet_list.draw()
       self.player_list.draw()
       self.moving_sprites_list.draw()
       self.particle_burst.draw()

    def on_mouse_press(self, x, y, button, modifiers):
       bullet = BulletSprite(20, 5, arcade.color.DARK_YELLOW)
       self.bullet_list.append(bullet)
       start_x = self.player_sprite.center_x
       start_y = self.player_sprite.center_y
       bullet.position = self.player_sprite.position

       dest_x = x
       dest_y = y

       x_diff = dest_x - start_x
       y_diff = dest_y - start_y
       angle = math.atan2(y_diff, x_diff)

       size = max(self.player_sprite.width, self.player_sprite.height) / 2

       bullet.center_x += size * math.cos(angle)
       bullet.center_y += size * math.sin(angle)
       bullet.angle = math.degrees(angle)

       bullet_gravity = (0, -BULLET_GRAVITY)

       self.physics_engine.add_sprite(bullet,
                                      mass=BULLET_MASS,
                                      damping=1.0,
                                      friction=0.6,
                                      collision_type="bullet",
                                      gravity=bullet_gravity,
                                      elasticity=0.9)

       force = (BULLET_MOVE_FORCE, 0)
       print(self.bullet_list)
       self.physics_engine.apply_force(bullet, force)


def main():
   window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
   start_view = StartView()
   window.show_view(start_view)
   arcade.run()


if __name__ == "__main__":
   main()
