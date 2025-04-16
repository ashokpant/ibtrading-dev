"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 27/02/2025
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config

from ibtrading.utils.dtutil import datetime_encoder, datetime_from_str


@dataclass_json
@dataclass
class AccountValueData:
    id: Optional[int] = None
    account_id: Optional[str] = None
    tag: Optional[str] = None
    value: Optional[str] = None
    currency: Optional[str] = None
    model_code: Optional[str] = None
    created_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))
    updated_at: Optional[datetime] = field(default=None,
                                           metadata=config(encoder=datetime_encoder, decoder=datetime_from_str))

    def as_dict(self):
        d = {
            "id": self.id,
            "tag": self.tag,
            "value": self.value,
            "currency": self.currency,
            "model_code": self.model_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return d


@dataclass_json
@dataclass
class AccountData:
    account_id: Optional[str] = None
    values: Optional[list[AccountValueData]] = None

    def as_dict(self):
        d = {
            "account_id": self.account_id,
            "values": [v.as_dict() for v in self.values] if self.values else None
        }
        return d

