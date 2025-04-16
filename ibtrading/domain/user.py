"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 10/03/2025
"""
from pydantic import BaseModel


class User(BaseModel):
    username: str = None
    full_name: str = None
    email: str = None
    role: str = None
    active: bool = False
    profile_pic: str = None


class UserWithPassword(BaseModel):
    user: User = None
    hashed_password: bytes = None
