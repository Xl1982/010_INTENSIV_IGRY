import pygame
from random import randint
from time import sleep
from pygame.locals import *

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
SIZE = 500, 200
pygame.init()
screen = pygame.display.set_mode(SIZE)
running = True
rect = Rect(100, 50, 50, 50)
n = 500
def random_point():
    x = randint(0, SIZE[0])
    y = randint(0, SIZE[1])
    return (x, y)
def random_rects(n):
    rects = []
    for i in range(n):
        r = Rect(random_point(), (10, 20))
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
