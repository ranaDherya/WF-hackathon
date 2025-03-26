
import re
from datetime import datetime
from langchain_core.tools import tool

# Generic Validation Functions
def is_integer(value):
    return isinstance(value, int)

def is_whole_number(value):
    return isinstance(value, int) and value >= 0

def is_in_range(value, min_v, max_v):
    return min_v <= value <= max_v

def matches_pattern(value, pattern):
    for pat in pattern:
        if re.fullmatch(pat, str(value)) is not None:
            return True
    return False

def is_in_list(value, allowed_values):
    return value in allowed_values

def is_valid_date(value):
    try:
        date_format="%Y-%m-%d"
        datetime.strptime(value, date_format)
        return True
    except ValueError:
        return False

def is_valid_country_code(value, valid_codes):
    return value in valid_codes

def no_nonprintable_chars(value):
    return not bool(re.search(r"[\x00-\x1F\x7F]", value))