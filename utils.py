from memory_profiler import memory_usage
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


# декоратор для измерения пикового потребления памяти функцией
def memory_timer(foo):
    def wrapper(*args, **kwargs):
        mem_usage = memory_usage((foo, args, kwargs), max_usage=True) * 1.048576
        print(f"Function {foo.__name__} peak memory usage: {mem_usage:.6f} MB")
        return foo(*args, **kwargs)
    return wrapper
