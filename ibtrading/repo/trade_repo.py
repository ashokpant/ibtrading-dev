"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 23/10/2024
"""
import logging
from typing import List

from sqlalchemy import asc
from sqlalchemy.sql.operators import like_op

from ibtrading import domain, mapper
from ibtrading.domain import TradeDataFilter
from ibtrading.model import TradeRecord, OrderRecord, ContractRecord, WebhookRecord
from ibtrading.repo.datasource import DataSource, Repo

logger = logging.getLogger(__name__)


class TradeRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def list_trades_v1(self, filter: TradeDataFilter) -> List[domain.TradeData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(TradeRecord, OrderRecord, ContractRecord, WebhookRecord)
                    .outerjoin(OrderRecord, OrderRecord.perm_id == TradeRecord.order_id)
                    .outerjoin(ContractRecord, ContractRecord.contract_id == OrderRecord.contract_id)
                    .outerjoin(WebhookRecord, WebhookRecord.ref_id == OrderRecord.ref_id))
                orders = query.order_by(asc(TradeRecord.created_at)).all()
                return [mapper.map2trade_data(trade=t, order=o, contract=c, webhook_log=wl) for t, o, c, wl in orders]
            except Exception as e:
                logger.exception("Error fetching trades from database: %s", e)
                return []

    def list_trades_v2(self, filter: TradeDataFilter) -> List[domain.TradeData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(TradeRecord, OrderRecord, ContractRecord, WebhookRecord)
                    .outerjoin(OrderRecord, OrderRecord.perm_id == TradeRecord.order_id)
                    .outerjoin(ContractRecord, ContractRecord.contract_id == OrderRecord.contract_id)
                    .outerjoin(WebhookRecord, WebhookRecord.ref_id == OrderRecord.ref_id))
                if filter.query:
                    query = query.filter(like_op(ContractRecord.vt_symbol, filter.query))
                if filter.from_dt is not None:
                    query = query.filter(TradeRecord.created_at >= filter.from_dt)
                if filter.to_dt is not None:
                    query = query.filter(TradeRecord.created_at <= filter.to_dt)
                if filter.symbols:
                    query = query.filter(ContractRecord.symbol.in_(filter.symbols))
                if filter.security_types:
                    query = query.filter(ContractRecord.sec_type.in_(filter.security_types))

                orders = query.order_by(asc(TradeRecord.created_at)).all()
                return [mapper.map2trade_data(trade=t, order=o, contract=c, webhook_log=wl) for t, o, c, wl in orders]
            except Exception as e:
                logger.exception("Error fetching trades from database: %s", e)
                return []
