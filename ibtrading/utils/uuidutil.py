"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 28/02/2025
"""
import hashlib
import time
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_int_uuid() -> int:
    return uuid.uuid4().int


def generate_md5(payload: str):
    md5_hash = hashlib.md5()
    md5_hash.update(str(payload).encode('utf-8'))
    return md5_hash.hexdigest()


def generate_sortable_int_uuid():
    """
    Generate a sortable UUID based on the current timestamp. Might not be unique for same nanosecond operations. Use with caution.
    :return:
    """
    timestamp = int(time.time() * 1000 * 1000 * 1000)
    return timestamp
