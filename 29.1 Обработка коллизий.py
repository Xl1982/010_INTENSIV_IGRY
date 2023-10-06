import random
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Космический шутер'

SPRITE_SCALING_LASER = 0.3
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 1

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/playerShip1_blue.png', SPRITE_SCALING_PLAYER)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        

class Laser(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/laserBlue01.png', SPRITE_SCALING_LASER, angle=90)
        self.change_y = 2


        def update(self):
            self.center_y += self.change_y
            if self.bottom >= SCREEN_HEIGHT:
                self.kill()
                
                
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/playerShip3_orange.png', SPRITE_SCALING_ENEMY, angle=180)
        self.change_y = 1 
        
    def update(self):
        self.center_y -= self.change_y
        
        
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_texture = arcade.load_texture(':resources:images/backgrounds/stars.png')

        self.player_sprite = None
        self.set_mouse_visible(False)

        self.player_sprite = None
        self.player_sprite_list = None

        self.enemy_sprite = None
        self.laser_sprite_list = None
        self.status = True

    def setup(self):
        self.player_sprite = Player()
        self.laser_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList()

        for _ in range(1, 31):
            self.enemy_sprite = Enemy()
            self.enemy_sprite.center_x = random.randint(0, SCREEN_WIDTH)
            self.enemy_sprite.center_y = SCREEN_HEIGHT + _ * 50
            self.enemy_sprite_list.append(self.enemy_sprite)


    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background_texture)

        self.player_sprite.draw()
        self.laser_sprite_list.draw()
        self.enemy_sprite_list.draw()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.status:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y
            if self.player_sprite.center_y >= SCREEN_HEIGHT / 2:
                self.player_sprite.center_y = SCREEN_HEIGHT / 2

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.status:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.laser_sprite = Laser()
                self.laser_sprite.bottom = self.player_sprite.top
                self.laser_sprite.center_x = self.player_sprite.center_x
                self.laser_sprite_list.append(self.laser_sprite)


    def on_update(self, delta_time: float):
        if self.status:
            self.laser_sprite_list.update()
            self.enemy_sprite_list.update()
            for laser in self.laser_sprite_list:
                shot_list = arcade.check_for_collision_with_list(laser, self.enemy_sprite_list)
                if shot_list:
                    laser.kill()
                    for enemy in shot_list:
                        enemy.kill()
        if not self.enemy_sprite_list:
            self.status = False

def main():
    game = Game()
    game.setup()
    arcade.run()

main()