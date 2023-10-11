import pygame
from pygame import QUIT, K_RIGHT, K_LEFT

SIZE = WIDTH, HEIGHT = 600, 400
BACKGROUND_COLOR = pygame.Color('white')
FPS = 10
is_walk = False
left = right = False
MOVE_SPEED = 7

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
        self.xvel = 0
        self.images = []
        self.images.append(pygame.image.load('resources/images/walk1.png'))
        self.images.append(pygame.image.load('resources/images/walk2.png'))
        self.images.append(pygame.image.load('resources/images/walk3.png'))
        self.images.append(pygame.image.load('resources/images/walk4.png'))
        self.images.append(pygame.image.load('resources/images/walk5.png'))
        self.images.append(pygame.image.load('resources/images/walk6.png'))
        self.images.append(pygame.image.load('resources/images/walk7.png'))
        self.images.append(pygame.image.load('resources/images/walk8.png'))
        self.images.append(pygame.image.load('resources/images/walk9.png'))
        self.images.append(pygame.image.load('resources/images/walk10.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 150, 198)

    def update(self):
        if is_walk:
            self.rect.x += self.xvel
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        if left:
            self.xvel = -MOVE_SPEED
            self.image = pygame.transform.flip(self.image, True, False)

        if right:
            self.xvel = MOVE_SPEED

        if not (left or right):
                self.xvel = 0


def main():
       global is_walk
       global right, left
       pygame.init()
       screen = pygame.display.set_mode(SIZE)
       my_sprite = MySprite()
       my_group = pygame.sprite.Group(my_sprite)
       clock = pygame.time.Clock()
       while True:
           for event in pygame.event.get():
               if event.type == QUIT:
                   raise SystemExit

               elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                   left = True
                   is_walk = True

               elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                   right = True
                   is_walk = True

               elif event.type == pygame.KEYUP and event.key == K_RIGHT:
                   left = False
                   is_walk = False

               elif event.type == pygame.KEYUP and event.key == K_LEFT:
                   right = False
                   is_walk = False

           my_group.update()
           screen.fill(BACKGROUND_COLOR)
           my_group.draw(screen)
           pygame.display.update()
           clock.tick(10)


if __name__ == '__main__':
   main()
