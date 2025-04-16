"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 27/02/2025
"""
from ib_async import Contract

from ibtrading.domain.contract import ContractData


def map2ib_contract(contract: ContractData) -> Contract:
    c = Contract(conId=contract.contract_id, secType=contract.sec_type, symbol=contract.symbol,
                 lastTradeDateOrContractMonth=contract.last_trade_date_or_contract_month,
                 strike=contract.strike, right=contract.right, exchange=contract.exchange, currency=contract.currency,
                 multiplier=contract.multiplier, localSymbol=contract.local_symbol,
                 tradingClass=contract.trading_class)
    return c
