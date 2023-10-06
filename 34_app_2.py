import arcade
import arcade.gui # импорт гр интерфейса пользователя graphic user interface

class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "UIFlatbutton Example", resizable=True) #инициализация родителського класса с параметрами
        self.manager = arcade.gui.UIManager() # инициализация менеджера пользовательского интерфейса
        self.manager.enable() # включение менеджера юзеринтерфейса
        arcade.set_background_color(arcade.color.DARK_YELLOW) # установка цвета фона
        self.v_box = arcade.gui.UIBoxLayout() # контейнер для элемента польз интерфейса
        start_button = arcade.gui.UIFlatButton(text="START", width=200) #создание кнопки старт
        self.v_box.add(start_button.with_space_around(bottom=20)) # добавление кнопки в вертикальный контейнер

        settings_button = arcade.gui.UIFlatButton(text='Settings', width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)







        start_button.on_click = self.on_click_start # привязка метода onclick к событию нажатия на кнопку

        @start_button.event('on_click') # добавление дополнительного обработчика для события нажатия на кнопку
        def on_click_setting(event):
            print("Settings", event)

        #добавление вертикального контейнере в менеджер пользовательского интерфейса
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    # определение метода, который вызывается при клике на кнопку старт
    def on_click_start(self, event):
        print("Start:", event) # вывод сообщения в консоль

    def on_draw(self):
        self.clear()
        self.manager.draw()

window = MyWindow()
arcade.run()