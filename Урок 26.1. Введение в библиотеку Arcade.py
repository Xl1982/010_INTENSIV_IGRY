import datetime

def measure(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        elapsed = end - start
        print(f"РІСЂРµРјСЏ РІС‹РїРѕР»РЅРµРЅРёСЏ С„СѓРЅРєС†РёРё '{func.__name__}': {elapsed}")
        return result
    return wrapper