Методические указания
Урок 39.1 Отрисовка и анимация геометрических фигур
Задачи урока:
Отрисовка и анимация геометрических фигур

0. Подготовка к уроку

До начала урока преподавателю необходимо:
Просмотреть, как ученики справились с домашним заданием
Прочитать методичку

1. Отрисовка и анимация геометрических фигур

Учитель: ‎‎Сегодня мы вами продолжим знакомиться с отрисовкой геометрических фигур. Перейдем к более сложному примеру. Создадим фигуру состоящую из множества вершин(точек). Для начала создадим заготовку нашего окна
import pygame
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((640, 240))

running = True

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

   screen.fill(GRAY)
   pygame.display.update()

pygame.quit()




Введем переменные отвечающие за возможность отрисовки и список для хранения наших точек
drawing = False
points = []




В событии MOUSEBUTTONDOWN добавляем текущую точку в список и устанавливаем флаг true
elif event.type == MOUSEBUTTONDOWN:
    points.append(event.pos)
    drawing = True


и соответственно при нажатии флаг будем делать false
elif event.type == MOUSEBUTTONUP:
    drawing = False


В событии MOUSEMOTION перемещаем последнюю точку в списке, если установлен флаг рисования
elif event.type == MOUSEMOTION and drawing:
    points[-1] = event.pos




Если в списке более 2 точек, рисуем линию. Каждая функция возвращает прямоугольник. Отобразим этот прямоугольник зеленым цветом
screen.fill(GRAY)
if len(points) > 1:
   rect = pygame.draw.lines(screen, RED, True, points, 3)
   pygame.draw.rect(screen, GREEN, rect, 1)
pygame.display.update()


Нажатие клавиши ESCAPE удалит последнюю точку в списке
elif event.type == KEYDOWN:
    if event.key == K_ESCAPE:
        if len(points) > 0:
            points.pop()


Запускаем! Все работает замечательно.
Вернемся к прямоугольникам и поработаем с ними.
Прямоугольник является очень полезным объектом в графическом программировании. Он имеет свой собственный класс в Pygame и используется для хранения и управления прямоугольной областью. Объект можно создать, указав:
4 параметра влево, верх, ширина и высота
положение и размер
Объект, имеющий атрибут rect
Rect(left, top, width, height)
Rect(pos, size)
Rect(obj)




Создадим приложение с красным прямоугольником и выведем координаты, размер и положение краев в консоль.
import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode(SIZE)

rect = Rect(50, 60, 200, 80)
print(f'x={rect.x}, y={rect.y}, w={rect.w}, h={rect.h}')
print(f'left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}')
print(f'center={rect.center}')

running = True
while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

   screen.fill(GRAY)
   pygame.draw.rect(screen, RED, rect)
   pygame.display.flip()

pygame.quit()




Для того, чтобы сдвинуть наш прямоугольник к любому краю у нас есть размеры приложения. Давайте сдвинем наш прямоугольник вниз
rect = Rect(50, SIZE[1] / 2, 200, 80)


Отлично, а теперь сделаем так, чтобы прямоугольник выравнивался по краям в зависимости от нажатой кнопки для этого добавим в игровой цикл условие
if event.type == KEYDOWN:
   if event.key == K_l:
       rect.left = 0
   if event.key == K_c:
       rect.centerx = SIZE[0] // 2
   if event.key == K_r:
       rect.right = SIZE[0]

   if event.key == K_t:
       rect.top = 0
   if event.key == K_m:
       rect.centery = SIZE[1] // 2
   if event.key == K_b:
       rect.bottom = SIZE[1]




Теперь наш прямоугольник выравнивается по необходимому краю. Давайте изменим наш код и сделаем, чтобы при запуске появлялся красный и синий прямоугольники в одних координатах, а по нажатию на кнопки вверх, низ, лево или право у нас смещался красный прямоугольник. Создадим необходимые переменные
BLUE = (0, 0, 255)
dir = {K_LEFT: (-5, 0), K_RIGHT: (5, 0), K_UP: (0, -5), K_DOWN: (0, 5)}


