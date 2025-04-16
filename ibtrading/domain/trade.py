"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/01/2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config

from ibtrading.domain import ContractData
from ibtrading.domain.order import OrderData, OrderDirection, OrderStatus
from ibtrading.utils.dtutil import datetime_encoder, datetime_from_str


@dataclass_json
@dataclass
class TradeData:
    id: Optional[int] = None  # Primary key
    trade_id: Optional[int] = None
    order_id: Optional[int] = None  # Order perm id
    client_id: Optional[int] = None
    account_id: Optional[str] = None
    contract_id: Optional[int] = None
    direction: Optional[OrderDirection] = None
    market_action: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    avg_price: Optional[float] = None
    trade_time: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    status: Optional[OrderStatus] = OrderStatus.Unknown
    commission: Optional[float] = None
    pnl: Optional[float] = None
    released_pnl: Optional[float] = 0.0
    unrealized_pnl: Optional[float] = 0.0

    total_pnl: float = 0.0
    total_pnl_percent: float = 0.0
    cumulative_pnl: float = 0.0
    cumulative_pnl_percent: float = 0.0

    total_commission:float = 0.0
    cumulative_commission: float = 0.0

    created_at: Optional[datetime] = field(default=None, metadata=config(encoder=datetime_encoder,
                                                                         decoder=datetime_from_str))
    updated_at: Optional[datetime] = field(default=None, metadata=config(encoder=datetime_encoder,
                                                                         decoder=datetime_from_str))

    order: Optional['OrderData'] = field(default=None)
    contract: Optional['ContractData'] = field(default=None)

    def as_dict(self):
        d = {
            "id": self.id,
            "trade_id": self.trade_id,
            "order_id": self.order_id,
            "client_id": self.client_id,
            "account_id": self.account_id,
            "contract_id": self.contract_id,
            "direction": self.direction.name if self.direction else None,
            "market_action": self.market_action,
            "quantity": self.quantity,
            "price": self.price,
            "avg_price": self.avg_price,
            "trade_time": str(self.trade_time),
            "commission": self.commission,
            "pnl": self.pnl,
            "released_pnl": self.released_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "total_pnl": self.total_pnl,
            "total_commission": self.total_commission,
            "status": self.status.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        if self.contract:
            d["contract"] = self.contract.as_dict()

        if self.order:
            d["order"] = self.order.as_dict()
        return d
