"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 24/02/2025
"""
import math
from datetime import datetime, timedelta
from typing import Optional

from ibtrading.settings import Settings
from ibtrading.utils import dtutil


def round_to_nearest_int(x, step, lower=False) -> int:
    if lower:
        return int(math.floor(x / step) * step)
    else:
        return int(math.ceil(x / step) * step)


def flatten(nested_list) -> list:
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))  # Recursion for deeper nesting
        else:
            flat_list.append(item)
    return flat_list