Также создадим наши 2 прямоугольника
rect0 = Rect(50, 60, 200, 80)
rect = rect0.copy()


Изменим игровой цикл и отрисуем прямуогольники
while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       if event.type == KEYDOWN:
           if event.key in dir:
               v = dir[event.key]
               rect.move_ip(v)

   screen.fill(GRAY)
   pygame.draw.rect(screen, BLUE, rect0, 1)
   pygame.draw.rect(screen, RED, rect, 4)
   pygame.display.flip()




С помощью специальных методов , можно также сжимать или растягивать наши фигуры.Метод inflate(v) увеличивает или сжимает прямоугольник вектором и создает новый Объект Rect. Метод vinflate_ip(v) выращивает или сжимает Rect на месте. Напишем код, который использует 4 клавиши со стрелками для изменения размера прямоугольника. Тонкий синий прямоугольник является оригинальным, толстый красный прямоугольник - измененным.
import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode(SIZE)

dir = {K_LEFT: (-5, 0), K_RIGHT: (5, 0), K_UP: (0, -5), K_DOWN: (0, 5)}
running = True
rect = Rect(50, 60, 200, 80)
rect0 = rect.copy()

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       if event.type == KEYDOWN:
           if event.key in dir:
               v = dir[event.key]
               rect.inflate_ip(v)

   screen.fill(GRAY)
   pygame.draw.rect(screen, BLUE, rect0, 1)
   pygame.draw.rect(screen, RED, rect, 4)
   pygame.display.flip()

pygame.quit()


Существуют методы и для обрезки прямоугольника.Метод r0.clip(r1)возвращает новый прямоугольник, который является пересечением двух прямоугольников. Метод r0.union(r1) возвращает новый прямоугольник, который является объединением двух прямоугольников.
import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

dir = {K_LEFT: (-5, 0), K_RIGHT: (5, 0), K_UP: (0, -5), K_DOWN: (0, 5)}
running = True
r0 = Rect(50, 60, 200, 80)
r1 = Rect(100, 20, 100, 140)

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       if event.type == KEYDOWN:
           if event.key in dir:
               r1.move_ip(dir[event.key])

   clip = r0.clip(r1)
   union = r0.union(r1)

   screen.fill(GRAY)
   pygame.draw.rect(screen, YELLOW, union, 0)
   pygame.draw.rect(screen, GREEN, clip, 0)
   pygame.draw.rect(screen, BLUE, r0, 4)
   pygame.draw.rect(screen, RED, r1, 4)
   pygame.display.flip()

pygame.quit()




Учитель: Давайте разберем пример перемещения прямоугольника с помощью мыши. Функция rect.collidepoint(pos)возвращает значение True, если точка сталкивается с прямоугольником. Мы используем его с положением мыши, чтобы проверить, произошел ли щелчок мыши внутри прямоугольника. Если это так, мы перемещаем прямоугольник относительным движением мыши(event.rel)
Логическая переменная задается, когда кнопка мыши нажата внутри прямоугольника. Он остается истинным до тех пор, пока кнопка отжата. Прямоугольник перемещается только тогда, когда щелчок мыши происходит внутри прямоугольника. Пока прямоугольник движется, добавляем синий контур.
import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

running = True
rect = Rect(50, 60, 200, 80)
moving = False

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       elif event.type == MOUSEBUTTONDOWN:
           if rect.collidepoint(event.pos):
               moving = True

       elif event.type == MOUSEBUTTONUP:
           moving = False

       elif event.type == MOUSEMOTION and moving:
           rect.move_ip(event.rel)

   screen.fill(GRAY)
   pygame.draw.rect(screen, RED, rect)
   if moving:
       pygame.draw.rect(screen, BLUE, rect, 4)
   pygame.display.flip()

pygame.quit()




Напишем код, в котором прямоугольник будет постоянно перемещаться на значение v
from time import sleep

import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

