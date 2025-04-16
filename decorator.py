# Standard module
import time
from typing import Any, Callable, Optional, Union, cast
from functools import wraps

# Custom module
from logger import logger

def tic_tok(func: Callable) -> Callable:
    """It's a tic_tok function"""
    # position & keyword argument. The prefix star is meaning Any number.
    def wrapper(*arg, **kwargs) -> Any:
        t1: float = time.time()
        result:Any = func(*arg, **kwargs)
        t2: float = time.time() - t1
        logger.info(f"{func.__name__} took {round(t2, 3)} seconds")
        return result
    return wrapper

class TicTok:
    """It's a TicTok class"""
    def __init__(self, func:Callable):
        self.func = func

        """wraps(func) return a decorator"""
        # 複製func的metadata, __name__, __doc__, __annotations__ ...etc
        wraps(func)(self)
    
    def __call__(self, *args, **kwargs) -> Any:
        t1: float = time.time()
        result:Any = self.func(*args, **kwargs)
        t2: float = time.time() - t1
        logger.info(f"{self.func.__name__} took {round(t2, 3)} seconds")
        return result

@TicTok
def test_func(num):
    """It's a test_func"""
    for i in range(num):
        pass
    return None

if __name__ == "__main__":
    print(test_func.__name__)
    print(test_func.__doc__)
    test_func(1000000)