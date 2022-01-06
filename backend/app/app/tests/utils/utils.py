import random
import string
import sys
from typing import Dict, List, Union


def random_int(start: int = 0, end: int = sys.maxsize):
    return random.randint(start, end)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_alphanumeric() -> Union[str, int]:
    if random.choice((True, False)):
        return random_lower_string()
    return random.randint(-99, 99)


def random_list() -> List[int]:
    return random.sample(range(-99, 99), random.randint(0, 5))


def random_dict() -> Dict[str, Union[str, int]]:
    return {
        random_lower_string(): random_alphanumeric()
        for _ in range(random.randint(0, 3))
    }
