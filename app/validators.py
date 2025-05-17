import re

def is_valid_first_name(name: str) -> bool:
    pattern = r'^[А-Яа-яA-Za-z\- \']{2,50}$'
    return bool(re.fullmatch(pattern, name))

def is_valid_second_name(second_name: str) -> bool:
    pattern = r'^[А-Яа-яA-Za-z\- \']{2,50}$'
    return bool(re.fullmatch(pattern, second_name))

def is_valid_phone_number(number: str) -> bool:
    pattern = r'^(\+7|8)\d{10}$'
    return bool(re.fullmatch(pattern, number))

