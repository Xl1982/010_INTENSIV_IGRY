import time
from pygame.locals import*
import pygame

ball = pygame.image.load('giraff.gif')
rect = ball.get_rect()
speed = [2, 2] # скорость в пикселях X Y
size = 640, 320
width, height = size
screen = pygame.display.set_mode(size)
RED = (255, 0, 0)

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]

    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, RED, rect, 1)
    screen.blit(ball, rect)
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()


