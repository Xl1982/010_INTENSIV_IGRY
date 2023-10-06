import random
import time
import math
from array import array # для работы с массивами
from dataclasses import dataclass
import arcade
import arcade.gl # подмодуль для работы с open Gl

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'GPU'

PARTICLE_COUNT = 10 # колличество частиц
MIN_FADE_TIME = 0.25
MAX_FADE_TIME = 11.5

@dataclass
class Burst: # класс взрыва
    buffer: arcade.gl.Buffer # буфер данных частиц
    vao: arcade.gl.geometry # объект вершинного массива
    start_time: float # время начала взрыва


class ParticleBurstApp(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.burst_list = [] # список взрывов
        # загрузка шейдерных программ для отображения
        self.program = self.ctx.load_program(
            vertex_shader="vertex_shader_v1.glsl",
            fragment_shader="fragment_shader.glsl",
        )

        self.ctx.enable_only(self.ctx.BLEND)


    def on_draw(self):
        self.clear()

        self.ctx.point_size = 5 * self.get_pixel_ratio()# установка точек в зависимости от разрешения экрана
        for burst in self.burst_list:
            self.program['time'] = time.time() - burst.start_time # время жизни взрыва
            # отображение взрыва с помощью шейдерной программы
            burst.vao.render(self.program, mode=self.ctx.POINTS)

    def on_update(self, dt):
        temp_list = self.burst_list.copy() #создаем копию списка взрывов
        for burst in temp_list:
            if time.time() - burst.start_time > MAX_FADE_TIME:
                self.burst_list.remove(burst) # удаляем взрыв из списка


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        def _gen_initial_data(initial_x, initial_y):
            for i in range(PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi) # случайный угол частицы
                speed = abs(random.gauss(0, 9)) * .5 # случайная скорость
                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed
                red = random.uniform(0.1, 1.0)
                green = random.uniform(0, red)
                blue = 0
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME) # скорость исчезновения

                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        # преобразование координат мыши в координаты OpenGl
        x2 = x / self.width * 2. - 1.
        y2 = y / self.height * 2. - 1.

        initial_data = _gen_initial_data(x2, y2)
        buffer = self.ctx.buffer(data=array('f', initial_data))

        # описание буфера
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         '2f 2f 3f f',
                                                         ['in_pos',
                                                          'in_vel',
                                                          'in_color',
                                                          'in_fade_rate'])

        vao = self.ctx.geometry([buffer_description]) # создание объекта вершинного массива

        #создание нового взрыва и добавление его в список
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)

if __name__ == "__main__":
    window = ParticleBurstApp()
    window.center_window()
    arcade.run()