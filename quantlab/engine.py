from __future__ import annotations

import pandas as pd

from quantlab.models import BacktestResult
from quantlab.strategy import Strategy


def run_backtest(
    strategy: Strategy,
    prices: pd.DataFrame,
    initial_capital: float = 1.0,
    cost_per_trade: float = 0.001,
) -> BacktestResult:
    """
    Simulate a strategy over a price series.

    Args:
        strategy: The strategy to run.
        prices: OHLCV DataFrame indexed by date, ascending.
        initial_capital: Starting portfolio value (default 1.0 for
            easy percentage reading).
        cost_per_trade: Transaction cost as a fraction of traded amount,
            charged when the position changes (0.001 = 10 basis points).

    Returns:
        A BacktestResult with the equity curve, daily returns, and positions.
    """
    positions = strategy.generate_signals(prices)
    daily_returns = prices["close"].pct_change().fillna(0.0)

    # The CRITICAL LINE: today's decision earns tomorrow's return.
    # Without this shift, the strategy would trade on same-day information
    # it could not have known in advance (lookahead bias).
    effective_positions = positions.shift(1).fillna(0.0)
    gross_returns = effective_positions * daily_returns

    # Charge costs when the position changes (a trade occurs).
    position_changes = effective_positions.diff().abs().fillna(0.0)
    costs = position_changes * cost_per_trade

    net_returns = gross_returns - costs

    equity_curve = initial_capital * (1.0 + net_returns).cumprod()

    return BacktestResult(
        strategy_name=strategy.name,
        equity_curve=equity_curve,
        returns=net_returns,
        positions=positions,
    )
