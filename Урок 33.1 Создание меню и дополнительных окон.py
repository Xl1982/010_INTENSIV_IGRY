Методические указания
Урок 33.1 Создание меню и дополнительных окон
Задачи урока:
Создание меню и дополнительных окон

0. Подготовка к уроку

До начала урока преподавателю необходимо:
Просмотреть, как ученики справились с домашним заданием
Прочитать методичку

1. Создание меню и дополнительных окон

Учитель: ‎ Сегодня мы научимся создавать стартовые экраны, а также экраны проигрыша для нашей игры.
Для начала создадим простой прототип игры, где персонаж управляется мышкой и собирает монеты
import random
import arcade

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Работа с окнами"


class MyGame(arcade.Window):

   def __init__(self):
       super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
       arcade.set_background_color(arcade.color.AMAZON)

   def setup(self):
      pass

   def on_draw(self):
       self.clear()

   def on_mouse_motion(self, x, y, dx, dy):
      pass

   def on_update(self, delta_time):
      pass

if __name__ == "__main__":
   window = MyGame()
   window.setup()
   arcade.run()




Заготовку сделали. Идем далее. Создадим персонажа. Создадим необходимые переменные в методе init
self.player_list = None
self.player_sprite = None


В setup
def setup(self):
   self.player_list = arcade.SpriteList()
   self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                      SPRITE_SCALING_PLAYER)
   self.player_sprite.center_x = 50
   self.player_sprite.center_y = 50
   self.player_list.append(self.player_sprite)




в on_draw отрисуем
def on_draw(self):
   self.clear()
   self.player_list.draw()




Теперь давайте добавим движение с помощью мыши
def on_mouse_motion(self, x, y, dx, dy):
   self.player_sprite.center_x = x
   self.player_sprite.center_y = y




Так отлично. Ну и осталось реализовать монетки
self.coin_list = None





self.coin_list = arcade.SpriteList()
for i in range(COIN_COUNT):
   coin = arcade.Sprite(":resources:images/items/coinGold.png",
                        SPRITE_SCALING_COIN)
   coin.center_x = random.randrange(SCREEN_WIDTH)
   coin.center_y = random.randrange(SCREEN_HEIGHT)
   self.coin_list.append(coin)




self.coin_list.draw()




def on_update(self, delta_time):
   self.coin_list.update()




Готово. Давайте сделаем так, что если сталкивается игрок и монета, то она будет удаляться из списка. Также прописываем в on_update
coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
for coin in coins_hit_list:
   coin.remove_from_sprite_lists()




Также сделаем курсор мыши невидимым
self.set_mouse_visible(False)




Наш прототип готов. Давайте перейдем к основной теме занятия
Для создания окон нам потребуется использовать представления
Представления позволяют легко переключать то, что вы показываете в окне. Вы можете использовать это для добавления экранов, таких как:
Начальные экраны
Экраны инструкций
Конец игры
Экран паузы


Класс View очень похож на класс Window, с которым мы уже работали.. В классе View есть методы для on_update и on_draw так же, как Window. Мы можем изменить текущий вид, чтобы быстро изменить код, управляющий тем, что рисуется в окне, и обрабатывающий пользовательский ввод.

Давайте изменим основной класс окна используя представления
class GameView(arcade.View):




Класс View не контролирует размер окна, поэтому нам нужно убрать это из вызова родительского класса
class GameView(arcade.View):
   def __init__(self):
       super().__init__()




Класс Window по-прежнему контролирует, видима мышь или нет, поэтому, чтобы скрыть мышь, нам нужно использовать атрибут, window который является частью View класса.
self.window.set_mouse_visible(False)




Теперь вместо простого создания окна мы создадим окно, представление и затем покажем это представление.
if __name__ == "__main__":
   window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
   start_view = GameView()
   window.show_view(start_view)
   start_view.setup()
   arcade.run()


Запускаем. Все работает как и прежде. Теперь мы готовы добавить экран инструкций. Создадим для него класс:
class InstructionView(arcade.View):
   pass




Затем нам нужно определить метод on_show_view, который будет запущен один раз, когда мы переключимся на это представление. В этом случае нам не нужно много делать, просто установим цвет фона. Если игра имеет скроллинг, нам также нужно сбросить область просмотра.
class InstructionView(arcade.View):
   def on_show_view(self):
       arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
       arcade.set_viewport(0, self.window.width, 0, self.window.height)




Метод on_draw работает также, как метод класса окна, но он будет вызываться только тогда, когда это представление активно.
В этом случае мы просто нарисуем текст для экрана инструкций с помощью draw_text
def on_draw(self):
   self.clear()
   arcade.draw_text("Экран инструкций", self.window.width / 2, self.window.height / 2,
                    arcade.color.WHITE, font_size=50, anchor_x="center")
   arcade.draw_text("Щелкни для продолжения", self.window.width / 2, self.window.height / 2 - 75,
                    arcade.color.WHITE, font_size=20, anchor_x="center")




