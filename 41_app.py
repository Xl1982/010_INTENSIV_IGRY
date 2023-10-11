import pygame
from pygame import sprite, Surface, Color, QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP


class PlatformerGame():
    def __init__(self):
        self.WIN_WIDTH = 800
        self.WIN_HEIGHT = 640
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.BACKGROUND_COLOR = "#004400"
        self.PLATFORM_WIDTH = 32
        self.PLATFORM_HEIGHT = 32
        self.PLATFORM_COLOR = "#FF6262"
        self.MOVE_SPEED = 7
        self.WIDTH = 22
        self.HEIGHT = 32
        self.COLOR = "#888888"
        self.JUMP_POWER = 10
        self.GRAVITY = 0.35
        self.level = [
            "___________",
            "_         _",
            "_         _",
            "___________",
        ]

        self.hero = self.Player(55, 55, self)
        self.left = self.right = self.up = False # инициализация направления движения

        self.entities = pygame.sprite.Group()
        self.platforms = []
        self.entities.add(self.hero)

        pygame.init()

        #создание окна игры
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption('Платформер')

        #установка цвета фона
        self.bg = Surface((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.bg.fill(Color(self.BACKGROUND_COLOR))

    class Player(sprite.Sprite):
        def __init__(self, x, y, game):
            sprite.Sprite.__init__(self)
            self.game = game
            self.yvel = 0
            self.onGround = False
            self.xvel = 0
            self.startX = x
            self.startY = y
            self.image = Surface((self.game.WIDTH, self.game.HEIGHT))
            self.image.fill(Color(self.game.COLOR))
            self.rect = pygame.Rect(x, y, self.game.WIDTH, self.game.HEIGHT)


        def update(self, left, right, up, platforms):
            if up:
                if self.onGround:
                    self.yvel = -self.game.JUMP_POWER

            if left:
                self.xvel = -self.game.MOVE_SPEED
            if right:
                self.xvel = self.game.MOVE_SPEED

            if not self.onGround:
                self.yvel += self.game.GRAVITY

            self.onGround = False
            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)
            self.rect.x += self.xvel

        def collide(self, xvel, yvel, platforms):
            for p in platforms:
                if sprite.collide_rect(self, p):
                    if xvel > 0:
                        self.rect.right = p.rect.left
                    if xvel < 0:
                        self.rect.left = p.rect.right
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0



    class Platform(sprite.Sprite):
        def __init__(self, x, y, game):
            sprite.Sprite.__init__(self)
            self.image = Surface((game.PLATFORM_WIDTH, game.PLATFORM_HEIGHT ))
            self.image.fill(Color(game.PLATFORM_COLOR))
            self.rect = pygame.Rect(x, y, game.PLATFORM_WIDTH, game.PLATFORM_HEIGHT)

    def create_level(self): # функция которая обходит через цикл фор list открывая строки а потом, столбцы
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "_":
                    # создание платформы и ее добавление в сп иски
                    pf = self.Platform(x, y, self)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                x += self.PLATFORM_WIDTH # переход к следующему блоку
            y += self.PLATFORM_HEIGHT
            x = 0

    def run(self):
        timer = pygame.time.Clock()
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    raise SystemExit("QUIT")
                if e.type == KEYDOWN and e.key == K_UP:
                    self.up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    self.left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    self.right = True

                if e.type == KEYUP and e.key == K_UP:
                    self.up = False
                if e.type == KEYUP and e.key == K_LEFT:
                    self.left = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    self.right = False

            self.screen.blit(self.bg, (0, 0))
            self.hero.update(self.left, self.right, self.up, self.platforms)
            self.entities.draw(self.screen)
            pygame.display.update()
            timer.tick(60)

if __name__ == "__main__":
    game = PlatformerGame()
    game.create_level()
    game.run()


