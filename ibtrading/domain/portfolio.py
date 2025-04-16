"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 19/02/2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config

from ibtrading.domain import ContractData
from ibtrading.utils.dtutil import datetime_encoder, datetime_from_str


@dataclass_json
@dataclass
class PortfolioData:
    id: Optional[int] = None
    account_id: Optional[str] = None
    contract_id: Optional[int] = None
    position: Optional[float] = None
    market_price: Optional[float] = None
    market_value: Optional[float] = None
    average_cost: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    realized_pnl: Optional[float] = None

    created_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    updated_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))

    contract: Optional['ContractData'] = None

    def as_dict(self):
        d = {
            "id": self.id,
            "account_id": self.account_id,
            "contract_id": self.contract_id,
            "position": self.position,
            "market_price": self.market_price,
            "market_value": self.market_value,
            "average_cost": self.average_cost,
            "unrealized_pnl": self.unrealized_pnl,
            "realized_pnl": self.realized_pnl,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "contract": self.contract.as_dict() if self.contract else None
        }
        return d
