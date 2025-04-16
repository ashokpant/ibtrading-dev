"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/01/2025
"""

import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config

from ibtrading.domain import ContractData
from ibtrading.utils.dtutil import datetime_encoder, datetime_from_str


class OptionType(enum.Enum):
    CALL = "CALL"
    PUT = "PUT"

    @staticmethod
    def from_ib(value: str) -> 'OptionType':
        return OptionType(value)

    @staticmethod
    def to_ib(option_type: 'OptionType') -> str:
        return option_type.value


class StrikeType(enum.Enum):
    ATM = "ATM"
    ITM = "ITM"
    OTM = "OTM"

    @staticmethod
    def from_ib(value: str) -> 'StrikeType':
        return StrikeType(value)

    @staticmethod
    def to_ib(strike_type: 'StrikeType') -> str:
        return strike_type.value


class OrderType(enum.Enum):
    MARKET = "MKT"
    LIMIT = "LMT"
    STOP = "STP"
    STOP_LIMIT = "STP LMT"
    TRAILING_STOP = "TRAIL"
    TRAILING_STOP_LIMIT = "TRAIL LIMIT"

    @staticmethod
    def from_ib(value: str) -> 'OrderType':
        return OrderType(value)

    @staticmethod
    def to_ib(order_type: 'OrderType') -> str:
        return order_type.value


class OrderStatus(enum.Enum):
    Unknown = 'Unknown'
    PendingSubmit = 'PendingSubmit'
    PendingCancel = 'PendingCancel'
    PreSubmitted = 'PreSubmitted'
    Submitted = 'Submitted'
    ApiPending = 'ApiPending'
    ApiCancelled = 'ApiCancelled'
    Cancelled = 'Cancelled'
    Filled = 'Filled'
    Inactive = 'Inactive'

    DoneStates: {'Filled', 'Cancelled', 'ApiCancelled'}
    ActiveStates: {'PendingSubmit', 'ApiPending', 'PreSubmitted', 'Submitted'}

    def is_done(self) -> bool:
        return self in OrderStatus.DoneStates

    def is_active(self) -> bool:
        return self in OrderStatus.ActiveStates


class OrderDirection(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

    @staticmethod
    def from_ib(value: str) -> 'OrderDirection':
        if value == "BOT":
            return OrderDirection.BUY
        elif value == "SLD":
            return OrderDirection.SELL
        else:
            return OrderDirection(value)

    @staticmethod
    def to_ib(direction: 'OrderDirection') -> str:
        if direction == OrderDirection.BUY:
            return "BOT"
        elif direction == OrderDirection.SELL:
            return "SLD"
        else:
            return direction.value


@dataclass_json
@dataclass
class OrderData:
    id: Optional[int] = None
    order_id: Optional[int] = None
    perm_id: Optional[int] = None  # Permanent order id
    client_id: Optional[int] = None
    account_id: Optional[str] = None
    contract_id: Optional[int] = None
    order_type: Optional[OrderType] = None
    direction: Optional[OrderDirection] = None
    market_action: Optional[str] = None
    quantity: Optional[float] = None
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    trailing_percent: Optional[float] = None
    trail_stop_price: Optional[float] = None
    percent_offset: Optional[float] = None
    tif: Optional[str] = "DAY"
    status: Optional[OrderStatus] = OrderStatus.Unknown
    message: Optional[str] = None
    error_code: Optional[str] = None
    filled_quantity: Optional[float] = 0
    remaining_quantity: Optional[float] = 0
    avg_fill_price: Optional[float] = None
    is_active: Optional[bool] = True
    order_time: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    ref_id: Optional[str] = None
    ref_data: Optional['RefData'] = None
    contract: Optional['ContractData'] = None
    created_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    updated_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))

    def as_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "perm_id": self.perm_id,
            "client_id": self.client_id,
            "account_id": self.account_id,
            "contract_id": self.contract_id,
            "order_type": self.order_type.value,
            "direction": self.direction.value,
            "market_action": self.market_action,
            "quantity": self.quantity,
            "limit_price": self.limit_price,
            "stop_price": self.stop_price,
            "trailing_percent": self.trailing_percent,
            "trail_stop_price": self.trail_stop_price,
            "percent_offset": self.percent_offset,
            "tif": self.tif,
            "status": self.status.value,
            "message": self.message,
            "error_code": self.error_code,
            "filled_quantity": self.filled_quantity,
            "remaining_quantity": self.remaining_quantity,
            "avg_fill_price": self.avg_fill_price,
            "is_active": self.is_active,
            "order_time": str(self.order_time),
            "contract": self.contract.as_dict() if self.contract else None,
            "ref_id": self.ref_id,  # webhook trigger id
            "ref_data": self.ref_data.as_dict() if self.ref_data else None,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }


@dataclass_json
@dataclass
class RefData:
    id: Optional[int] = None
    ref_id: Optional[str] = None
    dt: Optional[datetime] = field(default=None,
                                   metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    vt_symbol: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    action: Optional[str] = None
    market_action: Optional[str] = None
    market_position: Optional[str] = None
    market_position_size: Optional[float] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))

    def as_dict(self):
        return {
            "id": self.id,
            "vt_symbol": self.vt_symbol,
            "dt": str(self.dt),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "action": self.action,
            "market_action": self.market_action,
            "market_position": self.market_position,
            "market_position_size": self.market_position_size,
            "created_at": str(self.created_at)
        }
