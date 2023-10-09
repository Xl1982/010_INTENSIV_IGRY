import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"


def main():
   pygame.init()
   screen = pygame.display.set_mode(DISPLAY)
   pygame.display.set_caption("Платформер")
   bg = Surface((WIN_WIDTH, WIN_HEIGHT))
   bg.fill(Color(BACKGROUND_COLOR))

   while 1:
       for e in pygame.event.get():
           if e.type == QUIT:
               raise SystemExit

       screen.blit(bg, (0, 0))
       pygame.display.update()


if __name__ == "__main__":
   main()
