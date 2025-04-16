"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""

from fastapi import APIRouter
from fastapi import Depends

from ibtrading.api.auth_router import authorize, get_authorization_token
from ibtrading.domain import User, ListTradeResponse, ListOrderResponse, ListPortfolioResponse, \
    ListPositionResponse, \
    ListContractResponse, ListAccountResponse, ErrorCode, ListTradeRequest
from ibtrading.domain.webhook import ListWebhookPayloadResponse
from ibtrading.service.helper import get_order_service, get_trade_service
from ibtrading.utils import loggerutil

logger = loggerutil.get_logger(__name__)

router = APIRouter(tags=["Trades"])


@router.get("/api/v1/trades", response_model=ListTradeResponse)
async def list_trades(authorization: str = Depends(get_authorization_token)):
    try:
        req = ListTradeRequest(authorization=authorization)
        return await get_trade_service().list_trades(req)
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListTradeResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.get("/api/v1/orders", response_model=ListOrderResponse)
async def list_orders(user: User = Depends(authorize)):
    try:
        return await get_order_service().list_orders()
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListOrderResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.get("/api/v1/portfolios", response_model=ListPortfolioResponse)
async def list_portfolio(user: User = Depends(authorize)):
    try:
        return await get_order_service().list_portfolio()
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListPortfolioResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.get("/api/v1/positions", response_model=ListPositionResponse)
async def list_position(user: User = Depends(authorize)):
    try:
        return await get_order_service().list_position()
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListPositionResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.get("/api/v1/contracts", response_model=ListContractResponse)
async def list_contracts(user: User = Depends(authorize)):
    try:
        return await get_order_service().list_contracts()
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListContractResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.get("/api/v1/account", response_model=ListAccountResponse)
async def list_account_summary(user: User = Depends(authorize)):
    try:
        return await  get_order_service().list_account_summary()
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListAccountResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))


@router.get("/api/v1/webhooklogs", response_model=ListWebhookPayloadResponse)
async def list_webhooklogs(user: User = Depends(authorize)):
    try:
        return await get_order_service().list_webhook_logs()
    except Exception as e:
        logger.exception(f"Error: {e}")
        return ListWebhookPayloadResponse(error=True, code=ErrorCode.INTERNAL_ERROR, message=str(e))
