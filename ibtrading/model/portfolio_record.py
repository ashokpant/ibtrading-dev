"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 19/02/2025
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from ibtrading.repo.datasource import Base
from ibtrading.utils.dtutil import current_time


class PortfolioRecord(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(32), nullable=True)
    contract_id = Column(Integer, nullable=True)
    position = Column(Float, nullable=True)
    market_price = Column(Float, nullable=True)
    market_value = Column(Float, nullable=True)
    average_cost = Column(Float, nullable=True)
    unrealized_pnl = Column(Float, nullable=True)
    realized_pnl = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), default=current_time)
    updated_at = Column(DateTime(timezone=True), default=current_time, onupdate=current_time)
    contract = None

    def __repr__(self):
        return f"Portfolio(id={self.id}, account_id={self.account_id}, contract_id={self.contract_id}, position={self.position}, market_price={self.market_price}, market_value={self.market_value}, average_cost={self.average_cost}, unrealized_pnl={self.unrealized_pnl}, realized_pnl={self.realized_pnl}, created_at={self.created_at}, updated_at={self.updated_at}, contract={self.contract})"
