from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def cagr(equity_curve: pd.Series) -> float:
    """
    Compound annual growth rate.
    Assumes daily data: annualizes based on 252 trading days per year.
    """
    if len(equity_curve) < 2:
        return 0.0
    total_growth = equity_curve.iloc[-1] / equity_curve.iloc[0]
    years = len(equity_curve) / TRADING_DAYS_PER_YEAR
    if years == 0 or total_growth <= 0:
        return 0.0
    return float(total_growth ** (1 / years) - 1)


def volatility(returns: pd.Series) -> float:
    """
    Annualized standard deviation of daily returns.
    """
    return float(returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR))


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Annualized Sharpe ratio: excess return per unit of volatility.

    Args:
        returns: Daily return series.
        risk_free_rate: Annual risk-free rate (default 0).
    """
    excess = returns - risk_free_rate / TRADING_DAYS_PER_YEAR
    std = returns.std()
    if std == 0:
        return 0.0
    return float(excess.mean() / std * np.sqrt(TRADING_DAYS_PER_YEAR))


def max_drawdown(equity_curve: pd.Series) -> float:
    """
    Largest peak-to-trough decline, as a negative fraction.
    A return of -0.30 means the portfolio fell 30% from a prior peak.
    """
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1.0
    return float(drawdown.min())


def win_rate(returns: pd.Series) -> float:
    """
    Fraction of days with a positive return.
    """
    active = returns[returns != 0.0]
    if len(active) == 0:
        return 0.0
    return float((active > 0).sum() / len(active))


def summarize(equity_curve: pd.Series, returns: pd.Series) -> dict[str, float]:
    """
    Compute all metrics at once, for reports.
    """
    return {
        "cagr": cagr(equity_curve),
        "volatility": volatility(returns),
        "sharpe": sharpe_ratio(returns),
        "max_drawdown": max_drawdown(equity_curve),
        "win_rate": win_rate(returns),
    }
