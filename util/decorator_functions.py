import time
import datetime


def time_elapsed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end - start, " : passed")
    return wrapper