running = True
rect = Rect(100, 50, 50, 50)
v = [2, 2]

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

   rect.move_ip(v)
   sleep(0.05)

   if rect.left < 0:
       v[0] *= -1
   if rect.right > SIZE[0]:
       v[0] *= -1
   if rect.top < 0:
       v[1] *= -1
   if rect.bottom > SIZE[1]:
       v[1] *= -1

   screen.fill(GRAY)
   pygame.draw.rect(screen, RED, rect)
   pygame.display.flip()

pygame.quit()


Метод rect.collidepoint(p) проверяет, сталкивается ли прямоугольник rect с точкой . Напишем код, где мы создаем 100 случайных точек и окрашиваем их в красный цвет, если они попадают внутрь прямоугольника.
Каждый раз при нажатии клавиши R создается 100 новых случайных точек.
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

pygame.init()
screen = pygame.display.set_mode(SIZE)

running = True
rect = Rect(100, 50, 50, 50)


def random_point():
   x = randint(0, SIZE[0])
   y = randint(0, SIZE[1])
   return (x, y)


def random_points(n):
   points = []
   for i in range(n):
       p = random_point()
       points.append(p)
   return points


points = random_points(100)
while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       if event.type == KEYDOWN:
           if event.key == K_r:
               points = random_points(100)

   screen.fill(GRAY)
   pygame.draw.rect(screen, GREEN, rect, 1)
   for p in points:
       if rect.collidepoint(p):
           pygame.draw.circle(screen, RED, p, 4, 0)
       else:
           pygame.draw.circle(screen, BLUE, p, 4, 0)

   pygame.display.flip()

pygame.quit()




Сделаем похожее, но с прямоугольниками.Метод rect.colliderect(r) проверяет, сталкивается ли прямоугольник с другим прямоугольником. В следующей программе мы создаем 50 случайных прямоугольников и окрашиваем их в красный цвет, если они сталкиваются с зеленым прямоугольником.
Каждый раз при нажатии клавиши R создается 50 новых случайных прямоугольников.
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

pygame.init()
screen = pygame.display.set_mode(SIZE)

running = True
rect = Rect(100, 50, 50, 50)

n = 50


def random_point():
   x = randint(0, SIZE[0])
   y = randint(0, SIZE[1])
   return (x, y)


def random_rects(n):
   rects = []
   for i in range(n):
       r = Rect(random_point(), (20, 20))
       rects.append(r)
   return rects


rects = random_rects(n)

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       if event.type == KEYDOWN:
           if event.key == K_r:
               rects = random_rects(n)

   screen.fill(GRAY)
   pygame.draw.rect(screen, GREEN, rect, 1)

   for r in rects:
       if rect.colliderect(r):
           pygame.draw.rect(screen, RED, r, 2)
       else:
           pygame.draw.rect(screen, BLUE, r, 1)

   pygame.display.flip()

pygame.quit()




Метод rect.colliderect(r) проверяет, сталкивается ли прямоугольник с другим прямоугольником. Если мы хотим знать, есть ли какие-либо два перекрывающихся прямоугольника, то мы должны сравнить каждый прямоугольник друг с другом.
Каждый раз при нажатии клавиши R создается 20 новых случайных прямоугольников.
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
rect = Rect(100, 50, 50, 50)

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
               rects = random_rects(n)

   screen.fill(GRAY)

   intersecting = []
   for i in range(n - 1):
       r0 = rects[i]
       for j in range(i + 1, n):
           r1 = rects[j]
           if r0.colliderect(r1):
               intersecting.append(r0)
               intersecting.append(r1)
               break

   for i, r in enumerate(rects):
       color = RED if r in intersecting else BLUE
       pygame.draw.rect(screen, color, r)
       draw_text(str(i), r.topleft)

   pygame.display.flip()

pygame.quit()





Дополнительно
Если на уроке остается время, то ученикам можно предложить начать прорешивать домашнее задание.

Домашняя работа
Задача 1
Отрисовать простого человека с помощью простых геометрических фигур






