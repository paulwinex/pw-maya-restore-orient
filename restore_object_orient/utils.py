import time
from datetime import timedelta

times = {}


def compute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        if duration > 0.001:
            times[func.__qualname__] = duration
        return result
    return wrapper



def show_stat():
    for f, tm in sorted(times.items(), key=lambda x: x[1], reverse=True):
        print(f'{f}: {timedelta(seconds=tm)}')