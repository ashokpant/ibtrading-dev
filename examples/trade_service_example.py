"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/02/2025
"""
import asyncio

import nest_asyncio

from ibtrading.repo.trade_repo import TradeRepo
from ibtrading.service.auth_service import AuthService
from ibtrading.service.trade_service import TradeService
from ibtrading.utils import dtutil

nest_asyncio.apply()
from ibtrading.domain import ListTradeRequest, TradeDataFilter
from ibtrading.repo.datasource import DataSource


async def list_trade_example():
    db = DataSource()
    repo = TradeRepo(db)
    auth_service = AuthService()
    service = TradeService(trade_repo=repo, auth_service=auth_service)
    req = ListTradeRequest(filter=TradeDataFilter(
        symbols=["NQ"],
        security_types=["FOP"],
        from_dt=dtutil.datetime_from_str("2025-04-08T03:00:00"),
        to_dt=dtutil.datetime_from_str("2025-04-08T20:00:00"),
    ))
    print("Req", req)
    res = await service.list_trades(req)
    print(res.error, res.code, res.message)
    for t in res.trades:
        print(
            f"{t.contract.symbol}, {t.contract.sec_type}, {t.trade_id}, {t.trade_time}, {t.created_at}, {t.market_action}, {t.direction}, {t.avg_price:.2f}, {t.quantity}, {t.total_pnl or 0:.2f}, {t.cumulative_pnl or 0:.2f},  {t.total_pnl_percent or 0:.2f}, {t.total_commission or 0:.2f}, {t.cumulative_commission or 0:.2f}")

    await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(list_trade_example())
