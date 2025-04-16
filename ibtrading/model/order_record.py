"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/02/2025
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum

from ibtrading.domain import OrderType, OrderStatus
from ibtrading.domain.order import OrderDirection
from ibtrading.repo.datasource import Base
from ibtrading.utils.dtutil import current_time


class OrderRecord(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=True)
    perm_id = Column(Integer, nullable=True)
    client_id = Column(Integer, nullable=True)
    account_id = Column(String(32), nullable=True)
    contract_id = Column(Integer, nullable=True)
    direction = Column(Enum(OrderDirection), nullable=True)
    market_action = Column(String(32), nullable=True)
    order_type = Column(Enum(OrderType), nullable=True)
    quantity = Column(Integer, nullable=True)
    filled_quantity = Column(Float, default=0)
    remaining_quantity = Column(Float, default=0)
    avg_fill_price = Column(Float, nullable=True)
    stop_price = Column(Float, nullable=True)
    limit_price = Column(Float, nullable=True)
    trailing_percent = Column(Float, nullable=True)  # For trailing stop orders
    percent_offset = Column(Float, nullable=True)
    tif = Column(String(10), nullable=True, default="DAY")  # Time in Force (e.g., DAY, GTC)
    status = Column(Enum(OrderStatus), nullable=True, default=OrderStatus.Unknown)
    is_active = Column(Boolean, default=True)
    order_time = Column(DateTime(timezone=True), nullable=True)
    ref_id = Column(String(36), nullable=True)
    message = Column(String(1024), nullable=True)
    error_code = Column(String(16), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_time)
    updated_at = Column(DateTime(timezone=True), default=current_time, onupdate=current_time)

    contract = None

    def __repr__(self):
        return f"Order(id={self.id}, order_id={self.order_id}, perm_id={self.perm_id}, client_id={self.client_id}, account_id={self.account_id}, contract_id={self.contract_id}, direction={self.direction}, market_action={self.market_action},  order_type={self.order_type}, quantity={self.quantity}, limit_price={self.limit_price}, stop_price={self.stop_price}, trailing_percent={self.trailing_percent}, percent_offset={self.percent_offset}, tif={self.tif}, status={self.status}, filled={self.filled_quantity}, avg_fill_price={self.avg_fill_price}, is_active={self.is_active}, ref_id={self.ref_id}, created_at={self.created_at}, updated_at={self.updated_at})"
