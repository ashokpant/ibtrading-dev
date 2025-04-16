"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/03/2025
"""
import json
from datetime import timedelta

from ibtrading import model
from ibtrading.domain import WebhookPayload
from ibtrading.utils import uuidutil, ibutil, dtutil


def populate_webhook_payload(req: WebhookPayload) -> WebhookPayload:
    req.ref_id = uuidutil.generate_uuid()
    if req.symbol == "BTC1!":
        req.symbol = "BRR1!"  # TODO changed BTC to BRR for IBKR processing
    req.time = dtutil.convert_to_default_tz(req.time)
    req.timenow = dtutil.convert_to_default_tz(req.timenow)
    req.action = req.action.upper()
    req.order_type = req.order_type.upper()
    req.currency = req.currency.upper()
    req.sec_type = req.sec_type.upper()
    if req.sec_type == "FUT":
        req.sec_type = "CONTFUT"
    req.exchange = req.exchange.upper()
    req.market_position = req.market_position.upper()
    req.market_action = get_market_action(req.action, req.market_position)

    if req.market_position != "FLAT":  # To manage order of execution
        req.time = req.time + timedelta(milliseconds=999)
    req.vt_symbol = ibutil.generate_vt_symbol_from_webhook(symbol=req.symbol, sec_type=req.sec_type,
                                                           last_trade_date_or_contract_month=req.last_trade_date_or_contract_month,
                                                           timeframe=req.timeframe,
                                                           exchange=req.exchange,
                                                           currency=req.currency)
    return req


def get_market_action(action, market_position) -> str:
    if action == 'BUY' and market_position == 'LONG':
        return 'ENTRY_LONG'
    elif action == 'SELL' and market_position == 'SHORT':
        return 'ENTRY_SHORT'
    elif action == 'SELL' and market_position == 'FLAT':
        return 'EXIT_LONG'
    elif action == 'BUY' and market_position == 'FLAT':
        return 'EXIT_SHORT'
    else:
        raise ValueError(f"Unhandled action: {action}-{market_position}")


def map2contract_record(payload: WebhookPayload):
    r = model.WebhookRecord(
        id=payload.id,
        ref_id=payload.ref_id,
        contracts=payload.contracts,
        symbol=payload.symbol,
        position_size=payload.position_size,
        action=payload.action,
        market_action=payload.market_action,
        market_position=payload.market_position,
        market_position_size=payload.market_position_size,
        dt=payload.time,
        close=payload.close,
        open=payload.open,
        high=payload.high,
        low=payload.low,
        volume=payload.volume,
        timeframe=payload.timeframe,
        exchange=payload.exchange,
        dt_now=payload.timenow,
        currency=payload.currency,
        strategy=payload.strategy,
        metainfo=json.dumps(payload.metadata) if payload.metadata else None,
        order_type=payload.order_type,
        sec_type=payload.sec_type,
        last_trade_date_or_contract_month=payload.last_trade_date_or_contract_month,
        message=payload.message,
        vt_symbol=payload.vt_symbol,
        payload=payload.model_dump(mode="json"),
        created_at=payload.created_at,
        updated_at=payload.updated_at,
    )
    return r


def map2webhook_payload(record: model.WebhookRecord):
    if record is None:
        return None
    d = WebhookPayload(
        id=record.id,
        ref_id=record.ref_id,
        contracts=record.contracts,
        symbol=record.symbol,
        position_size=record.position_size,
        action=record.action,
        market_action=record.market_action,
        market_position=record.market_position,
        market_position_size=record.market_position_size,
        time=record.dt,
        close=record.close,
        open=record.open,
        high=record.high,
        low=record.low,
        volume=record.volume,
        timeframe=record.timeframe,
        exchange=record.exchange,
        timenow=record.dt_now,
        currency=record.currency,
        strategy=record.strategy or "",
        metadata=json.loads(record.metainfo) if record.metainfo else None,
        order_type=record.order_type,
        sec_type=record.sec_type,
        last_trade_date_or_contract_month=record.last_trade_date_or_contract_month,
        message=record.message,
        vt_symbol=record.vt_symbol or "",
        created_at=record.created_at,
        updated_at=record.updated_at,
    )
    return d
