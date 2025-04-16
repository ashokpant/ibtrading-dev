"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/11/2024
"""
from dataclasses import field
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel

from ibtrading.domain import OrderData, TradeData, BaseResponse


class WebhookPayload(BaseModel):
    id: int = None
    ref_id: str = None
    action: str = None
    contracts: float = 0
    symbol: str = None
    position_size: float = 0
    market_position: str = 0
    market_action: Optional[str] = None
    market_position_size: float = 0
    time: Optional[datetime] = None
    close: float = 0
    open: float = 0
    high: float = 0
    low: float = 0
    volume: float = 0
    timeframe: str = None
    exchange: str = None
    timenow: Optional[datetime] = None
    currency: str = None
    strategy: str = None
    metadata: Optional[dict] = None
    order_type: str = "MARKET"  # MARKET, LIMIT, STOP, STOP_LIMIT
    sec_type: str = None  # FUT, STK, OPT, FOP, CASH, BAG, IND, FUND, CONTFUT
    last_trade_date_or_contract_month: str = None  # YYYYMMDD
    message: str = None
    vt_symbol: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    skip_order_close: bool = False  # Skip closing order if already handled by previous action

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class WebhookResponse(BaseResponse):
    trades: Optional[List[TradeData]] = field(default_factory=list)
    orders: Optional[List[OrderData]] = field(default_factory=list)


class ListWebhookPayloadResponse(BaseResponse):
    webhooks: Optional[List[WebhookPayload]] = field(default_factory=list)
