import arcade

WIDTH = 888
HEIGHT = 800
PLAYER_MOVEMENT_SPEED = 5
JUMP = 30
GRAVITY = 2

class Defeat(arcade.View):
    def __init__(self):
        super().__init__()
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        self.clear()
        arcade.draw_text("DEFEAT!!!", self.window.width//2 - 100, self.window.height//2, arcade.color.RED,font_size=25,font_name="Kenney Blocks")


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((0, 100, 150))

        self.player = None  # СЃРѕР·РґР°РµРј РїСѓСЃС‚СѓСЋ РїРµСЂРµРјРµРЅРЅСѓСЋ РґР»СЏ РїРµСЂСЃРѕРЅР°Р¶Р°
        self.player_list = None  # СЃРѕР·РґР°РµРј РїСѓСЃС‚СѓСЋ РїРµСЂРµРјРµРЅРЅСѓСЋ РґР»СЏ СЃРїРёСЃРєР° РїРµСЂСЃРѕРЅР°Р¶РµР№ (РЅР° Р±СѓРґСѓС‰РµРµ, РґР»СЏ Р°РЅРёРјР°С†РёР№)
        self.ground = None  # СЃРѕР·РґР°РµРј РїСѓСЃС‚СѓСЋ РїРµСЂРµРјРµРЅРЅСѓСЋ РґР»СЏ Р·РµРјР»Рё
        self.ground_list = None  # СЃРѕР·РґРµРј РїСѓСЃС‚СѓСЋ РїРµСЂРµРјРµРЅСѓСЋ РґР»СЏ СЃРїРёСЃРєР° Р·РµРјР»Рё
        self.box = None
        self.box_list = None
        self.box_list_coords = [[512, 96], [256, 96], [768, 96], [1000, 96], [1200, 96], [1500, 96]]
        self.physics_engine = None
        self.camera = None
        self.enemy = None
        self.exit_player = None

    def setup(self):
        self.player = Player()  # СЃРѕР·РґР°РµРј РїРµСЂСЃРѕРЅР°Р¶Р°
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite("Player", self.player)
        self.player_list = arcade.SpriteList()  # СЃРѕР·РґР°РµРј СЃРїРёСЃРѕРє РґР»СЏ РїРµСЂСЃРѕРЅР°Р¶Р°
        self.player_list.append(self.player)  # РґРѕР±Р°РІР»СЏРµРј РїРµСЂСЃРѕРЅР°Р¶Р° РІ СЃРїРёСЃРѕРє
        self.ground_list = arcade.SpriteList()  # СЃРѕР·РґР°РµРј СЃРїРёСЃРѕРє РґР»СЏ Р·РµРјР»Рё
        self.box_list = arcade.SpriteList()
        self.camera = arcade.Camera(self.window.width, self.window.height)
        enemy_sprite = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.enemy = arcade.Sprite(enemy_sprite, 1)
        self.enemy.center_x = 333
        self.enemy.center_y = 128
        self.scene.add_sprite("Enemy", self.enemy)
        exit_sprite = ":resources:images/tiles/signExit.png"
        self.exit_player = arcade.Sprite(exit_sprite, 1)
        self.exit_player.center_x = 666
        self.exit_player.center_y = 128
        self.scene.add_sprite("Exit", self.exit_player)

        for i in range(0, 5000, 128):
            self.ground = arcade.Sprite(':resources:images/tiles/grassMid.png', scale=1)  # СЃРѕР·РґР°РµРј Р·РµРјР»СЋ
            self.ground.center_x = i
            self.ground.center_y = 32
            self.ground_list.append(self.ground)  # РґРѕР±Р°РІР»СЏРµРј Р·РµРјР»СЋ РІ СЃРїРёСЃРѕРє
            self.scene.add_sprite("Walls", self.ground)

        for i in self.box_list_coords:
            self.box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=1)
            self.box.position = i
            self.box_list.append(self.box)
            self.scene.add_sprite("Walls", self.box)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.camera.use()

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
                self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_player()

        if arcade.check_for_collision(self.player, self.enemy):
            self.player.kill()
            defeat = Defeat()
            window.show_view(defeat)

        if arcade.check_for_collision(self.player, self.exit_player):
            arcade.close_window()
            print('Р’С‹ РїРѕР±РµРґРёР»Рё')

    def on_key_press(self, symbol: int, modifiers: int):  # Р»РѕРІРёС‚ РЅР°Р¶Р°С‚РёСЏ РєР»Р°РІРёС€
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED  # РёР·РјРµРЅРµРЅРёРµ РїРѕ РѕСЃРё X = 3
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED  # РёР·РјРµРЅРµРЅРёРµ РїРѕ РѕСЃРё X = -3
        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP

    def on_key_release(self, symbol: int, modifiers: int):  # Р»РѕРІРёС‚ РѕС‚РїСѓСЃРєР°РЅРёСЏ РєР»Р°РІРёС€
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 0  # РёР·РјРµРЅРµРЅРёРµ РїРѕ РѕСЃРё X = 0
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = 0  # РёР·РјРµРЅРµРЅРёРµ РїРѕ РѕСЃРё X = 0
        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = 0  # РёР·РјРµРЅРµРЅРёРµ РїРѕ РѕСЃРё Y = 0


class Player(arcade.Sprite):  # РЅР°СЃР»РµРґСѓРµРјСЃСЏ РѕС‚ РєР»Р°СЃСЃР° РЎРїСЂР°Р№С‚
    def __init__(self):
        super().__init__(':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png', scale=1)
        self.center_x = 122
        self.center_y = 555


window = arcade.Window(WIDTH,HEIGHT)
my_game = MyGame()
my_game.setup()
window.show_view(my_game)
arcade.run()
