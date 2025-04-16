"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 17/02/2025
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config

from ibtrading.utils import ibutil
from ibtrading.utils.dtutil import datetime_encoder, datetime_from_str


@dataclass_json
@dataclass
class ContractData:
    id: Optional[int] = None
    contract_id: Optional[int] = None
    sec_type: Optional[str] = None
    symbol: Optional[str] = None
    last_trade_date_or_contract_month: Optional[str] = None
    strike: Optional[float] = None
    right: Optional[str] = None
    multiplier: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    local_symbol: Optional[str] = None
    trading_class: Optional[str] = None
    include_expired: Optional[bool] = False
    sec_id_type: Optional[str] = None
    sec_id: Optional[str] = None
    description: Optional[str] = None
    issuer_id: Optional[str] = None
    combo_legs_desc: Optional[str] = None
    combo_legs: Optional[str] = None
    delta_neutral_contract: Optional[str] = None
    vt_symbol: Optional[str] = None
    created_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    updated_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))

    def as_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "sec_type": self.sec_type,
            "symbol": self.symbol,
            "last_trade_date_or_contract_month": self.last_trade_date_or_contract_month,
            "strike": self.strike,
            "right": self.right,
            "multiplier": self.multiplier,
            "exchange": self.exchange,
            "currency": self.currency,
            "local_symbol": self.local_symbol,
            "trading_class": self.trading_class,
            "include_expired": self.include_expired,
            "sec_id_type": self.sec_id_type,
            "sec_id": self.sec_id,
            "description": self.description,
            "issuer_id": self.issuer_id,
            "combo_legs_desc": self.combo_legs_desc,
            "combo_legs": self.combo_legs,
            "delta_neutral_contract": self.delta_neutral_contract,
            "vt_symbol": self.vt_symbol,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def get_vt_symbol(self):
        return ibutil.generate_vt_symbol_v1(symbol=self.symbol, sec_type=self.sec_type,
                                            last_trade_date_or_contract_month=self.last_trade_date_or_contract_month,
                                            strike=self.strike, multiplier=self.multiplier, right=self.right,
                                            currency=self.currency, exchange=self.exchange, )
