# Standard module
import time
from typing import Any, Callable, Optional, Union, cast

# Custom module
from logger import logger

def tic_tok(func: Callable) -> Callable:
    # position & keyword argument. The prefix star is meaning Any number.
    def wrapper(*arg, **kwargs) -> Any:
        t1: float = time.time()
        result:Any = func(*arg, **kwargs)
        t2: float = time.time() - t1
        logger.info(f"{func.__name__} took {round(t2, 3)} seconds")
        return result
    return wrapper