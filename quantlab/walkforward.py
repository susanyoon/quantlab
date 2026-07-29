from __future__ import annotations

from collections.abc import Callable, Iterable

import pandas as pd

from quantlab.engine import run_backtest
from quantlab.optimize import best_parameters
from quantlab.strategy import Strategy


def walk_forward(
    strategy_factory: Callable[..., Strategy],
    param_grid: Iterable[dict],
    prices: pd.DataFrame,
    train_size: int,
    test_size: int,
) -> pd.Series:
    """
    Run walk-forward validation.

    Repeatedly: optimize parameters on a `train_size` window, then apply them
    to the following `test_size` window. The out-of-sample return series from
    each test window are concatenated into one honest equity-relevant series.

    Args:
        strategy_factory: Builds a Strategy from keyword params.
        param_grid: Parameter dicts to search over each training window.
        prices: Full price history.
        train_size: Number of rows in each in-sample (training) window.
        test_size: Number of rows in each out-of-sample (test) window.

    Returns:
        Concatenated out-of-sample daily returns across all test windows.
    """
    grid = list(param_grid)  # reusable across iterations
    oos_returns = []

    start = 0
    while start + train_size + test_size <= len(prices):
        train = prices.iloc[start : start + train_size]
        test = prices.iloc[start + train_size : start + train_size + test_size]
        params = best_parameters(strategy_factory, grid, train)
        strategy = strategy_factory(**params)
        result = run_backtest(strategy, test)
        oos_returns.append(result.returns)
        start += test_size  # roll forward by 1 test window
    if not oos_returns:
        raise ValueError(
            "Not enough data for even 1 train/test split. "
            "Reduce train_size or test_size."
        )
    return pd.concat(oos_returns)
