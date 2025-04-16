"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/02/2025
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum

from ibtrading.domain import OrderDirection, OrderStatus
from ibtrading.repo.datasource import Base
from ibtrading.utils.dtutil import current_time


class TradeRecord(Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_id = Column(Integer, nullable=True)
    order_id = Column(Integer, nullable=True)  # Order permId
    client_id = Column(Integer, nullable=True)
    account_id = Column(String(32), nullable=True)
    contract_id = Column(Integer, nullable=True)
    direction = Column(Enum(OrderDirection), nullable=True)
    market_action = Column(String(32), nullable=True)
    quantity = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    avg_price = Column(Float, nullable=True)
    trade_time = Column(DateTime, nullable=True)
    commission = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    released_pnl = Column(Float, default=0.0)
    unrealized_pnl = Column(Float, default=0.0)
    total_pnl = Column(Float, nullable=True)
    total_commission = Column(Float, nullable=True)
    status = Column(Enum(OrderStatus), nullable=True)
    created_at = Column(DateTime, default=current_time)
    updated_at = Column(DateTime, default=current_time, onupdate=current_time)

    contract = None
    order = None

    def __repr__(self):
        return f"Trade(id={self.id}, trade_id={self.trade_id}, order_id={self.order_id}, client_id={self.client_id}, account_id={self.account_id}, contract_id={self.contract_id}, direction={self.direction}, market_action={self.market_action}, quantity={self.quantity}, price={self.price}, avg_price={self.avg_price}, trade_time={self.trade_time}, commission={self.commission}, pnl={self.pnl}, released_pnl={self.released_pnl}, unrealized_pnl={self.unrealized_pnl}, total_pnl={self.total_pnl}, total_commission={self.total_commission}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})"
