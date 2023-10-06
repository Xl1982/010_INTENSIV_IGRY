Методические указания
Урок 38.1 Введение в библиотеку PyGame
Задачи урока:
Введение в библиотеку PyGame

0. Подготовка к уроку

До начала урока преподавателю необходимо:
Просмотреть, как ученики справились с домашним заданием
Прочитать методичку

1. Введение в библиотеку PyGame

Учитель: ‎‎Сегодня мы с вами начнем знакомство еще с одним модулем для создания 2D игр - pygame.
Pygame — это «игровая библиотека», набор инструментов, помогающих программистам создавать игры. К ним относятся:
Графика и анимация
Звук (включая музыку)
Управление (мышь, клавиатура, геймпад и так далее)
Для начала необходимо установить модуль с помощью команды
pip install pygame
 ‎
Теперь создадим простой шаблон окна нашего приложения. Для этого импортируем pygame
import pygame




Чтобы установить размер нашего окна, воспользуемся командой pygame.display.setmode, которая принимает кортеж с размерами окна
screen = pygame.display.set_mode((640, 240))




Далее нам необходимо создать бесконечный цикл(игровой цикл). В основе каждой игры лежит цикл, который принято называть «игровым циклом». Он запускается снова и снова, делая все, чтобы работала игра.
while True:
   for event in pygame.event.get():
       print(event)



В данном случае в цикле мы перебираем список всех событий(нажатие кнопки, перемещение мыши и т.п) и выводим в консоль. При запуске данного кода, мы получим черное окно заданного размера и вывод всех событий в консоль. Так как цикл у нас бесконечный, то прекратить выполнение программы можно только остановив ее в pycharm, либо же нажав комбинацию клавиш CTRL+C.

Чтобы наше приложение закрывалось по нажатию по кнопке закрыть, мы должны обработать данное событие в игровом цикле.
import pygame

screen = pygame.display.set_mode((640, 240))
running = True
while running:
   for event in pygame.event.get():
       print(event)
       if event.type == pygame.QUIT:
           running = False

pygame.quit()




Теперь давайте разберемся с работой с цветами в pygame. Цвета определяются как кортежи базовых цветов красного, зеленого и синего. Это называется моделью RGB. Каждый базовый цвет представлен в виде числа от 0 (минимум) до 255 (максимум), которое занимает 1 байт в памяти. Таким образом, цвет RGB представляется в виде 3-байтового значения. Смешивание двух или более цветов приводит к появлению новых цветов. В общей сложности 16 миллионов различных цветов могут быть представлены таким образом.
Поскольку цвета являются константами, будем писать их с помощью заглавных букв. Отсутствие всех цветов приводит к черному. Максимальное значение для всех трех компонентов приводит к белому цвету. Три одинаковых промежуточных значения приводят к серому цвету:
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)




Основные(базовые) цвета указываются как:
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




Смешивая два базовых цвета, мы получаем больше цветов:
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)




В конце игрового цикла добавим следующее:
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
   screen.fill(YELLOW)
   pygame.display.update()




Метод fill(color) заполняет весь экран заданным цветом. На этом этапе ничего не будет отображаться. Для того, чтобы что-либо показать, должна быть вызвана функция pygame.display.update().

Теперь давайте модернизируем наш код таким образом, чтобы при нажатии на кнопки R и G цвет фона менялся с серого на красный или зеленый соответственно.
Добавим константы с цветами
GRAY = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)




Создадим переменную в которой укажем начальный цвет фона
background = GRAY




и теперь изменим наш игровой цикл
while running:
   for event in pygame.event.get():
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_r:
               background = RED
           elif event.key == pygame.K_g:
               background = GREEN
       elif event.type == pygame.QUIT:
           running = False
   screen.fill(background)
   pygame.display.update()





В данном случае мы указываем, что цвет фона при запуске - серый, а при перехвате события нажатия на клавиши r(K_r) или g(K_g) цвет менялся на соответствующий.

Модуль pygame.locals содержит около 280 констант, используемых и определяемых pygame. Размещение этого оператора в начале программы импортирует их все:
import pygame
from pygame.locals import *




Теперь мы можем обратиться к ключевым модификаторам, таким как alt, ctrl, cmd и т.д
KMOD_ALT, KMOD_CAPS, KMOD_CTRL, KMOD_LALT,
KMOD_LCTRL, KMOD_LMETA, KMOD_LSHIFT, KMOD_META,
KMOD_MODE, KMOD_NONE, KMOD_NUM, KMOD_RALT, KMOD_RCTRL,
KMOD_RMETA, KMOD_RSHIFT, KMOD_SHIFT


числовым клавишам
K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9


