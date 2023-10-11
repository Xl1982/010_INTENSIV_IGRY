from random import randint
from time import sleep

import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

running = True
rect = Rect(50, 60, 200, 80)
n = 50

def draw_text(text, pos):
    img = font.render(text, True, BLACK)
    screen.blit(img, pos)

def random_point():
    x = randint(0, SIZE[0])
    y = randint(0, SIZE[1])
    return (x, y)

def random_rects(n):
    rects = []
    for i in range(n):
        x, y = random_point()
        r = Rect(random_point(), (20, 20))
        rects.append(r)
    return rects

n = 30
rects = random_rects(n)
font = pygame.font.Font(None, 24)
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_r:
                rect = random_rects(n)

    screen.fill(GRAY)

    interesting = []
    for i in range(n - 1):
        r0 = rects[i]
        for j in range(i + 1, n):
            r1 = rects[j]
            if r0.colliderect(r1):
                interesting.append(r0)
                interesting.append(r1)
                break


    for i, r in enumerate(rects):
        color = RED if r in interesting else BLUE
        pygame.draw.rect(screen, color, r)
        draw_text(str(i), r.topleft)
    pygame.display.flip()

pygame.quit()
