import random
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (122, 122, 122)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ball = pygame.image.load('ball.gif')
rect = ball.get_rect()
speed = [2, 2]
size = 640, 320
width, height = size

screen = pygame.display.set_mode(size)
running = True

background = WHITE
caption = "Привет жми все кнопки сразу"

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(WHITE)

    screen.blit(ball, rect) # отрисовать слой поверху
    pygame.display.flip()

    pygame.time.delay(10) # задержка

pygame.quit()
