"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/02/2025
"""
import asyncio
from datetime import datetime

import nest_asyncio
from ib_async import util

nest_asyncio.apply()
from ibtrading.domain import WebhookPayload, GetMarketPriceRequest
from ibtrading.repo.datasource import DataSource
from ibtrading.repo.order_repo import OrderRepo
from ibtrading.service.ibkr_service import IBKRService
from ibtrading.service.order_service import OrderService


def place_order_example():
    ibkr_service = IBKRService(client_id=18)
    util.run(ibkr_service.connect())
    db = DataSource()
    order_repo = OrderRepo(db)
    order_service = OrderService(ibkr_service, order_repo)
    req = WebhookPayload(
        action="BUY",
        contracts=1,
        symbol="NQ1!",
        position_size=1,
        market_position="LONG",
        market_position_size=1,
        time=datetime.now(),
        close=21660.0,
        open=21660.0,
        high=21660.0,
        low=21660.0,
        volume=1,
        timeframe="1D",
        exchange="CME",
        timenow=datetime.now(),
        currency="USD",
        sec_type="CONTFUT",
        last_trade_date_or_contract_month="20250321",
        message="Test message",
        order_type="MARKET",
        strategy="Test strategy",
        metadata={}
    )
    print(req)
    res = order_service.place_order(req)
    print(res)


async def market_price_example():
    ibkr_service = IBKRService(client_id=19)
    # util.run(ibkr_service.connect())
    db = DataSource()
    order_repo = OrderRepo(db)
    order_service = OrderService(ibkr_service, order_repo)

    req = GetMarketPriceRequest(contract_id=769043285)
    res = await order_service.get_market_price(req)
    print(res)


if __name__ == '__main__':
    asyncio.run(market_price_example())
