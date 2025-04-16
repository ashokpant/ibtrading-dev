"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/02/2025
"""
from typing import List

from ib_async import Trade
from ib_async.util import UNSET_DOUBLE

from ibtrading.domain import PortfolioData
from ibtrading.domain.account import AccountValueData
from ibtrading.domain.contract import ContractData
from ibtrading.domain.order import OrderData
from ibtrading.domain.order import OrderDirection, OrderType, OrderStatus
from ibtrading.domain.trade import TradeData
from ibtrading.utils import strutil, dtutil


def map_trade(trade: Trade, market_action: str = None) -> TradeData:
    # (market_action, trade)
    print("tradetradetrade: ", trade, market_action)
    t = TradeData()

    contract = map_contract(trade.contract)
    order = map_order(trade.order)

    if market_action is not None:
        order.market_action = market_action
        t.market_action = market_action

    order.contract = contract
    order.contract_id = contract.contract_id
    order.status = OrderStatus(trade.orderStatus.status)
    if len(trade.log) > 0:
        log = trade.log[-1]
        order.message = log.message
        order.error_code = str(log.errorCode)
        order.order_time = dtutil.convert_to_default_tz(log.time)

    t.order_id = order.perm_id if order.perm_id > 0 else order.order_id
    t.client_id = order.client_id
    t.account_id = order.account_id
    t.direction = order.direction
    t.order_type = order.order_type
    t.contract_id = contract.contract_id
    t.status = order.status
    t.trade_time = order.order_time

    fills = trade.fills

    if len(fills) > 0:
        price = 0
        avg_price = 0
        commission = 0
        quantity = 0
        for fill in fills:
            price += fill.execution.price
            avg_price += fill.execution.avgPrice
            commission += fill.commissionReport.commission
            quantity += fill.execution.shares
        t.quantity = quantity
        t.price = price / len(fills)
        t.avg_price = avg_price / len(fills)
        t.commission = commission

    t.contract = contract
    t.order = order
    return t


#
# def map_order(trade, ref_id: int = None) -> OrderData:
#     o = OrderData()
#     o.order_id = trade.order.orderId
#     o.perm_id = trade.orderStatus.permId
#     o.client_id = trade.order.clientId
#     o.account_id = trade.order.account
#     o.direction = OrderDirection.from_ib(trade.order.action)
#     o.order_type = OrderType.from_ib(trade.order.orderType)
#     o.contract_id = trade.contract.conId
#
#     if trade.order.lmtPrice != UNSET_DOUBLE:
#         o.limit_price = trade.order.lmtPrice
#     if trade.order.auxPrice != UNSET_DOUBLE:
#         o.stop_price = trade.order.auxPrice
#     if trade.order.trailingPercent != UNSET_DOUBLE:
#         o.trailing_percent = trade.order.trailingPercent
#     if trade.order.trailStopPrice != UNSET_DOUBLE:
#         o.trail_stop_price = trade.order.trailStopPrice
#     if trade.order.percentOffset != UNSET_DOUBLE:
#         o.percent_offset = trade.order.percentOffset
#
#     o.tif = trade.order.tif
#     o.price = trade.order.lmtPrice
#     o.quantity = trade.order.totalQuantity
#     o.filled_quantity = trade.filled()
#     o.remaining_quantity = trade.remaining()
#     o.status = OrderStatus(trade.orderStatus.status)
#
#     if len(trade.log) > 0:
#         log = trade.log[-1]
#         o.message = log.message
#         o.error_code = str(log.errorCode)
#         o.order_time = log.time
#
#     if ref_id is not None:
#         o.ref_id = ref_id
#     o.is_active = trade.isActive()
#     return o


def map_order(order) -> OrderData:
    o = OrderData()
    o.order_id = order.orderId
    o.perm_id = order.permId
    o.client_id = order.clientId
    o.account_id = order.account
    o.direction = OrderDirection.from_ib(order.action)
    o.order_type = OrderType.from_ib(order.orderType)

    if order.lmtPrice != UNSET_DOUBLE:
        o.limit_price = order.lmtPrice
    if order.auxPrice != UNSET_DOUBLE:
        o.stop_price = order.auxPrice
    if order.trailingPercent != UNSET_DOUBLE:
        o.trailing_percent = order.trailingPercent
    if order.trailStopPrice != UNSET_DOUBLE:
        o.trail_stop_price = order.trailStopPrice
    if order.percentOffset != UNSET_DOUBLE:
        o.percent_offset = order.percentOffset

    o.tif = order.tif
    o.price = order.lmtPrice
    o.quantity = order.totalQuantity
    if order.filledQuantity != UNSET_DOUBLE:
        o.filled_quantity = order.filledQuantity

    o.remaining_quantity = o.quantity - o.filled_quantity
    return o


def map_trades(trades: List[tuple[str, Trade]]) -> List[TradeData]:
    return [map_trade(trade=t[1], market_action=t[0]) for t in trades]


def inject_data_to_trade(trade: TradeData, ref_id: str) -> TradeData:
    trade.order.ref_id = ref_id
    return trade


def inject_data_to_trades(trades: List[TradeData], ref_id: str) -> List[TradeData]:
    return [inject_data_to_trade(t, ref_id) for t in trades]


def map_portfolio(portfolio) -> PortfolioData:
    p = PortfolioData()
    p.account_id = portfolio.account
    p.contract_id = portfolio.contract.conId
    p.position = portfolio.position
    p.market_price = portfolio.marketPrice
    p.market_value = portfolio.marketValue
    p.average_cost = portfolio.averageCost
    p.unrealized_pnl = portfolio.unrealizedPNL
    p.realized_pnl = portfolio.realizedPNL
    p.contract = map_contract(portfolio.contract)
    return p


def map_position2portfolio(position) -> PortfolioData:
    p = PortfolioData()
    p.account_id = position.account
    p.contract_id = position.contract.conId
    p.position = position.position
    p.average_cost = position.avgCost
    p.contract = map_contract(position.contract)
    return p


def map_contract(contract) -> ContractData:
    c = ContractData()
    c.contract_id = contract.conId
    c.symbol = contract.symbol
    c.sec_type = contract.secType
    c.exchange = contract.exchange
    c.currency = contract.currency
    c.last_trade_date_or_contract_month = contract.lastTradeDateOrContractMonth
    c.multiplier = contract.multiplier
    c.local_symbol = contract.localSymbol
    c.trading_class = contract.tradingClass
    c.strike = contract.strike
    c.right = contract.right
    c.exchange = contract.exchange if strutil.is_not_empty(contract.exchange) else contract.primaryExchange
    c.description = contract.description
    c.vt_symbol = c.get_vt_symbol()
    return c


def map_account_value(account_value):
    a = AccountValueData()
    a.account_id = account_value.account
    a.tag = account_value.tag
    a.value = account_value.value
    a.currency = account_value.currency
    a.model_code = account_value.modelCode
    return a
