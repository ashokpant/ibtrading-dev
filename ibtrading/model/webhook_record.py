"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/02/2025
"""

from sqlalchemy import Column, Integer, JSON, DateTime, String, Float, Text

from ibtrading.domain import WebhookPayload
from ibtrading.repo.datasource import Base
from ibtrading.utils.dtutil import current_time


class WebhookRecord(Base):
    __tablename__ = "webhook_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_id = Column(String, nullable=True)
    contracts = Column(Float, default=0)
    symbol = Column(String, nullable=True)
    position_size = Column(Float, default=0)
    action = Column(String, nullable=True)
    market_position = Column(String, nullable=True)
    market_action = Column(String, nullable=True)
    market_position_size = Column(Float, default=0)
    dt = Column(DateTime(timezone=True), nullable=True)
    close = Column(Float, default=0)
    open = Column(Float, default=0)
    high = Column(Float, default=0)
    low = Column(Float, default=0)
    volume = Column(Float, default=0)
    timeframe = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    dt_now = Column(DateTime(timezone=True), nullable=True)
    currency = Column(String, nullable=True)
    strategy = Column(String, nullable=True)
    metainfo = Column(Text, nullable=True)
    order_type = Column(String, nullable=True)
    sec_type = Column(String, nullable=True)
    last_trade_date_or_contract_month = Column(String, nullable=True)
    message = Column(String, nullable=True)
    vt_symbol = Column(String, nullable=True)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=current_time)
    updated_at = Column(DateTime(timezone=True), default=current_time, onupdate=current_time)

    @classmethod
    def to_payload_str(cls, data: WebhookPayload):
        payload = data.model_dump(mode="json")
        return payload
