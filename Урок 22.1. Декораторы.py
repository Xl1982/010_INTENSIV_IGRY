import time

def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(start_time)
        result = func(*args, **kwargs)
        end_time = time.time()
        print(end_time)
        print(f'Время выполнения функции {func.__name__} : {end_time - start_time:.4f} секунд')
        return result
    return wrapper


def memory(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(start_time)
        result = func(*args, **kwargs)
        end_time = time.time()
        print(end_time)
        print(f'Время выполнения функции {func.__name__} : {end_time - start_time:.4f} секунд')
        return result
    return wrapper

#@decorator
def basic(duration):
    time.sleep(duration)
    input("Имя")
    input('age')
    print("основная функция")

basic(2)



