"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/03/2025
"""
from collections import OrderedDict

from ibtrading.domain import ListTradeRequest, \
    ListTradeResponse, TradeData
from ibtrading.repo.trade_repo import TradeRepo
from ibtrading.service.service_base import ServiceBase
from ibtrading.settings import Settings
from ibtrading.utils import loggerutil, tradeutil


class TradeService(ServiceBase):
    def __init__(self, trade_repo: TradeRepo, auth_service=None):
        super().__init__(auth_service=auth_service)
        self.trade_repo = trade_repo
        self.logger = loggerutil.get_logger(self.__class__.__name__)
        self.tz = Settings.TIMEZONE

    def calculate_cumulative_pnl(self, trades) -> list[TradeData]:
        cum_pnl = 0
        cum_commission = 0
        trade_groups = OrderedDict()
        processed_trades = []
        for trade in trades:
            key = trade.trade_id if trade.trade_id and trade.trade_id > 0 else trade.order_id
            trade_groups.setdefault(key, []).append(trade)

        for _key, _trades in trade_groups.items():
            if len(_trades) == 1:
                processed_trades.append(_trades[0])
                continue
            t = _trades[0]
            cum_pnl += t.total_pnl
            cum_commission += t.total_commission
            entry_price = 0
            for _trade in _trades:
                if _trade.market_action and _trade.market_action.startswith("ENTRY"):
                    entry_price += _trade.avg_price * _trade.quantity

            total_pnl_percent = t.total_pnl / entry_price * 100
            for _trade in _trades:
                _trade.total_pnl_percent = total_pnl_percent
                _trade.cumulative_pnl = cum_pnl
                _trade.cumulative_commission = cum_commission
                processed_trades.append(_trade)
        return processed_trades

    def calculate_cumulative_pnl_groups(self, trades) -> list[list[TradeData]]:
        cum_pnl = 0
        cum_commission = 0
        trade_groups = OrderedDict()
        processed_trades = []
        for trade in trades:
            key = trade.trade_id if trade.trade_id and trade.trade_id > 0 else trade.order_id
            trade_groups.setdefault(key, []).append(trade)

        for _key, _trades in trade_groups.items():
            if len(_trades) == 1:
                processed_trades.append([_trades[0]])
                continue
            t = _trades[0]
            cum_pnl += t.total_pnl
            cum_commission += t.total_commission
            entry_price = 0
            for _trade in _trades:
                if _trade.market_action and _trade.market_action.startswith("ENTRY"):
                    entry_price += _trade.avg_price * _trade.quantity

            total_pnl_percent = t.total_pnl / entry_price * 100 if entry_price != 0 else 0
            _trades_processed = []
            for _trade in _trades:
                _trade.total_pnl_percent = round(total_pnl_percent, 2)
                _trade.cumulative_pnl = round(cum_pnl, 2)
                _trade.cumulative_commission = round(cum_commission, 2)
                _trades_processed.append(_trade)
            processed_trades.append(_trades_processed)
        return processed_trades

    async def list_trades(self, req: ListTradeRequest) -> ListTradeResponse:
        self.logger.info("List trade request: %s", req)
        authres = self.auth_service.authorize(req.authorization)
        if authres.error:
            return ListTradeResponse(error=True, code=authres.code, message=authres.message)
        trades = self.trade_repo.list_trades_v2(filter=req.filter)
        grouped_trades = self.calculate_cumulative_pnl_groups(trades)
        flattened_trades = tradeutil.flatten(grouped_trades)

        res = ListTradeResponse(trades=flattened_trades, grouped_trades=grouped_trades)
        return res

    async def list_trades_v0(self, req: ListTradeRequest) -> ListTradeResponse:
        self.logger.info("List trade request: %s", req)
        authres = self.auth_service.authorize(req.authorization)
        if authres.error:
            return ListTradeResponse(error=True, code=authres.code, message=authres.message)
        trades = self.trade_repo.list_trades_v1(filter=req.filter)
        grouped_trades = self.calculate_cumulative_pnl_groups(trades)
        flattened_trades = tradeutil.flatten(grouped_trades)

        res = ListTradeResponse(trades=flattened_trades, grouped_trades=grouped_trades)
        return res
