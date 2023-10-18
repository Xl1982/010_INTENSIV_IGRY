import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Пинг понг")
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
sound0 = "1918.mp3"
pygame.mixer.music.load(sound0)
pygame.mixer.music.play()
s = pygame.mixer.Sound("sound.wav")
win = pygame.mixer.Sound("win.wav")
scorep1 = 0
scorep2 = 0
x1 = (490)
y1 = 250

x2 = (0)
y2 = 250

xb = 500
yb = 300

speedball = 5
dbo = 0
dbv = 0

def collision():
   global x1, y1
   global x2, y2
   global xb, yb
   global x, y
   global dbo
   global scorep1, scorep2

   def restart():
       global xb, yb, scorep1, scorep2
       global x, y
       scorep2 += 10
       pygame.display.set_caption("Пинг понг" + "Score player 1: " + str(scorep1) + " - Score player 2: " + str(scorep2))

   if dbo:
       if xb > 480:
           if yb >= y and yb < y + 50:
               dbo = 0
               s.play()
           else:
               xb, yb = 10, 20
               pygame.display.update()
               pygame.time.delay(500)
               win.play()
               restart()
   else:
       if xb < 10:
           if yb >= y2 and yb < y2 + 50:
               dbo = 1
               s.play()
           else:
               xb, yb = 480, 20
               pygame.display.update()
               pygame.time.delay(500)
               win.play()
               restart()

def sprite1(y):
   pygame.draw.rect(screen, RED, (x1, y, 10, 50))


def sprite2(y):
   pygame.draw.rect(screen, GREEN, (x2, y, 10, 50))


def ball():
   global xb, yb
   pygame.draw.ellipse(screen, WHITE, (xb, yb, 10, 10))


def move_ball(x, y):
   global xb, yb, dbo, dbv, speedball
   if dbo == 0:
       xb -= speedball
   if dbv == 0:
       yb += speedball
       if yb > 490:
           dbv = 1
   if dbv:
       yb -= speedball
       if yb < speedball:
           dbv = 0
   if dbo:
       xb += speedball


def move2():
   global y2
   if y2 <= 450:
       if keys[pygame.K_z]:
           y2 += 20
   if y2 > 0:
       if keys[pygame.K_a]:
           y2 -= 20

pygame.mouse.set_visible(False)
loop = 1
while loop:
   keys = pygame.key.get_pressed()
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           loop = 0

   x, y = pygame.mouse.get_pos()
   screen.fill((0, 0, 0))
   move_ball(xb, yb)
   ball()
   move2()
   sprite1(y)
   sprite2(y2)
   collision()
   pygame.display.update()
   clock.tick(60)

pygame.quit()
