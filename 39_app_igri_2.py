import  pygame
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((640, 240))

running = True
drawing = False

points = []

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            print(event.pos)
            points.append(event.pos)
            drawing =True

        elif event.type == MOUSEBUTTONUP:
            drawing = False

        elif event.type == MOUSEMOTION and drawing:
            points[-1] = event.pos


        elif event.type == KEYDOWN: #если событие типа == НАЖИТИЕВНИЗ любой клавиши
            if event.key == K_ESCAPE: #если событие клавишы == ESC
                if len(points) > 0: # если длина списка больше 0
                    points.pop() # список удаляет последнюю

    screen.fill(GRAY)
    if len(points) > 1:
        rect = pygame.draw.lines(screen, RED, True, points, 3) # метод отрисовки линий
        pygame.draw.rect(screen, GREEN, rect, 1)
    pygame.display.update()
pygame.quit()