Затем мы добавим метод, реагирующий на щелчок мыши. Здесь мы создадим GameView и вызовем метод setup.
def on_mouse_press(self, _x, _y, _button, _modifiers):
   game_view = GameView()
   game_view.setup()
   self.window.show_view(game_view)




Теперь нам нужно вернуться к созданию нашего окна. Вместо создания GameView теперь необходимо создать InstructionView
if __name__ == "__main__":
   window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
   start_view = InstructionView()
   window.show_view(start_view)
   arcade.run()




Проверяем. Все работает.
Другой способ сделать экраны инструкций, паузы и игры оконченными — использовать изображения. В этом примере мы используем отдельное изображение того же размера, что и наше окно.
Новое представление GameOverView, которое мы добавляем в игру, загружает изображение экрана в виде текстуры в __init__. Метод on_draw рисует эту текстуру на экране.

Когда пользователь нажимает кнопку мыши, мы просто начинаем игру заново.
class GameOverView(arcade.View):
   def __init__(self):
       super().__init__()
       self.texture = arcade.load_texture("game_over.png")
       arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

   def on_draw(self):
       self.clear()
       self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                               SCREEN_WIDTH, SCREEN_HEIGHT)

   def on_mouse_press(self, _x, _y, _button, _modifiers):
       game_view = GameView()
       game_view.setup()
       self.window.show_view(game_view)




Последнее, что нам нужно, это вызвать представление «Game Over».В методе on_update мы можем проверить длину списка. Как только он достигнет нуля, мы изменим наше представление
if len(self.coin_list) == 0:
   view = GameOverView()
   self.window.show_view(view)




Теперь давайте создадим  подобный класс для паузы
class PauseView(arcade.View):
   def __init__(self, game_view):
       super().__init__()
       self.game_view = game_view




def on_draw(self):
   self.clear()
   player_sprite = self.game_view.player_sprite
   player_sprite.draw()




Добавим в на экран также текст
arcade.draw_text("Пауза", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                arcade.color.BLACK, font_size=50, anchor_x="center")

arcade.draw_text("Нажмите Esc для продолжения",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center")
arcade.draw_text("Press Enter to reset",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 30,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center")




Также необходимо прописать обработчик нажатия клавиши Esc, при нажатии на которую у нас будут переключаться экраны
def on_key_press(self, key, _modifiers):
   if key == arcade.key.ESCAPE:
       self.window.show_view(self.game_view)
   elif key == arcade.key.ENTER:
       game = GameView()
       self.window.show_view(game)




Подобное сделаем и в основном игровом классе
def on_key_press(self, key, _modifiers):
   if key == arcade.key.ESCAPE:
       pause = PauseView(self)
       self.window.show_view(pause)


Проверяем. Все работает. Давайте немного только поправим цвет окна паузы. Для этого мы создадим в классе нашего окна паузы метод on_show_view, в котором укажем цвет фона
def on_show_view(self):
   arcade.set_background_color(arcade.color.ORANGE)




При запуске все работает, но после паузы цвет основного игрового окна меняется. Решение достаточно простое. Создадим такой же метод в основном классе

def on_show_view(self):
   arcade.set_background_color(arcade.color.AMAZON)




Проблема решена. Ну и напоследок для красоты можем отрисовать прямоугольник, такого же цвета как и экран паузы, чтобы немного затемнить персонажа
arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                 right=player_sprite.right,
                                 top=player_sprite.top,
                                 bottom=player_sprite.bottom,
                                 color=arcade.color.ORANGE + (200,))




Дополнительно
Если на уроке остается время, то ученикам можно предложить начать прорешивать домашнее задание.





2. Решение задач
Задача 1
	Отрисовать текст на стартовом окне НАЧАТЬ ИГРУ. При нажатии на который, игра будет начинаться
Решение
class InstructionView(arcade.View):
   def on_show_view(self):
       arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
       arcade.set_viewport(0, self.window.width, 0, self.window.height)

   def on_draw(self):
       self.clear()
       arcade.draw_text("Экран инструкций", self.window.width / 2, self.window.height / 2,
                        arcade.color.WHITE, font_size=50, anchor_x="center")
       arcade.draw_text("Щелкни для продолжения", self.window.width / 2, self.window.height / 2 - 75,
                        arcade.color.WHITE, font_size=20, anchor_x="center")

       arcade.draw_text("НАЧАТЬ ИГРУ", self.window.width / 2, self.window.height / 2 - 145,
                        arcade.color.WHITE, font_size=20, anchor_x="center")

   def on_mouse_press(self, _x, _y, _button, _modifiers):
       if 310 < _x < 490 and 158 < _y < 175:
           game_view = GameView()
           game_view.setup()
           self.window.show_view(game_view)




Для нахождения и проверки координат создаем метод on_mouse_motion
def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
   print(f'{x=}')
   print(f'{y=}')






Домашняя работа
Задача 1
Добавить в свой платформер стартовое меню с возможностью запуска игры, выхода из игры
