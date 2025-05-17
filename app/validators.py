import re
import datetime


def is_valid_first_name(name: str) -> bool:
    pattern = r'^[А-Яа-яA-Za-z\- \']{2,50}$'
    return bool(re.fullmatch(pattern, name))


def is_valid_second_name(second_name: str) -> bool:
    pattern = r'^[А-Яа-яA-Za-z\- \']{2,50}$'
    return bool(re.fullmatch(pattern, second_name))


def is_valid_phone_number(number: str) -> bool:
    pattern = r'^(\+7|8)\d{10}$'
    return bool(re.fullmatch(pattern, number))


def is_valid_event_date(date_str: str) -> bool:
    pattern = r'^(?:\d{4}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4})\s\d{2}:\d{2}:\d{2}$'
    if not re.fullmatch(pattern, date_str):
        return False
    try:
        if '.' in date_str:
            datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
        else:
            datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def is_valid_location(location: str) -> bool:
    pattern = r'^[А-Яа-яA-Za-z0-9\s,.-]{2,100}$'
    return bool(re.fullmatch(pattern, location.strip()))


def is_valid_event_name(event_name: str) -> bool:
    pattern = r'^[А-Яа-яA-Za-z0-9\s-]{2,200}$'
    return bool(re.fullmatch(pattern, event_name.strip()))


def is_valid_attendees_count(count: str) -> bool:
    pattern = r'^\d+$'
    if not re.fullmatch(pattern, count):
        return False
    try:
        num = int(count)
        return num > 0
    except ValueError:
        return False

