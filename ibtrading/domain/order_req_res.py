"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/03/2025
"""
from dataclasses import field
from datetime import datetime
from typing import Optional, List

from ibtrading.domain.account import AccountData
from ibtrading.domain.commons import BaseResponse
from ibtrading.domain.commons import Pagination, BaseRequest
from ibtrading.domain.order import OrderData, ContractData
from ibtrading.domain.portfolio import PortfolioData
from ibtrading.domain.trade import TradeData


class ListOrderRequest(BaseRequest):
    symbol: str = None
    from_dt: datetime = None
    to_dt: datetime = None
    pagination: Pagination = None


class ListOrderResponse(BaseResponse):
    orders: Optional[List[OrderData]] = field(default_factory=list)


class ListAccountResponse(BaseResponse):
    accounts: Optional[List[AccountData]] = field(default_factory=list)


class ListPositionResponse(BaseResponse):
    positions: Optional[List[PortfolioData]] = field(default_factory=list)


class ListPortfolioResponse(BaseResponse):
    portfolios: Optional[List[PortfolioData]] = field(default_factory=list)


class ListContractResponse(BaseResponse):
    contracts: Optional[List[ContractData]] = field(default_factory=list)


class CloseOrderRequest(BaseRequest):
    position_id: str = None
    account_id: str = None
    contract_id: str = None


class CloseOrderResponse(BaseResponse):
    trade: Optional[TradeData] = None


class GetMarketPriceRequest(BaseRequest):
    contract_id: int = 0


class GetMarketPriceResponse(BaseResponse):
    price: Optional[float] = None
    contract: Optional[ContractData] = None
    dt: Optional[datetime] = None
