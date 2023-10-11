import pygame
import pymunk
from pymunk.pygame_util import DrawOptions

# Инициализация
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Настройка Pymunk
space = pymunk.Space()
space.gravity = (0, 1000)  # гравитация вниз

# Персонаж игры
radius = 25
mass = 1
player_body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
player_body.position = (width/2, height/2)
player_shape = pymunk.Circle(player_body, radius)
player_shape.friction = 0.5
space.add(player_body, player_shape)

# Платформы
segment1 = pymunk.Segment(space.static_body, (100, 300), (700, 300), 5)
segment1.friction = 1.0
space.add(segment1)

segment2 = pymunk.Segment(space.static_body, (100, 500), (700, 500), 5)
segment2.friction = 1.0
space.add(segment2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_body.apply_impulse_at_local_point((-0, -300))  # прыжок

    screen.fill((255, 255, 255))
    space.debug_draw(DrawOptions(screen))
    space.step(1/60.0)  # обновление физики
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
