import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз


class Player(sprite.Sprite):
   def __init__(self, x, y):
       sprite.Sprite.__init__(self)
       self.yvel = 0  # скорость вертикального перемещения
       self.onGround = False  # На земле ли я?
       self.xvel = 0  # скорость перемещения. 0 - стоять на месте
       self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
       self.startY = y
       self.image = Surface((WIDTH, HEIGHT))
       self.image.fill(Color(COLOR))
       self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

   def update(self, left, right, up, platforms):
       if up:
           if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
               self.yvel = -JUMP_POWER
       if left:
           self.xvel = -MOVE_SPEED  # Лево = x- n

       if right:
           self.xvel = MOVE_SPEED  # Право = x + n

       if not (left or right):  # стоим, когда нет указаний идти
           self.xvel = 0

       if not self.onGround:
           self.yvel += GRAVITY
       self.onGround = False
       self.rect.y += self.yvel
       self.collide(0, self.yvel, platforms)

       self.rect.x += self.xvel
       self.collide(self.xvel, 0, platforms)

   def collide(self, xvel, yvel, platforms):
       for p in platforms:
           if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

               if xvel > 0:  # если движется вправо
                   self.rect.right = p.rect.left  # то не движется вправо

               if xvel < 0:  # если движется влево
                   self.rect.left = p.rect.right  # то не движется влево

               if yvel > 0:  # если падает вниз
                   self.rect.bottom = p.rect.top  # то не падает вниз
                   self.onGround = True  # и становится на что-то твердое
                   self.yvel = 0  # и энергия падения пропадает

               if yvel < 0:  # если движется вверх
                   self.rect.top = p.rect.bottom  # то не движется вверх
                   self.yvel = 0  # и энергия прыжка пропадает


class Platform(sprite.Sprite):
   def __init__(self, x, y):
       sprite.Sprite.__init__(self)
       self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)) #поверхность
       self.image.fill(Color(PLATFORM_COLOR))
       self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def main():
   hero = Player(55, 55)  # создаем героя по (x,y) координатам
   left = right = False  # по умолчанию — стоим
   up = False
   entities = pygame.sprite.Group()  # Все объекты entities-сущности
   platforms = []  # то, во что мы будем врезаться или опираться
   entities.add(hero)

   level = [
       "-------------------------",
       "-                       -",
       "-                       -",
       "-                       -",
       "-            --         -",
       "-                       -",
       "--                      -",
       "-                       -",
       "-                   --- -",
       "-                       -",
       "-                       -",
       "-      ---              -",
       "-                       -",
       "-   -----------         -",
       "-                       -",
       "-                -      -",
       "-                   --  -",
       "-                       -",
       "-                       -",
       "-------------------------"]

   timer = pygame.time.Clock()
   x = y = 0
   # координаты
   for row in level:  # вся строка
       for col in row:  # каждый символ
           if col == "-":
               pf = Platform(x, y)
               entities.add(pf)
               platforms.append(pf)

           x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
       y += PLATFORM_HEIGHT  # то же самое и с высотой
       x = 0
   pygame.init()
   screen = pygame.display.set_mode(DISPLAY)
   pygame.display.set_caption("Платформер")
   bg = Surface((WIN_WIDTH, WIN_HEIGHT))
   bg.fill(Color(BACKGROUND_COLOR))

   while 1:
       timer.tick(60)
       for e in pygame.event.get():
           if e.type == QUIT:
               raise SystemExit

           if e.type == KEYDOWN and e.key == K_LEFT:
               left = True

           if e.type == KEYDOWN and e.key == K_RIGHT:
               right = True

           if e.type == KEYUP and e.key == K_RIGHT:
               right = False
           if e.type == KEYUP and e.key == K_LEFT:
               left = False
           if e.type == KEYDOWN and e.key == K_UP:
               up = True
           if e.type == KEYUP and e.key == K_UP:
               up = False
       screen.blit(bg, (0, 0))

       hero.update(left, right, up, platforms)  # передвижение
       entities.draw(screen)
       pygame.display.update()


if __name__ == "__main__":
   main()
