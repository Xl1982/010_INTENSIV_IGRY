import math
import arcade

SCREEN_TITLE = "Использование PyMunk"
SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING_PLAYER = 0.3
SPRITE_SCALING_TILES = 0.3
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT
GRAVITY = 1500
PLAYER_JUMP_FORCE = 35000
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6
PLAYER_MASS = 2.0
PLAYER_MAX_HORIZONTAL_SPEED = 200
PLAYER_MAX_VERTICAL_SPEED = 1600
PLAYER_MOVE_FORCE_ON_GROUND = 9999
DEAD_ZONE = 0.1
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 5
BULLET_MOVE_FORCE = 4500
BULLET_MASS = 0.1
BULLET_GRAVITY = 300



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

