"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 17/02/2025
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from ibtrading.repo.datasource import Base
from ibtrading.utils import ibutil
from ibtrading.utils.dtutil import current_time


class ContractRecord(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, unique=True, nullable=True)
    sec_type = Column(String(16), nullable=True)
    symbol = Column(String(16), nullable=True)
    last_trade_date_or_contract_month = Column(String(16), nullable=True)
    strike = Column(Float, nullable=True)
    right = Column(String(16), nullable=True)
    multiplier = Column(String(16), nullable=True)
    exchange = Column(String(16), nullable=True)
    currency = Column(String(6), nullable=True)
    local_symbol = Column(String(16), nullable=True)
    trading_class = Column(String(16), nullable=True)
    include_expired = Column(Boolean, default=False)
    sec_id_type = Column(String(16), nullable=True)
    sec_id = Column(String(16), nullable=True)
    description = Column(String(64), nullable=True)
    issuer_id = Column(String(16), nullable=True)
    combo_legs_desc = Column(String(64), nullable=True)
    combo_legs = Column(String(64), nullable=True)
    delta_neutral_contract = Column(String(64), nullable=True)
    vt_symbol = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_time)
    updated_at = Column(DateTime(timezone=True), default=current_time, onupdate=current_time)

    def __repr__(self):
        return f"Contract(id={self.id}, contract_id={self.contract_id}, sec_type={self.sec_type}, symbol={self.symbol}, last_trade_date_or_contract_month={self.last_trade_date_or_contract_month}, strike={self.strike}, right={self.right}, multiplier={self.multiplier}, exchange={self.exchange}, currency={self.currency}, local_symbol={self.local_symbol}, trading_class={self.trading_class}, include_expired={self.include_expired}, sec_id_type={self.sec_id_type}, sec_id={self.sec_id}, description={self.description}, issuer_id={self.issuer_id}, combo_legs_desc={self.combo_legs_desc}, combo_legs={self.combo_legs}, delta_neutral_contract={self.delta_neutral_contract}, created_at={self.created_at}, updated_at={self.updated_at})"

    def get_vt_symbol(self):
        return ibutil.generate_vt_symbol_v1(symbol=self.symbol, sec_type=self.sec_type,
                                            last_trade_date_or_contract_month=self.last_trade_date_or_contract_month,
                                            strike=self.strike, multiplier=self.multiplier, right=self.right,
                                            currency=self.currency, exchange=self.exchange)
