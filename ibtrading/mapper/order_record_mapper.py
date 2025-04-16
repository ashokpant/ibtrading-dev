"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/02/2025
"""
from ibtrading import domain
from ibtrading.model.account_value_record import AccountValueRecord
from ibtrading.model.contract_record import ContractRecord
from ibtrading.model.order_record import OrderRecord
from ibtrading.model.portfolio_record import PortfolioRecord
from ibtrading.model.trade_record import TradeRecord
from ibtrading.model.webhook_record import WebhookRecord


def map2trade_record(trade: domain.TradeData) -> TradeRecord:
    t = TradeRecord()
    t.trade_id = trade.trade_id
    t.order_id = trade.order_id
    t.client_id = trade.client_id
    t.account_id = trade.account_id
    t.contract_id = trade.contract_id
    t.direction = trade.direction
    if trade.market_action:
        t.market_action = trade.market_action
    t.price = trade.price
    t.avg_price = trade.avg_price
    t.quantity = trade.quantity
    t.trade_time = trade.trade_time.replace(tzinfo=None) if trade.trade_time else None
    t.status = trade.status
    t.pnl = trade.pnl
    t.commission = trade.commission
    t.released_pnl = trade.released_pnl
    t.unrealized_pnl = trade.unrealized_pnl
    t.total_pnl = trade.total_pnl
    t.total_commission = trade.total_commission

    if trade.order:
        t.order = map2order_record(trade.order)
    if trade.contract:
        t.contract = map2contract_record(trade.contract)
    return t


def map2trade_data(trade: TradeRecord, order: OrderRecord, contract: ContractRecord,
                   webhook_log: WebhookRecord) -> domain.TradeData:
    t = domain.TradeData()
    t.id = trade.id
    t.trade_id = trade.trade_id
    t.order_id = trade.order_id
    t.client_id = trade.client_id
    t.account_id = trade.account_id
    t.contract_id = trade.contract_id
    t.direction = trade.direction
    # t.market_action = trade.market_action
    t.price = trade.price
    t.avg_price = trade.avg_price
    t.quantity = trade.quantity
    t.trade_time = trade.trade_time
    t.status = trade.status
    t.pnl = trade.pnl
    t.commission = trade.commission
    t.released_pnl = trade.released_pnl
    t.unrealized_pnl = trade.unrealized_pnl
    t.total_pnl = trade.total_pnl
    t.total_commission = trade.total_commission

    if order:
        o = order
    else:
        o = trade.order
    t.order = map2order_data(order=o, contract=contract, webhook_log=webhook_log)
    t.market_action = t.order.market_action
    t.contract = t.order.contract
    t.order.contract = None
    t.created_at = trade.created_at
    t.updated_at = trade.updated_at
    return t


def map2order_record(order: domain.OrderData) -> OrderRecord:
    o = OrderRecord()
    o.order_id = order.order_id
    o.perm_id = order.perm_id
    o.client_id = order.client_id
    o.account_id = order.account_id
    o.contract_id = order.contract_id
    o.ref_id = order.ref_id
    o.direction = order.direction
    if order.market_action:
        o.market_action = order.market_action
    o.order_type = order.order_type
    o.order_time = order.order_time
    o.stop_price = order.stop_price
    o.limit_price = order.limit_price
    o.trailing_percent = order.trailing_percent
    o.percent_offset = order.percent_offset
    o.tif = order.tif
    o.status = order.status
    o.quantity = order.quantity
    o.filled_quantity = order.filled_quantity
    o.remaining_quantity = order.remaining_quantity
    o.avg_fill_price = order.avg_fill_price
    o.is_active = order.is_active
    o.message = order.message
    o.error_code = order.error_code
    return o


def map2order_data(order: OrderRecord, contract: ContractRecord,
                   webhook_log: WebhookRecord) -> domain.OrderData:
    o = domain.OrderData()
    o.order_id = order.order_id
    o.perm_id = order.perm_id
    o.client_id = order.client_id
    o.account_id = order.account_id
    o.contract_id = order.contract_id
    o.ref_id = order.ref_id
    o.direction = order.direction
    o.market_action = order.market_action
    o.order_type = order.order_type
    o.order_time = order.order_time
    o.stop_price = order.stop_price
    o.limit_price = order.limit_price
    o.trailing_percent = order.trailing_percent
    o.percent_offset = order.percent_offset
    o.tif = order.tif
    o.status = order.status
    o.quantity = order.quantity
    o.filled_quantity = order.filled_quantity
    o.remaining_quantity = order.remaining_quantity
    o.avg_fill_price = order.avg_fill_price
    o.is_active = order.is_active
    o.message = order.message
    o.error_code = order.error_code
    if webhook_log:
        o.ref_data = map2_ref_data(webhook_log)
    if contract:
        c = contract
    else:
        c = order.contract
    o.contract = map2contract_data(c)
    return o


def map2_ref_data(webhook_log: WebhookRecord):
    if webhook_log.id is None or webhook_log.id == 0 and webhook_log is None:
        return None
    d = domain.RefData()
    d.id = webhook_log.id
    d.ref_id = webhook_log.ref_id
    d.vt_symbol = webhook_log.vt_symbol
    d.dt = webhook_log.dt
    d.open = webhook_log.open
    d.high = webhook_log.high
    d.low = webhook_log.low
    d.close = webhook_log.close
    d.volume = webhook_log.volume
    d.action = webhook_log.action
    d.market_action = webhook_log.market_action
    d.market_position = webhook_log.market_position
    d.market_position_size = webhook_log.market_position_size
    d.message = webhook_log.message
    d.created_at = webhook_log.created_at
    return d


def map2contract_record(contract: domain.ContractData) -> ContractRecord:
    c = ContractRecord()
    c.id = contract.id
    c.contract_id = contract.contract_id
    c.sec_type = contract.sec_type
    c.symbol = contract.symbol
    c.last_trade_date_or_contract_month = contract.last_trade_date_or_contract_month
    c.strike = contract.strike
    c.right = contract.right
    c.multiplier = contract.multiplier
    c.exchange = contract.exchange
    c.currency = contract.currency
    c.local_symbol = contract.local_symbol
    c.trading_class = contract.trading_class
    c.include_expired = contract.include_expired
    c.sec_id_type = contract.sec_id_type
    c.sec_id = contract.sec_id
    c.description = contract.description
    c.issuer_id = contract.issuer_id
    c.combo_legs_desc = contract.combo_legs_desc
    c.combo_legs = contract.combo_legs
    c.delta_neutral_contract = contract.delta_neutral_contract
    c.vt_symbol = contract.vt_symbol
    return c


def map2contract_data(contract: ContractRecord):
    if contract is None:
        return None
    c = domain.ContractData()
    c.id = contract.id
    c.contract_id = contract.contract_id
    c.sec_type = contract.sec_type
    c.symbol = contract.symbol
    c.last_trade_date_or_contract_month = contract.last_trade_date_or_contract_month
    c.strike = contract.strike
    c.right = contract.right
    c.multiplier = contract.multiplier
    c.exchange = contract.exchange
    c.currency = contract.currency
    c.local_symbol = contract.local_symbol
    c.trading_class = contract.trading_class
    c.include_expired = contract.include_expired
    c.sec_id_type = contract.sec_id_type
    c.sec_id = contract.sec_id
    c.description = contract.description
    c.issuer_id = contract.issuer_id
    c.combo_legs_desc = contract.combo_legs_desc
    c.combo_legs = contract.combo_legs
    c.delta_neutral_contract = contract.delta_neutral_contract
    c.vt_symbol = contract.vt_symbol
    c.created_at = contract.created_at
    c.updated_at = contract.updated_at
    return c


def map2portfolio_record(portfolio):
    p = PortfolioRecord()
    p.account_id = portfolio.account_id
    p.contract_id = portfolio.contract_id
    p.position = portfolio.position
    p.market_price = portfolio.market_price
    p.market_value = portfolio.market_value
    p.average_cost = portfolio.average_cost
    p.unrealized_pnl = portfolio.unrealized_pnl
    p.realized_pnl = portfolio.realized_pnl
    if portfolio.contract:
        p.contract = map2contract_record(portfolio.contract)
    return p


def map2portfolio_data(portfolio, contract=None):
    p = domain.PortfolioData()
    p.id = portfolio.id
    p.account_id = portfolio.account_id
    p.contract_id = portfolio.contract_id
    p.position = portfolio.position
    p.market_price = portfolio.market_price
    p.market_value = portfolio.market_value
    p.average_cost = portfolio.average_cost
    p.unrealized_pnl = portfolio.unrealized_pnl
    p.realized_pnl = portfolio.realized_pnl
    if contract is not None:
        p.contract = map2contract_data(contract)
    elif portfolio.contract:
        p.contract = map2contract_data(portfolio.contract)
    return p


# def map2position_record(position):
#     p = PositionRecord()
#     p.account_id = position.account_id
#     p.contract_id = position.contract_id
#     p.position = position.position
#     p.average_cost = position.average_cost
#     if position.contract:
#         p.contract = map2contract_record(position.contract)
#     return p


# def map2position_data(position, contract=None):
#     p = domain.PositionData()
#     p.id = position.id
#     p.account_id = position.account_id
#     p.contract_id = position.contract_id
#     p.position = position.position
#     p.average_cost = position.average_cost
#     p.created_at = position.created_at
#     p.updated_at = position.updated_at
#     if contract is not None:
#         c = contract
#     else:
#         c = position.contract
#     p.contract = map2contract_data(c)
#     return p


def map2account_value_record(account_value):
    a = AccountValueRecord()
    a.account_id = account_value.account_id
    a.tag = account_value.tag
    a.value = account_value.value
    a.currency = account_value.currency
    a.model_code = account_value.model_code
    return a


def map2account_value_data(account_value):
    a = domain.AccountValueData()
    a.account_id = account_value.account_id
    a.tag = account_value.tag
    a.value = account_value.value
    a.currency = account_value.currency
    a.model_code = account_value.model_code
    return a
