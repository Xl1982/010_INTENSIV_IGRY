import pygame

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

while True:
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 50)

    pygame.draw.ellipse(screen, (0, 255, 0), (200, 200, 100, 50))

    pygame.draw.polygon(screen, (0, 0, 255), [(400, 400), (450, 450), (500, 400)])

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255, 255, 0), (mx - 50, my - 25, 100, 100))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    clock.tick(60)



# import random
# import pygame
# from pygame.locals import *
#
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GRAY = (122, 122, 122)
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# ball = pygame.image.load('ball.gif')
# rect = ball.get_rect()
# speed = [2, 2]
# size = 640, 320
# width, height = size
#
# screen = pygame.display.set_mode(size)
# running = True
#
# background = WHITE
# caption = "Привет жми все кнопки сразу"
#
# while running:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             running = False
#
#     screen.fill(background)
#     # pygame.draw.ellipse(screen, RED, (50, 20, 160, 100))
#     pygame.draw.rect(screen, RED, (1, 1, 160, 100))
#     pygame.display.update()
#
# pygame.quit()
