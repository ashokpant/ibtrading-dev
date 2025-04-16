"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""

from fastapi import APIRouter
from fastapi import Depends

from ibtrading.api.auth_router import get_authorization_token
from ibtrading.domain import ListTradeRequest, ListTradeResponse, ErrorCode
from ibtrading.service.helper import get_trade_service
from ibtrading.utils import loggerutil

logger = loggerutil.get_logger(__name__)

router = APIRouter(tags=["Trades"])


@router.post("/api/v2/trades", response_model=ListTradeResponse)
async def list_trades_v2(req: ListTradeRequest = ListTradeRequest(),
                         authorization: str = Depends(get_authorization_token)):
    try:
        req.authorization = authorization

        data = await get_trade_service().list_trades(req)
        return data
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListTradeResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))
