import numpy as np
import pandas as pd

from quantlab.metrics import (
    cagr,
    max_drawdown,
    sharpe_ratio,
    summarize,
    volatility,
    win_rate,
)


def series(values: list[float]) -> pd.Series:
    return pd.Series(values, index=pd.date_range("2023-01-01", periods=len(values)))


def test_max_drawdown_simple():
    # peak @ 100, trough @ 70 -> 30%
    equity = series([100, 120, 90, 70, 85])
    # running peak is 120; lowest point 70 -> 70/120 - 1 = -0.4167
    assert abs(max_drawdown(equity) - (70 / 120 - 1)) < 1e-9


def test_max_drawdown_never_positive():
    equity = series([100, 110, 120, 130])  # only rises
    assert max_drawdown(equity) == 0.0


def test_win_rate_half():
    returns = series([0.01, -0.01, 0.02, -0.02])
    assert win_rate(returns) == 0.5


def test_win_rate_ignores_flat_days():
    returns = series([0.01, 0.0, 0.0, -0.01])
    # only 2 active days, 1 up -> 0.5
    assert win_rate(returns) == 0.5


def test_volaility_zero_for_constant_returns():
    returns = series([0.01, 0.01, 0.01, 0.01])
    assert volatility(returns) == 0.0


def test_sharpe_zero_when_no_volatility():
    returns = series([0.01, 0.01, 0.01])
    assert sharpe_ratio(returns) == 0.0


def test_sharpe_positive_for_good_returns():
    # mostly positive, low variance -> positive Sharpe
    returns = series([0.01, 0.012, 0.008, 0.011, 0.009])
    assert sharpe_ratio(returns) > 0


def test_cagr_doubles_in_one_year():
    # 252 days, value doubles -> 100% CAGR
    equity = series(list(np.linspace(1.0, 2.0, 252)))
    result = cagr(equity)
    assert abs(result - 1.0) < 0.01


def test_summarize_returns_all_keys():
    equity = series([100, 110, 105, 115])
    returns = equity.pct_change().fillna(0.0)
    result = summarize(equity, returns)
    assert set(result.keys()) == {
        "cagr",
        "volatility",
        "sharpe",
        "max_drawdown",
        "win_rate",
    }
