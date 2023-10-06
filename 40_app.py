import pygame
import time
from pygame.locals import *
RED = (255, 0, 0)
GRAY = (150, 150, 150)
GREEN = (150, 255, 150)
size = 800, 600
w, h = size

pygame.init() # инициализация пайгейм
pygame.font.init() # инициализация модуля шрифтов


screen = pygame.display.set_mode((w, h)) # создаем окно, с заданными размерами


background = pygame.image.load('desert.png') # задаем фон
pygame.display.set_caption('DinoGame') #описание в окне

running = True # флаг цикла


player_sprite = pygame.image.load('dino.png') # загружаем пикчу в спрайт
player_sprite = pygame.transform.rotozoom(player_sprite, 0, 0.1)
player_rect = player_sprite.get_rect()
player_rect.center = 0 + player_rect.size[0] / 2, size[1] // 2

speed = [0, 9]

cactus = pygame.image.load('cactus.png')
cactus = pygame.transform.rotozoom(cactus, 0, 0.2)
cactus_rect = cactus.get_rect()
cactus_rect.left = size[0]
cactus_rect.bottom = size[1] - 100

cactus_speed = [-10, 0]

timer = pygame.time.Clock()
is_jump = False # флаг прыжка перса
score = 0
score_font = pygame.font.SysFont('arial', 36)
score_text = score_font.render(f'Score{score}', True, (180, 0, 0))
lose_text = score_font.render('', True, (180, 0, 0))


while running:
    timer.tick(60) #максимальное колличество выполнения циклов в минут
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            is_jump = True

    keys = pygame.key.get_pressed()
    if keys[K_SPACE] and is_jump == False:
        player_rect.y -= 20

    # отображение фона и спрайтов
    screen.blit(background, (0,0))
    screen.blit(player_sprite, player_rect)
    screen.blit(cactus, cactus_rect)

    cactus_rect = cactus_rect.move(cactus_speed)
    player_rect = player_rect.move(speed)

    if player_rect.bottom > size[1] - 100:
        player_rect.bottom = size[1] - 100
        is_jump = False

    if cactus_rect.left < 0:
        cactus_rect.right = size[0]
        score += 1
        score_text = score_font.render(f'Screen {score}', True, (180, 0, 0))

    if player_rect.colliderect(cactus_rect):
        lose_text = score_font.render('You loose', True, (180, 0, 0))
        time.sleep(5)
        running = False

    screen.blit(lose_text, (size[0] / 2, size[1] / 2 ))
    screen.blit(score_text, (10, 20))

    pygame.display.update()

pygame.quit()







