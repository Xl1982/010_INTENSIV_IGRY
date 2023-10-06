import pygame
from random import randint
from time import sleep
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

running = True
rect = Rect(100, 50, 50, 50)
n = 50

def random_point():
    x = randint(0, SIZE[0])
    y = randint(0, SIZE[1])
    return (x, y)

def random_rects(n):
    rects = []
    for i in range(n):
        r = Rect(random_point(), (20, 20))
        rects.append(r)
    return rects

rects = random_rects(n)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_r:
                rects = random_rects(n)

    screen.fill(GRAY)
    pygame.draw.rect(screen, GREEN, rect, 1)

    for r in rects:
        if rect.colliderect(r):
            pygame.draw.circle(screen, RED, r.center, 2)
        else:
            pygame.draw.circle(screen, BLUE, r.center, 1)
    pygame.display.flip()

pygame.quit()
