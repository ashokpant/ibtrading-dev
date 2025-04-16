"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/03/2025
"""
from dataclasses import field
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from ibtrading.domain import TradeData, Pagination, BaseRequest
from ibtrading.domain.commons import BaseResponse


class TradeDataFilter(BaseModel):
    query: Optional[str] = Field(default=None, description="Search query")
    symbols: Optional[List[str]] = Field(default=None, description="List of symbols to filter")
    security_types: Optional[List[str]] = Field(default=None, description="List of security types")
    accounts: Optional[List[str]] = Field(default=None, description="List of account IDs")
    from_dt: Optional[datetime] = Field(default=None, description="Start datetime")
    to_dt: Optional[datetime] = Field(default=None, description="End datetime")
    pagination: Optional[Pagination] = Field(default=None, description="Pagination info")


class ListTradeRequest(BaseRequest):
    filter: TradeDataFilter = Field(default_factory=TradeDataFilter)


class ListTradeResponse(BaseResponse):
    trades: Optional[List[TradeData]] = field(default_factory=list)
    grouped_trades: Optional[List[List[TradeData]]] = field(default_factory=list)  # List of list of trade group
    pagination: Pagination = None
