from __future__ import annotations

from collections.abc import Callable, Iterable

import pandas as pd

from quantlab.engine import run_backtest
from quantlab.metrics import sharpe_ratio
from quantlab.strategy import Strategy


def best_parameters(
    strategy_factory: Callable[..., Strategy],
    param_grid: Iterable[dict],
    prices: pd.DataFrame,
    score: Callable[[pd.Series], float] = sharpe_ratio,
) -> dict:
    """
    Find the parameter set that maximizes a score on the given prices.

    Args:
        strategy_factory: Callable that builds a Strategy from keyword params,
            e.g. lambda **p: MovingAverageCrossover(**p).
        param_grid: Iterable of parameter dicts to try.
        prices: Price data to optimize on (the in-sample window).
        score: Function mapping a return series to a number to maximize.
            Defaults to Sharpe ratio.

    Returns:
        The parameter dict with the highest score.
    """
    best_params = None
    best_score = float("-inf")

    for params in param_grid:
        strategy = strategy_factory(**params)
        result = run_backtest(strategy, prices)
        s = score(result.returns)
        if s > best_score:
            best_score = s
            best_params = params

    if best_params is None:
        raise ValueError("param_grid was empty.")

    return best_params
