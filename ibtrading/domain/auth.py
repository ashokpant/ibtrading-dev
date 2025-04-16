"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""
from datetime import datetime

from pydantic import BaseModel

from ibtrading.domain.commons import BaseResponse
from ibtrading.domain.user import User


class Session(BaseModel):
    access_token: str = None
    token_type: str = None
    ttl: int = 0
    expiry: datetime = None
    username: str = None
    role: str = None
    user: User = None


class LoginResponse(BaseResponse):
    session: Session = None


class LogoutResponse(BaseResponse):
    pass


class AuthResponse(BaseResponse):
    session: Session = None
