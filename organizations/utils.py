import string
import random

def get_random_string(length: int, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(length))
