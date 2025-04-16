"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 27/02/2025
"""
from typing import Optional

from ib_async import Contract

JOIN_SYMBOL: str = "-"


def generate_ib_contract(symbol: str, exchange: str) -> Optional[Contract]:
    ib_contract: Optional[Contract] = None
    if "-" in symbol:
        try:
            fields: list = symbol.split(JOIN_SYMBOL)
            ib_contract: Contract = Contract()
            ib_contract.exchange = exchange
            ib_contract.secType = fields[-1]
            ib_contract.currency = fields[-2]
            ib_contract.symbol = fields[0]

            if ib_contract.secType in ["FUT", "OPT", "FOP"]:
                ib_contract.lastTradeDateOrContractMonth = fields[1]

            if ib_contract.secType == "FUT":
                if len(fields) == 5:
                    ib_contract.multiplier = fields[2]

            if ib_contract.secType in ["OPT", "FOP"]:
                ib_contract.right = fields[2]
                ib_contract.strike = float(fields[3])
                ib_contract.multiplier = fields[4]
        except IndexError:
            ib_contract = None
    else:
        if symbol.isdigit():
            ib_contract: Contract = Contract()
            ib_contract.exchange = exchange
            ib_contract.conId = int(symbol)
        else:
            ib_contract = None

    return ib_contract


def generate_vt_symbol(contract: Contract) -> str:
    return generate_vt_symbol_v1(contract.symbol, contract.secType, contract.lastTradeDateOrContractMonth,
                                 contract.strike, contract.multiplier, contract.right, contract.currency,
                                 contract.exchange)


def generate_vt_symbol_v1(symbol: str, sec_type: str, last_trade_date_or_contract_month: str, strike: float,
                          multiplier: str, right: str, currency: str, exchange: str) -> str:
    print( symbol, sec_type, last_trade_date_or_contract_month, strike, multiplier, right, currency, exchange)
    symbol: str = symbol
    if sec_type in ["FUT", "OPT", "FOP"]:
        symbol += JOIN_SYMBOL + last_trade_date_or_contract_month

    if multiplier is None:
        multiplier = "?"
    if right is None:
        right = "?"
    if strike is None:
        strike = "0"

    if sec_type == "FUT":
        symbol += JOIN_SYMBOL + str(multiplier)

    if sec_type in ["OPT", "FOP"]:
        symbol += JOIN_SYMBOL + right + JOIN_SYMBOL + str(int(strike)) + JOIN_SYMBOL + str(multiplier)

    symbol += JOIN_SYMBOL + currency + JOIN_SYMBOL + sec_type + "." + exchange
    return symbol


def generate_vt_symbol_from_webhook(symbol: str, sec_type: str, last_trade_date_or_contract_month: str, timeframe: str,
                                    currency: str, exchange: str) -> str:
    symbol: str = "WH_" + symbol
    if sec_type in ["FUT", "OPT", "FOP"]:
        symbol += JOIN_SYMBOL + last_trade_date_or_contract_month

    symbol += JOIN_SYMBOL + currency + JOIN_SYMBOL + sec_type + JOIN_SYMBOL + timeframe + "." + exchange
    return symbol
