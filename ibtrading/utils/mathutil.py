"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 07/04/2025
"""
import bisect


def find_value(sorted_values, target, lower=True):
    if lower:
        index = bisect.bisect_left(sorted_values, target)
        return sorted_values[index - 1] if index > 0 else None
    else:
        index = bisect.bisect_right(sorted_values, target)
        return sorted_values[index] if index < len(sorted_values) else None