специальным символьным клавишам
K_AMPERSAND, K_ASTERISK, K_AT, K_BACKQUOTE,
K_BACKSLASH, K_BACKSPACE, K_BREAK


и соответственно буквенном клавишам
K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z


Теперь вместо того, чтобы обращаться к нажатой клавише как pygame.KEYDOWN, можно обращаться просто KEYDOWN (например K_0)

С цветами думаю разобрались, можно рассмотреть как изменить заголовок нашего окна. В этом нам поможет команда pygame.display.set_caption(title). Добавим ее в игровой цикл
caption = 'Цвет фона = ' + str(background)
pygame.display.set_caption(caption)




В заголовке мы увидим строку Цвет фона и численное обозначение цвета в формате RGB.
Для примера базовых возможностей модуля напишем простую программу с прыгающим мячом. Изображение мяча можно скачать по ссылке https://pygame.readthedocs.io/en/latest/_downloads/3422fe7ca1642ced1476b30d5bac2868/ball.gif

Подгрузим изображения мяча
ball = pygame.image.load("ball.gif")


Создадим переменную, в которую запишем значение границ нашего мяча
rect = ball.get_rect()


У данного объекта есть 4 значения, к которым мы можем обратиться
rect.left
rect.top
rect.right
rect.bottom


Добавим необходимые переменные
RED = (255, 0, 0)
speed = [2, 2]
size = 640, 320
width, height = size
screen = pygame.display.set_mode(size)


Добавим условие в котором наш мяч при касании о края нашего окна будет менять направление и укажем скорость движения для мяча
rect = rect.move(speed)
if rect.left < 0 or rect.right > width:
   speed[0] = -speed[0]
if rect.top < 0 or rect.bottom > height:
   speed[1] = -speed[1]


и соответственно отрисуем наш мяч и укажем рамку для границ мяча
pygame.draw.rect(screen, RED, rect, 1)
screen.blit(ball, rect)


читель: ‎‎Давайте поработаем с отрисовкой примитивных фигур в pygame. Модуль pygame.draw позволяет рисовать на поверхности простые фигуры. Это может быть поверхность экрана или любой объект, такой как изображение или рисунок. Мы можем отрисовывать с помощью отдельных функций круги, прямоугольники, эллипсы и фигуры состоящие из множества точек.
Эти функции объединяет то, что они:
Принимают объект на котором отрисовываем в качестве первого аргумента
Цвет в качестве второго аргумента
Параметр width в качестве последнего аргумента
возвращает объект Rect, ограничивающий измененную область
и имеют следующий формат:
rect(Surface, color, Rect, width) -> Rect
polygon(Surface, color, pointlist, width) -> Rect
circle(Surface, color, center, radius, width) -> Rect


Большинство функций принимают аргумент width. Если ширина равна 0, фигура заливается указанным цветом.

Для начала отрисуем прямоугольники полностью залитые цветом, а также имеющие просто обводку. Также для примера укажем разную ширину.

import pygame

GRAY = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

background = GRAY
size = 640, 320
width, height = size
screen = pygame.display.set_mode(size)
running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   screen.fill(background)
   pygame.draw.ellipse(screen, RED, (50, 20, 160, 100))
   pygame.draw.ellipse(screen, GREEN, (100, 60, 160, 100))
   pygame.draw.ellipse(screen, BLUE, (150, 100, 160, 100))

   pygame.draw.ellipse(screen, RED, (350, 20, 160, 100), 1)
   pygame.draw.ellipse(screen, GREEN, (400, 60, 160, 100), 4)
   pygame.draw.ellipse(screen, BLUE, (450, 100, 160, 100), 8)

   pygame.display.update()
   pygame.display.update()

pygame.quit()


Сделаем подобное с эллипсами
pygame.draw.ellipse(screen, RED, (50, 20, 160, 100))
pygame.draw.ellipse(screen, GREEN, (100, 60, 160, 100))
pygame.draw.ellipse(screen, BLUE, (150, 100, 160, 100))
pygame.draw.ellipse(screen, RED, (350, 20, 160, 100), 1)
pygame.draw.ellipse(screen, GREEN, (400, 60, 160, 100), 4)
pygame.draw.ellipse(screen, BLUE, (450, 100, 160, 100), 8)




Нажатие кнопок мыши приводит к появлению событий MOUSEBUTTONDOWN и MOUSEBUTTONUP. Напишем код, который обнаруживает эти события и выводит в консоль:

import pygame
from pygame.locals import *

GRAY = (127, 127, 127)
background = GRAY
size = 640, 320
width, height = size
screen = pygame.display.set_mode(size)
running = True
while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False
       elif event.type == MOUSEBUTTONDOWN:
           print(event)
       elif event.type == MOUSEBUTTONUP:
           print(event)
   pygame.display.update()

