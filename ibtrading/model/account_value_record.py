"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 27/02/2025
"""

from sqlalchemy import Column, Integer, String, DateTime, func

from ibtrading.repo.datasource import Base
from ibtrading.utils.dtutil import current_time


class AccountValueRecord(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(32), nullable=True)
    tag = Column(String(64), nullable=True)
    value = Column(String(32), nullable=True)
    currency = Column(String(6), nullable=True)
    model_code = Column(String(32), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_time)
    updated_at = Column(DateTime(timezone=True), default=current_time, onupdate=current_time)

    contract = None

    def __repr__(self):
        return f"AccountValueRecord(id={self.id}, account_id={self.account_id}, tag={self.tag}, value={self.value}, currency={self.currency}, model_code={self.model_code}, created_at={self.created_at}, updated_at={self.updated_at})"
