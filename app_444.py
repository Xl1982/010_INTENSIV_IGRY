import pygame
from pygame import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG = 52, 78, 91



font = pygame.font.SysFont('arialblack', 30)
TEXT_COL = 255, 255, 255

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Главное меню')



class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height *scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

resume_img = pygame.image.load('buttons/button_resume.png').convert_alpha()
resume_button = Button(304, 125, resume_img, 1)

def draw_text(text, font, text_col, x, y) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

run = True
game_pause = False
while run:
    screen.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_pause = not game_pause


    if game_pause:
        draw_text("Pause", font, TEXT_COL, 250, 250)
        if resume_button.draw(screen):
            game_pause = False
    else:
        draw_text('press space for pause', font, TEXT_COL, 160, 250)


    pygame.display.update()

pygame.quit()