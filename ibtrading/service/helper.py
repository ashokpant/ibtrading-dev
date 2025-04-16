"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""

from ibtrading.repo.datasource import DataSource
from ibtrading.repo.order_repo import OrderRepo
from ibtrading.repo.trade_repo import TradeRepo
from ibtrading.service.auth_service import AuthService
from ibtrading.service.order_service_v1 import OrderService
from ibtrading.service.trade_service import TradeService

TV_WEBHOOK_PROCESSOR = None
IBKR_SERVICE = None
AUTH_SERVICE = None
ORDER_SERVICE = None
TRADE_SERVICE = None
OPTION_SERVICE = None
DATASOURCE = None


def get_datasource() -> DataSource:
    global DATASOURCE
    if DATASOURCE is None:
        DATASOURCE = DataSource()
    return DATASOURCE


def get_order_service() -> OrderService:
    global ORDER_SERVICE
    if ORDER_SERVICE is None:
        db = get_datasource()
        order_repo = OrderRepo(db)
        ORDER_SERVICE = OrderService(order_repo, auth_service=get_auth_service())
    return ORDER_SERVICE


def get_trade_service() -> TradeService:
    global TRADE_SERVICE
    if TRADE_SERVICE is None:
        db = get_datasource()
        repo = TradeRepo(db)

        TRADE_SERVICE = TradeService(trade_repo=repo, auth_service=get_auth_service())
    return TRADE_SERVICE


def get_auth_service() -> AuthService:
    global AUTH_SERVICE
    if AUTH_SERVICE is None:
        AUTH_SERVICE = AuthService()
    return AUTH_SERVICE