pygame.quit()


При нажатии и отпускании кнопки мыши в консоль будут выводится сообщения типа
<Event(5-MouseButtonDown {'pos': (123, 88), 'button': 1, 'window': None})>
<Event(6-MouseButtonUp {'pos': (402, 128), 'button': 1, 'window': None})>
<Event(5-MouseButtonDown {'pos': (402, 128), 'button': 3, 'window': None})>
<Event(6-MouseButtonUp {'pos': (189, 62), 'button': 3, 'window': None})>




Теперь добавим обработку перехвата перемещения мыши
elif event.type == MOUSEMOTION:
   print(event)


и при запуске при перемещении мыши увидим
<Event(4-MouseMotion {'pos': (537, 195), 'rel': (-1, 0), 'buttons': (0, 0, 0), 'window': None})>
<Event(4-MouseMotion {'pos': (527, 189), 'rel': (-10, -6), 'buttons': (0, 0, 0), 'window': None})>
<Event(4-MouseMotion {'pos': (508, 180), 'rel': (-19, -9), 'buttons': (0, 0, 0), 'window': None})>




Мы можем использовать эти три события, чтобы нарисовать прямоугольник на экране. Определяем прямоугольник по его диагональной начальной и конечной точке. Нам также нужен флаг, который указывает, если кнопка мыши опущена и если мы рисуем:
start = (0, 0)
size = (0, 0)
drawing = False


При нажатии кнопки мыши мы устанавливаем начало на текущее положение мыши и переключаем флаг, чтоб режим рисования начался:
elif event.type == MOUSEBUTTONDOWN:
    start = event.pos
    size = 0, 0
    drawing = True


Когда кнопка мыши отпущена, устанавливаем конечную точку и отмечаем флагом, что режим рисования закончился:
elif event.type == MOUSEBUTTONUP:
    end = event.pos
    size = end[0] - start[0], end[1] - start[1]
    drawing = False




Когда мышь движется, мы также должны проверить, находимся ли мы в режиме рисования. Если да, то устанавливаем конечную позицию на текущую позицию мыши:
elif event.type == MOUSEMOTION and drawing:
    end = event.pos
    size = end[0] - start[0], end[1] - start[1]


Наконец, рисуем прямоугольник на экране. Сначала заполняем цвет фона. Затем вычисляем размер прямоугольника,  рисуем его, и в самом конце обновляем экран:
screen.fill(GRAY)
pygame.draw.rect(screen, RED, (start, size), 2)
pygame.display.update()




Давайте модернизируем код, чтобы отрисовывать не одну, а несколько фигур.Создадим необходимые переменные
start = (0, 0)
size = (0, 0)
drawing = False
rect_list = []




изменим условие в игровом цикле
elif event.type == MOUSEBUTTONUP:
    end = event.pos
    size = end[0]-start[0], end[1]-start[1]
    rect = pygame.Rect(start, size)
    rect_list.append(rect)
    drawing = False




Ну и наконец добавим цикл внутри игрового цикла для отрисовки множества фигур
screen.fill(GRAY)
for rect in rect_list:
    pygame.draw.rect(screen, RED, rect, 3)
pygame.draw.rect(screen, BLUE, (start, size), 1)
pygame.display.update()




Код целиком
import pygame
from pygame.locals import *

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

pygame.init()
screen = pygame.display.set_mode((640, 240))

start = (0, 0)
size = (0, 0)
drawing = False
rect_list = []

running = True

while running:
   for event in pygame.event.get():
       if event.type == QUIT:
           running = False

       elif event.type == MOUSEBUTTONDOWN:
           start = event.pos
           size = 0, 0
           drawing = True

       elif event.type == MOUSEBUTTONUP:
           end = event.pos
           size = end[0] - start[0], end[1] - start[1]
           rect = pygame.Rect(start, size)
           rect_list.append(rect)
           drawing = False

       elif event.type == MOUSEMOTION and drawing:
           end = event.pos
           size = end[0] - start[0], end[1] - start[1]

   screen.fill(GRAY)
   for rect in rect_list:
       pygame.draw.rect(screen, RED, rect, 3)
   pygame.draw.rect(screen, BLUE, (start, size), 1)
   pygame.display.update()

pygame.quit()





Дополнительно
Если на уроке остается время, то ученикам можно предложить начать прорешивать домашнее задание.

Домашняя работа
Задача 1
Отрисовать круг, эллипс и многоульники в разных местах экрана, а также добавить возможность отрисовки эллипса при зажатой кнопке мыши






