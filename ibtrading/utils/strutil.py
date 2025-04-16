"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/02/2025
"""


def is_empty(value):
    return not value or value.strip() == ''


def is_not_empty(value):
    return not is_empty(value)
