import string
import random

def get_random_string(length: int, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(length))

def get_unique_name(normal_name):
    snake_case_name = normal_name.replace(" ", "_").lower()
    random_str = get_random_string(6)
    return snake_case_name + random_str
