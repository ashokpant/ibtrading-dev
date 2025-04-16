"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 23/10/2024
"""
import logging
from datetime import datetime
from typing import List, Optional

from ib_async import Contract
from sqlalchemy import or_, and_, asc, desc, text

from ibtrading import mapper
from ibtrading.domain import WebhookPayload, OrderStatus, TradeData, PortfolioData, OrderData, ContractData, \
    AccountValueData
from ibtrading.model.account_value_record import AccountValueRecord
from ibtrading.model.contract_record import ContractRecord
from ibtrading.model.order_record import OrderRecord
from ibtrading.model.portfolio_record import PortfolioRecord
from ibtrading.model.trade_record import TradeRecord
from ibtrading.model.webhook_record import WebhookRecord
from ibtrading.repo.datasource import DataSource, Repo
from ibtrading.service import tradepnl
from ibtrading.utils import strutil

logger = logging.getLogger(__name__)


class OrderRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def save_webhook_payload(self, req: WebhookPayload) -> Optional[WebhookPayload]:
        with self.db.get_session() as sess:
            try:

                result = sess.query(WebhookRecord).filter_by(ref_id=req.ref_id).with_for_update().first()
                if not result:
                    r = mapper.map2contract_record(req)
                    sess.add(r)
                    sess.commit()
                    sess.refresh(r)
                    req.id = r.id
                    req.created_at = r.created_at
                else:
                    req.id = result.id
                    req.created_at = result.created_at
                return req
            except Exception as e:
                sess.rollback()
                logger.exception(f"Error saving webhook log: {e}")
                return None

    def _save_or_update_trade(self, sess, trade: TradeData) -> None:
        print("Save trade request: ", trade)
        t = mapper.map2trade_record(trade)
        print("Mapped trade request: ", t)
        if t.contract:
            self.__save_or_update_contract(sess, t.contract)
        if t.order:
            self.__save_or_update_order(t.order, sess)
        self.__save_trade_record(sess, t)

        _trade = sess.query(TradeRecord).filter_by(order_id=t.order_id).with_for_update().first()
        print("Before commit tradeee: ", _trade)
        if _trade is not None:
            self.calculate_and_update_trade_pnl(sess, _trade)

    def __save_or_update_order(self, order: OrderRecord, sess) -> None:
        result = sess.query(OrderRecord).filter(
            or_(
                and_(OrderRecord.perm_id > 0, OrderRecord.perm_id == order.perm_id),
                and_(OrderRecord.order_id > 0, OrderRecord.order_id == order.order_id)
            )).first()
        if not result:
            sess.add(order)
            logger.debug(f"Order saved: {order}")
        else:
            for attr, value in order.__dict__.items():
                if (not attr.startswith('_') and value is not None
                        and attr != "contract"):  # Exclude internal SQLAlchemy attributes
                    setattr(result, attr, value)
            logger.debug(f"Order updated: {order}")

    def _save_or_update_order(self, order: OrderData, sess) -> None:
        o = mapper.map2order_record(order)
        self.__save_or_update_order(o, sess)

    def __save_trade_record(self, sess, trade: TradeRecord) -> bool:
        if trade:
            if trade.order_id <= 0 or trade.status != OrderStatus.Filled:
                return True

            result = sess.query(TradeRecord).filter_by(order_id=trade.order_id).first()
            if not result:
                sess.add(trade)
                logger.debug(f"Trade saved: {trade}")
            else:
                for attr, value in trade.__dict__.items():
                    if attr in ["contract", "order", "total_pnl", "total_commission", "market_action", "trade_id"]:
                        continue
                    if not attr.startswith('_') and attr is not None:  # Exclude internal SQLAlchemy attributes
                        setattr(result, attr, value)
                logger.debug(f"Trade updated: {trade}")
        return True

    def calculate_and_update_trade_pnl_v1(self, trade: TradeData, sess) -> bool:
        return self._calculate_and_update_trade_pnl(sess, trade_id=trade.id, trade_time=trade.trade_time,
                                                    market_action=trade.market_action, contract_id=trade.contract_id)

    def calculate_and_update_trade_pnl(self, sess, trade: TradeRecord) -> bool:
        return self._calculate_and_update_trade_pnl(sess, trade_id=trade.id, trade_time=trade.trade_time,
                                                    market_action=trade.market_action, contract_id=trade.contract_id)

    def _calculate_and_update_trade_pnl(self, sess, trade_id: int, market_action, contract_id,
                                        trade_time: datetime) -> bool:
        results = (sess.query(TradeRecord, OrderRecord)
                   .outerjoin(OrderRecord, OrderRecord.perm_id == TradeRecord.order_id)
                   .filter(TradeRecord.contract_id == contract_id,
                           TradeRecord.trade_time <= trade_time).order_by(desc(TradeRecord.trade_time)).limit(
            5).with_for_update().all())
        trades = []
        for t, o in results:
            t.market_action = o.market_action
            trades.append(t)
        _trades = tradepnl.calculate_pnl_for_ref_trade(trade_id=trade_id, market_action=market_action, trades=trades)
        if len(_trades) == 0:
            return True
        for t in _trades:
            self._update_trade_pnl(sess, t)
        return True

    def update_trades_pnl(self, trades: list[TradeRecord]) -> bool:
        if not trades:
            return True
        with self.db.get_session() as sess:
            try:
                for trade in trades:
                    if not self._update_trade_pnl(sess, trade):
                        return False
                sess.commit()
                return True
            except Exception as e:
                logger.exception("Error updating trades in database: %s", e)
                raise e

    def _update_trade_pnl(self, sess, trade: TradeRecord) -> bool:
        if not trade:
            return True
        update_query = text(
            "UPDATE trade SET trade_id=:trade_id, total_pnl=:total_pnl, total_commission=:total_commission WHERE id=:id")
        result = sess.execute(update_query, {'total_pnl': trade.total_pnl, 'total_commission': trade.total_commission,
                                             'trade_id': trade.trade_id, 'id': trade.id})
        if result.rowcount > 0:
            logger.debug(f"Trade updated: {trade}")
            return True
        else:
            logger.warning(f"Trade with ID {trade.id} not found for update.")
            return False

    def __save_or_update_contract(self, sess, contract: ContractRecord) -> bool:
        if contract:
            result = sess.query(ContractRecord).filter_by(contract_id=contract.contract_id).first()
            if not result:
                sess.add(contract)
                logger.debug(f"Contract saved: {contract}")

        return True

    def save_trade(self, trade: TradeData, sess=None) -> bool:
        if sess is None:
            sess = self.db.get_session()
        try:
            with sess.begin():
                self._save_or_update_trade(sess, trade)
            return True
        except Exception as e:
            sess.rollback()
            logger.exception("Error saving trade to database: %s", e)
            return False

    def save_order(self, order: OrderData, sess=None) -> bool:
        if sess is None:
            sess = self.db.get_session()
        try:
            with sess.begin():
                self._save_or_update_order(order, sess)
            return True
        except Exception as e:
            sess.rollback()
            logger.exception("Error saving order to database: %s", e)
            return False

    def save_trades(self, trades: List[TradeData]) -> bool:
        sess = self.db.get_session()
        try:
            for trade in trades:
                with sess.begin():
                    self._save_or_update_trade(sess, trade)
            return True
        except Exception as e:
            sess.rollback()
            logger.exception("Error saving trades to database: %s", e)
            return False

    def save_contact(self, contract: ContractData) -> bool:
        sess = self.db.get_session()
        try:
            with sess.begin():
                result = sess.query(ContractRecord).filter_by(contract_id=contract.contract_id).first()
                if not result:
                    c = mapper.map2contract_record(contract)
                    sess.add(c)
            return True
        except Exception as e:
            sess.rollback()
            logger.exception("Error saving contract to database: %s", e)
            return False

    def save_portfolio(self, portfolio: PortfolioData):
        p = mapper.map2portfolio_record(portfolio)
        sess = self.db.get_session()
        try:
            with sess.begin():
                self.__save_or_update_contract(sess, p.contract)

                result = sess.query(PortfolioRecord).filter_by(account_id=p.account_id,
                                                               contract_id=p.contract_id).first()
                if not result:
                    sess.add(p)
                else:
                    for attr, value in p.__dict__.items():
                        if not attr.startswith('_') and value is not None and attr not in ["contract_id", "account_id"]:
                            setattr(result, attr, value)
            return True
        except Exception as e:
            sess.rollback()
            logger.exception("Error saving portfolio to database: %s", e)
            return False

    def save_account_value(self, account_value: AccountValueData):
        p = mapper.map2account_value_record(account_value)
        sess = self.db.get_session()
        try:
            with sess.begin():
                result = sess.query(AccountValueRecord).filter_by(account_id=p.account_id,
                                                                  tag=p.tag).first()
                if not result:
                    sess.add(p)
                else:
                    for attr, value in p.__dict__.items():
                        if not attr.startswith('_'):  # Exclude internal SQLAlchemy attributes
                            setattr(result, attr, value)
            return True
        except Exception as e:
            sess.rollback()
            logger.exception("Error saving account value to database: %s", e)
            return False

    def list_orders(self) -> List[OrderData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(OrderRecord, ContractRecord, WebhookRecord)
                    .outerjoin(ContractRecord, ContractRecord.contract_id == OrderRecord.contract_id)
                    .outerjoin(WebhookRecord, WebhookRecord.ref_id == OrderRecord.ref_id))
                orders = query.order_by(desc(OrderRecord.created_at)).all()

                return [mapper.map2order_data(order=o, contract=c, webhook_log=wl) for o, c, wl in orders]
            except Exception as e:
                logger.exception("Error fetching open positions from database: %s", e)
                return []

    def list_trades(self) -> List[TradeData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(TradeRecord, OrderRecord, ContractRecord, WebhookRecord)
                    .outerjoin(OrderRecord, OrderRecord.perm_id == TradeRecord.order_id)
                    .outerjoin(ContractRecord, ContractRecord.contract_id == OrderRecord.contract_id)
                    .outerjoin(WebhookRecord, WebhookRecord.ref_id == OrderRecord.ref_id))
                orders = query.order_by(desc(TradeRecord.created_at)).all()
                return [mapper.map2trade_data(trade=t, order=o, contract=c, webhook_log=wl) for t, o, c, wl in orders]
            except Exception as e:
                logger.exception("Error fetching trades from database: %s", e)
                return []

    def get_trade_by_id(self, trade_id: int) -> Optional[TradeData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(TradeRecord, OrderRecord, ContractRecord, WebhookRecord)
                    .outerjoin(OrderRecord, OrderRecord.perm_id == TradeRecord.order_id)
                    .outerjoin(ContractRecord, ContractRecord.contract_id == OrderRecord.contract_id)
                    .outerjoin(WebhookRecord, WebhookRecord.ref_id == OrderRecord.ref_id))
                query = query.filter(TradeRecord.id == trade_id)
                results = query.order_by(desc(TradeRecord.created_at)).first()
                if not results or len(results) < 1:
                    return None
                t, o, c, wl = results
                return mapper.map2trade_data(trade=t, order=o, contract=c, webhook_log=wl)
            except Exception as e:
                logger.exception("Error fetching trade from database: %s", e)
                return None

    def list_portfolio(self) -> List[PortfolioData]:
        sess = self.db.get_session()
        try:
            portfolios = (sess.query(PortfolioRecord, ContractRecord)
                          .join(ContractRecord,
                                PortfolioRecord.contract_id == ContractRecord.contract_id)
                          .filter(PortfolioRecord.position != 0)
                          .order_by(desc(PortfolioRecord.created_at)).all())
            return [mapper.map2portfolio_data(p, contract=c) for p, c in portfolios]
        except Exception as e:
            logger.exception("Error fetching portfolio from database: %s", e)
            return []

    def list_position(self) -> List[PortfolioData]:
        sess = self.db.get_session()
        try:
            positions = (sess.query(PortfolioRecord, ContractRecord)
                         .join(ContractRecord,
                               PortfolioRecord.contract_id == ContractRecord.contract_id)
                         .order_by(desc(PortfolioRecord.created_at)).all())
            return [mapper.map2portfolio_data(p, contract=c) for p, c in positions]
        except Exception as e:
            logger.exception("Error fetching portfolio from database: %s", e)
            return []

    def list_contracts(self) -> List[ContractData]:
        with self.db.get_session() as sess:
            try:
                contracts = sess.query(ContractRecord).order_by(desc(ContractRecord.created_at)).all()
                return [mapper.map2contract_data(c) for c in contracts]
            except Exception as e:
                logger.exception("Error fetching contracts from database: %s", e)
                return []

    def list_account_summary(self) -> List[AccountValueData]:
        sess = self.db.get_session()
        try:
            values = sess.query(AccountValueRecord).order_by(asc(AccountValueRecord.created_at)).all()
            return [mapper.map2account_value_data(v) for v in values]
        except Exception as e:
            logger.exception("Error fetching account values from database: %s", e)
            return []

    def list_webhook_logs(self) -> List[WebhookPayload]:
        sess = self.db.get_session()
        try:
            logs = sess.query(WebhookRecord).order_by(desc(WebhookRecord.dt)).all()
            data = [mapper.map2webhook_payload(log) for log in logs]
            return data
        except Exception as e:
            logger.exception("Error fetching webhook logs from database: %s", e)
            return []

    def get_open_positions(self, symbol, sec_type, exchange, currency, right=None, contract_id: int = None) -> List[
        PortfolioData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(PortfolioRecord, ContractRecord)
                    .join(ContractRecord, PortfolioRecord.contract_id == ContractRecord.contract_id))
                if contract_id is not None:
                    query = query.filter(PortfolioRecord.contract_id == contract_id)
                else:
                    query.filter(
                        ContractRecord.symbol == symbol,
                        ContractRecord.sec_type == sec_type,
                        ContractRecord.exchange == exchange,
                        ContractRecord.currency == currency)
                if right is not None:
                    query = query.filter(ContractRecord.right == right)

                query = query.filter(PortfolioRecord.position != 0).order_by(PortfolioRecord.created_at.desc())

                positions = query.all()

                return [mapper.map2portfolio_data(portfolio=p, contract=c) for p, c in positions]
            except Exception as e:
                logger.exception("Error fetching open positions from database: %s", e)
                return []

    def get_open_position(self, position_id: int) -> Optional[PortfolioData]:
        with self.db.get_session() as sess:
            try:
                query = (
                    sess.query(PortfolioRecord, ContractRecord)
                    .join(ContractRecord, PortfolioRecord.contract_id == ContractRecord.contract_id)
                    .filter(
                        PortfolioRecord.id == position_id, PortfolioRecord.position != 0)
                    .order_by(PortfolioRecord.created_at.desc()))

                positions = query.all()
                if not positions or len(positions) < 1:
                    return None
                return mapper.map2portfolio_data(portfolio=positions[0][0], contract=positions[0][1])
            except Exception as e:
                logger.exception("Error fetching open positions from database: %s", e)
                return None

    def get_contract(self, contract: Contract) -> Optional[ContractData]:
        with self.db.get_session() as sess:
            try:
                query = sess.query(ContractRecord)
                if contract.conId > 0:
                    query = query.filter_by(contract_id=contract.conId)
                else:
                    query = query.filter_by(symbol=contract.symbol,
                                            sec_type=contract.secType,
                                            exchange=contract.exchange,
                                            currency=contract.currency,
                                            last_trade_date_or_contract_month=contract.lastTradeDateOrContractMonth)
                    if strutil.is_not_empty(contract.right):
                        query = query.filter_by(right=contract.right)
                result = query.first()
                if result:
                    return mapper.map2contract_data(result)
            except Exception as e:
                logger.exception("Error fetching contract from database: %s", e)
                return None

    def get_contract_by_id(self, contract_id: int) -> Optional[ContractData]:
        with self.db.get_session() as sess:
            try:
                query = sess.query(ContractRecord)
                query = query.filter_by(contract_id=contract_id)
                result = query.first()
                if result:
                    return mapper.map2contract_data(result)
            except Exception as e:
                logger.exception("Error fetching contract from database: %s", e)
                return None

    def get_last_webhook(self, req: WebhookPayload):
        with (self.db.get_session() as sess):
            try:
                log = sess.query(WebhookRecord
                                 ).filter(WebhookRecord.created_at < req.created_at,
                                          WebhookRecord.vt_symbol == req.vt_symbol).order_by(
                    desc(WebhookRecord.created_at)).limit(1).first()
                return mapper.map2webhook_payload(log)
            except Exception as e:
                logger.exception("Error fetching webhook log from database: %s", e)
            return None

    def get_webhook_by_id(self, webhook_id: int):
        with (self.db.get_session() as sess):
            try:
                log = sess.query(WebhookRecord).filter(WebhookRecord.id == webhook_id).first()
                return mapper.map2webhook_payload(log)
            except Exception as e:
                logger.exception("Error fetching contract from database: %s", e)
            return None
