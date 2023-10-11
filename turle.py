import turtle
import random

# Настройка экрана
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Калейдоскоп Turtle")

# Создание черепахи для рисования
kaleidoscope = turtle.Turtle()
kaleidoscope.speed(0)  # Максимальная скорость
kaleidoscope.width(2)  # Ширина линии

# Функция для получения случайного цвета
def random_color():
    return (random.random(), random.random(), random.random())

# Функция для рисования калейдоскопического узора
def draw_pattern(turt, size):
    for _ in range(4):  # Каждая часть узора состоит из 4х линий
        turt.color(random_color())  # Выберите случайный цвет для каждой линии
        turt.forward(size)
        turt.right(90)

# Основная часть программы для рисования калейдоскопического узора
for _ in range(72):  # Нарисуйте 72 узора для полного круга
    draw_pattern(kaleidoscope, 100)
    kaleidoscope.right(5)  # Поверните на 5 градусов после каждого узора

# Завершение рисования
kaleidoscope.hideturtle()
screen.mainloop()
