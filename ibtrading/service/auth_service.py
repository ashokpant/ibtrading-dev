"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""
from datetime import datetime, timedelta
from typing import Dict, Optional

import bcrypt
import jwt

from ibtrading.domain import User, LogoutResponse, LoginResponse, ErrorCode
from ibtrading.domain.auth import Session, AuthResponse
from ibtrading.domain.user import UserWithPassword
from ibtrading.utils import loggerutil
from ibtrading.utils.singleton import Singleton

JWT_SECRET_KEY = "secret@543"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_SECONDS = 7 * 24 * 60 * 60

logger = loggerutil.get_logger(__name__)


class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def add_session(self, username: str, token: str, expires: datetime):
        self.sessions[token] = Session(username=username, expiry=expires, access_token=token)

    def get_session(self, token: str = None) -> Optional[Session]:
        session = self.sessions.get(token, None)
        if session and session.expiry < datetime.now():
            self.remove_session(token)
            return None
        return session

    def remove_session(self, token: str):
        return self.sessions.pop(token, None)

    def cleanup_expired(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired = [
            token for token, session in self.sessions.items()
            if session.expiry < current_time
        ]
        for token in expired:
            self.remove_session(token)


class AuthService(metaclass=Singleton):
    _instance = None

    def __init__(self):
        if AuthService._instance is not None:
            return
        self.users = {}
        self.users["admin"] = UserWithPassword(
            user=User(username="admin", full_name="Admin", role="admin", active=True),
            hashed_password=self.hash_password("Admin@321"))
        self.users["ashok"] = UserWithPassword(
            user=User(username="ashok", full_name="Ashok Pant", role="admin", active=True),
            hashed_password=self.hash_password("Ashok@321"))
        self.users["test"] = UserWithPassword(
            user=User(username="test", full_name="Test User", role="user", active=True),
            hashed_password=self.hash_password("Test@321"))

        self.api_keys = {"APIKEY123": {"role": "admin"}, "APIKEY456": {"role": "admin"}}
        self.session_store = SessionStore()

    def get_user(self, username: str) -> Optional[User]:
        uwp = self.users.get(username, None)
        if uwp is None:
            return None
        return uwp.user

    def _get_password(self, username: str):
        uwp = self.users.get(username, None)
        if uwp is None:
            return None
        return uwp.hashed_password

    def get_api_key(self, api_key: str):
        return self.api_keys.get(api_key, None)

    def login(self, username: str, password: str) -> LoginResponse:
        user = self.get_user(username)
        if user is None:
            return LoginResponse(error=True, code=ErrorCode.UNAUTHORIZED, message="Invalid username")
        _password = self._get_password(username)
        if not self.verify_password(password, _password):
            return LoginResponse(error=True, code=ErrorCode.UNAUTHORIZED, message="Invalid password")
        session = self._create_access_token(username)
        session.user = user
        session.role = user.role
        return LoginResponse(error=False, session=session)

    def _create_access_token(self, username: str, expires_delta: timedelta = None) -> Session:
        expire = datetime.now() + (expires_delta or timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRE_SECONDS))
        to_encode = dict({"sub": username, "exp": expire})
        token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        self.session_store.add_session(username=username, token=token, expires=expire)
        session = Session(access_token=token, token_type="bearer", ttl=JWT_ACCESS_TOKEN_EXPIRE_SECONDS, expiry=expire,
                          username=username)
        return session

    def hash_password(self, password):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    def verify_password(self, plain_password, hashed_password):
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

    def _decode_jwt(self, token):
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            logger.exception(f"Error decoding JWT token: {e}")
            return None

    def _authorize(self, token: str) -> (ErrorCode, str, Session):
        try:
            if token is None or token == "" or token == "null":
                return ErrorCode.UNAUTHORIZED, "Invalid token", None

            payload = self._decode_jwt(token)
            if payload is None:
                return ErrorCode.UNAUTHORIZED, "Invalid token", None

            session = self.session_store.get_session(token)
            if not session or session.access_token != token:
                return ErrorCode.UNAUTHORIZED, "Unauthorized", None

            username = payload.get("sub")
            user = self.get_user(username)
            if user is None:
                return ErrorCode.UNAUTHORIZED, "Invalid token", None
            session.user = user
            session.role = user.role
            return None, None, session
        except jwt.ExpiredSignatureError:
            return ErrorCode.UNAUTHORIZED, "Token has expired", None
        except jwt.PyJWKError:
            return ErrorCode.UNAUTHORIZED, "Invalid token", None

    def authorize(self, token: str) -> AuthResponse:
        try:
            if token is None or token == "":
                return AuthResponse(error=True, code=ErrorCode.UNAUTHORIZED, message="Invalid token")
            code, msg, session = self._authorize(token)
            if code is not None:
                return AuthResponse(error=True, code=code, message=msg)
            return AuthResponse(error=False, session=session)
        except Exception as e:
            logger.exception(f"Error authorizing token: {e}")
            return AuthResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))

    def logout(self, token):
        session = self.session_store.remove_session(token)
        if session is None:
            return LogoutResponse(error=True, code=ErrorCode.NOT_FOUND, message="Session not found")
        return LogoutResponse(error=False)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AuthService()
        return cls._instance
