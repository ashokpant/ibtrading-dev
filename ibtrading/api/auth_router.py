"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from fastapi.security import OAuth2PasswordRequestForm

from ibtrading.domain import LogoutResponse, Session, ErrorCode
from ibtrading.domain.auth import LoginResponse
from ibtrading.service.helper import get_auth_service
from ibtrading.utils import loggerutil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=True)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

logger = loggerutil.get_logger(__name__)

router = APIRouter(tags=["Auth"])
auth_service = get_auth_service()


async def get_authorization_token(authorization: str = Depends(oauth2_scheme)):
    print("Authorization: ", authorization)
    return authorization


async def authorize(authorization: str = Depends(oauth2_scheme)):
    res = auth_service.authorize(authorization)
    if res.error:
        raise HTTPException(status_code=res.code.value, detail=res.message)
    return res.session.user


#
# async def authorize1(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Missing authorization header")
#
#     scheme, token = authorization.split()
#     if scheme.lower() != 'bearer':
#         raise HTTPException(status_code=401, detail="Invalid authentication scheme")
#
#     code, msg, user = auth_service.authorize(token)
#     if code is not None:
#         raise HTTPException(status_code=code, detail=msg)
#
#     return user


async def api_key_auth(api_key: str = Security(api_key_header)):
    result = auth_service.get_api_key(api_key)
    if result is None:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return {"role": result.get("role", None)}


@router.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = auth_service.login(form_data.username, form_data.password)
        return res
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return LoginResponse(error=True, code=ErrorCode.UNAUTHORIZED, message=str(ve))
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        return LoginResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.post("/api/v1/auth/token", response_model=Session)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = auth_service.login(form_data.username, form_data.password)
        if res.error:
            logger.error(f"Invalid credentials for user: {form_data.username}")
            raise HTTPException(status_code=res.code.value, detail=res.message)
        return res.session
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/auth/logout", response_model=LogoutResponse)
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        return auth_service.logout(token)
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return LogoutResponse(error=True, code=ErrorCode.UNAUTHORIZED, message=str(ve))
    except Exception as e:
        logger.exception(f"Authentication error: {e}")
        return LogoutResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))

#
# @router.get("/api/v1/auth/protected")
# async def protected_route(user: dict = Depends(authorize)):
#     return {"message": f"Hello {user['full_name']}, you have access!"}
#
#
# @router.get("/api/v1/auth/secure-data")
# async def secure_data(user: dict = Depends(api_key_auth)):
#     return {"message": "You have access to secure data"}
