import string
import uuid

from django.db.models import Model

from typing import Any

def get_random_alpha_numeric_string(length: int, chars=string.ascii_uppercase + string.digits) -> str:
    return uuid.uuid4().hex[:length].upper()

def get_unique_name(name: str, random_length: int = None) -> str:
    length = random_length or 6
    snake_case_name = name.replace(" ", "_").lower()
    random_str = get_random_alpha_numeric_string(length)
    return snake_case_name + random_str

def object_unique_name_already_exists(name: str, model_cls: Model, excluding_obj: Model):
    return model_cls.objects.filter(unique_name=name).exclude(pk=excluding_obj.pk).exists()
