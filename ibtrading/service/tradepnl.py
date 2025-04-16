"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/04/2025
"""
from ibtrading.utils import uuidutil, loggerutil

logger = loggerutil.get_logger(__name__)


def calculate_pnl(trades, last_set_only=False):
    """
    Collect trade sets and calculate pnls of each trade set of the same contract.
    """
    if len(trades) < 2:
        return []
    trades = sorted(trades, key=lambda x: (x.trade_time, x.created_at))
    _trades = []

    trade_set = [trades[0]]
    for i in range(1, len(trades)):
        t = trades[i]
        pt = trades[i - 1]
        # print(f"ID: {t.id}, Trade Time: {t.trade_time}, Market Action: {t.market_action}, "
        #       f"Price: {t.price}, Quantity: {t.quantity}, Commission: {t.commission}")
        current_action = t.market_action
        if current_action is None:
            trade_set = []
            continue
        previous_action = pt.market_action
        if previous_action is None:
            trade_set = [t]
            continue
        if current_action.startswith('ENTRY') and previous_action.startswith('EXIT'):
            if not last_set_only:
                _trade_set = _calculate_pnl(trade_set)
                _trades.append(_trade_set)
            trade_set = [t]
        else:
            actions = set([_t.market_action for _t in trade_set])
            if ["SHORT" in a for a in actions].count(True) > 0 and \
                    ["LONG" in a for a in actions].count(True) > 0:
                trade_set = []
            trade_set.append(t)

    if len(trade_set) > 0:
        _trade_set = _calculate_pnl(trade_set)
        _trades.append(_trade_set)

    if len(_trades) == 0:
        logger.debug("No trades to process.")
        return []
    return _trades


def _calculate_pnl(trade_set):
    """
    Calculate PnL for a set of trades.
    """
    trade_id = uuidutil.generate_sortable_int_uuid()
    total_pnl = 0
    total_commission = 0
    entry_price = 0
    entry_quantity = 0
    exit_price = 0
    exit_quantity = 0
    for trade in trade_set:
        if trade.market_action.startswith('ENTRY'):
            entry_price += trade.avg_price * trade.quantity
            entry_quantity += trade.quantity
        elif trade.market_action.startswith('EXIT'):
            exit_price += trade.avg_price * trade.quantity
            exit_quantity += trade.quantity
        total_commission += trade.commission

    logger.debug(f"Total entry quantity:{entry_quantity}, exit quantity:{exit_quantity}")
    if entry_quantity == 0 or exit_quantity == 0:
        logger.debug("Entry or exit quantity is zero. Cannot calculate PnL.")
        return []

    if entry_quantity == exit_quantity:
        entry_action = trade_set[0].market_action
        if entry_action == 'ENTRY_LONG':
            total_pnl = exit_price - entry_price
        elif entry_action == 'ENTRY_SHORT':
            total_pnl = entry_price - exit_price
    else:
        logger.debug("Entry and exit quantities do not match. Cannot calculate PnL.")
        return []

    _trade_set = []
    for trade in trade_set:
        trade.total_pnl = round(total_pnl, 2)
        trade.total_commission = round(total_commission, 2)
        trade.trade_id = trade_id
        _trade_set.append(trade)
    return _trade_set


def calculate_pnl_for_ref_trade(trade_id: int, market_action: str, trades):
    """
    Collect trade sets and calculate pnls of each trade set of the same contract.
    """
    if len(trades) < 2:
        return []

    # print("Raw Trades")

    trades = sorted(trades, key=lambda x: (x.trade_time, x.created_at))

    last_trade = trades[-1]
    exit_action = last_trade.market_action

    # print(trade_id, exit_action, "\n--")
    #
    # print("Trades")
    # for t in trades:
    #     print(t.id, t.market_action, t.trade_time, t.price, t.quantity, t.commission, t.pnl)
    # print("Last trade")
    # print(last_trade.id, last_trade.market_action, last_trade.trade_time, last_trade.price, last_trade.quantity,
    #       last_trade.commission, last_trade.pnl)
    # print("Given trade")
    # print("Exit action", exit_action)

    if last_trade.id != trade_id:
        logger.debug("Mismatched trade ID. Cannot calculate PnL.")
        return []
    if exit_action is None:
        logger.debug("Unknown trade action. Cannot calculate PnL.")
        return []
    if exit_action.startswith('ENTRY'):
        logger.debug("Trade is an entry trade. Cannot calculate PnL.")
        return []

    _trade_sets = calculate_pnl(trades, last_set_only=True)
    _trades = _trade_sets[0] if len(_trade_sets) > 0 else []
    # print("Trades with pnl")
    # for t in _trades:
    #     print(t.id, t.trade_id, t.market_action, t.trade_time, t.price, t.quantity, t.commission, t.pnl, t.total_pnl,
    #           t.total_commission)
    return _trades
