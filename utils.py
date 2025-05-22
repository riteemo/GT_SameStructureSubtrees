import time


# декоратор для измерения времени работы функций
def timer(foo):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = foo(*args, **kwargs)
        end_time = time.time()
        print(f"Function {foo.__name__} have worked for {end_time - start_time:.6f} sec")
        return result
    return wrapper
