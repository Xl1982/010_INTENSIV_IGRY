from main2 import func
func()
def decorator(func):
    """ДЕКОРАТОР"""

    def decorated():
        """функция Decorated"""

        func()
    return decorated

@decorator
def wrapped():
    """Оборачиваемая функция"""
    print("Функция wrapped")

print('старт программы...')
print(wrapped.__name__)
print(wrapped.__doc__)
print("Конец программы")



























"""def decorator_with_args(name): # определяем декоратор с аргументами, но еще не используем
    print('decorator_with_args: ', name)
    def real_decorator(func): # настоящий декоратор который будет принимать функцию
        print('>>> сам декоратор ', func.__name__)
        def decorated(*args, **kwargs): # определеям обернутую функцию, которая будет вызываться вместо оригинальной
            print(f'>>>перед функцией {func.__name__}')
            ret = func(*args, **kwargs)  # вызываем оригинальную функцию и сохраняем ее результат
            print(f'>>> после функции {func.__name__}')
            return ret # возвращаем результат оригинальной функции
        return decorated # возвращаем обернутую функцию
    return real_decorator # возвращаем настоящий декоратор


@decorator_with_args('тест')
def add(a,b):
    print('>>> функция add')
    return a + b

print('старт программы')
r = add(10, 10)
print(r)
print('Конец программы')





"""



"""Методические указания
Урок 24.1. Декораторы
Задачи урока:
Декораторы

0. Подготовка к уроку

До начала урока преподавателю необходимо:
Просмотреть, как ученики справились с домашним заданием
Прочитать методичку

1. Декораторы

Учитель:  Сегодня  давайте продолжим знакомство с декораторами в Python.
В декоратор можно передать и сам параметр. В этом случае нужно добавить еще один слой абстракции, то есть — еще одну функцию-обертку.
Это обязательно, поскольку аргумент передается декоратору. Затем функция, которая вернулась, используется для декорации нужной. Проще разобраться на примере.

def decorator_with_args(name):
    print('> decorator_with_args:', name)
    def real_decorator(func):
        print('>> сам декоратор', func.__name__)
        def decorated(*args, **kwargs):
            print('>>> перед функцие', func.__name__)
            ret = func(*args, **kwargs)
            print('>>> после функции', func.__name__)
            return ret
        return decorated
    return real_decorator

@decorator_with_args('test')
def add(a, b):
    print('>>>> функция add')
    return a + b

print('старт программы')
r = add(10, 10)
print(r)
print('конец программы')


Результат
> decorator_with_args: test
>> сам декоратор add
старт программы
>>> перед функцие add
>>>> функция add
>>> после функции add
20
конец программы

В декораторах-классах выполняются такие же настройки. Теперь конструктор класса получает все аргументы декоратора. Метод __call__ должен возвращать функцию-обертку, которая, по сути, будет выполнять декорируемую функцию. Например:

class DecoratorArgs:
    def __init__(self, name):
        print('> Декоратор с аргументами __init__:', name)
        self.name = name

    def __call__(self, func):
        def wrapper(a, b):
            print('>>> до обернутой функции')
            func(a, b)
            print('>>> после обернутой функции')
        return wrapper

@DecoratorArgs("test")
def add(a, b):
    print('функция add:', a, b)

print('>> старт')
add(10, 20)
print('>> конец')




Результат
> Декоратор с аргументами __init__: teste
>> старт
>>> до обернутой функции
функция add: 10 20
>>> после обернутой функции
>> конец

Учитель:  Один из атрибутов функции — строка документации (docstring), доступ к которой можно получить с помощью __doc__. Это строковая константа, определяемая как первая инструкция в объявлении функции.
При декорации возвращается новая функция с другими атрибутами. Но они не изменяются.

def decorator(func):
    '''Декоратор'''
    def decorated():
        '''Функция Decorated'''
        func()
    return decorated

@decorator
def wrapped():
    '''Оборачиваемая функция'''
    print('функция wrapped')

print('старт программы...')
print(wrapped.__name__)
print(wrapped.__doc__)
print('конец программы')


В этом примере функция wrapped — это, по сути, функция decorated, которую она заменяет.
Результат
старт программы...
decorated
Функция Decorated
конец программы

Вот где на помощь приходит функция wraps из модуля functools. Она сохраняет атрибуты оригинальной функции. Нужно лишь декорировать функцию wrapper с ее помощью.

from functools import wraps

def decorator(func):
    '''Декоратор'''
    @wraps(func)
    def decorated():
        '''Функция Decorated'''
        func()
    return decorated

@decorator
def wrapped():
    '''Оборачиваемая функция'''
    print('функция wrapped')

print('старт программы...')
print(wrapped.__name__)
print(wrapped.__doc__)
print('конец программы')


Результат
старт программы...
wrapped
Оборачиваемая функция
конец программы

Учитель:  Давайте напишем для практики несколько примеров.
Декоратор можно использовать для декорирования класса. Отличие лишь в том, что декоратор получает класс, а не функцию.
Singleton — это класс с одним экземпляром. Его можно сохранить как атрибут функции-обертки и вернуть при запросе. Это полезно в тех случаях, когда, например, ведется работа с соединением с базой данных.

def singleton(cls):
    '''Класс Singleton (один экземпляр)'''
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton

@singleton
class TheOne:
    pass

print('старт')
first_one = TheOne()
second_one = TheOne()
print(id(first_one))
print(id(second_one))
print('конец')


Результат
старт
56909912
56909912
конец

Декораторы можно использовать для проверки состояния перед выполнение функции: например, зарегистрирован ли пользователь, есть ли у него достаточное количество прав или валидны ли аргументы (типы, значения и так далее).

user_permissions = ["user"]

def check_permission(permission):
    def wrapper_permission(func):
        def wrapped_check():
            if permission not in user_permissions:
                raise ValueError("Недостаточно прав")
            return func()
        return wrapped_check
    return wrapper_permission

@check_permission("user")
def check_value():
    return "значение"

@check_permission("admin")
def do_something():
    return "только админ"

print('старт программы')
check_value()
do_something()
print('конец программы')


2. Решение задач
Задача 1
Выписав первые шесть простых чисел, получим 2, 3, 5, 7, 11 и 13. Очевидно, что 6-е простое число - 13.
Какое число является 10001-м простым числом?


Решение

simple=[3]
number=3
count=3
while count<=10001:
    number+=2
    simpleNuber=True
    for i in simple:
        if number<i**2: #числа кратные i, начинают высчитывать с i(квадрат)
            break
        else:
            if number%i==0:
                simpleNuber=False
                break
    if simpleNuber==True:
        simple.append(number)
        count+=1
print(simple[-1])


Дополнительно
Если на уроке остается время, то ученикам можно предложить начать прорешивать домашнее задание.

Домашняя работа
Задача 1





"""