from dataclasses import dataclass
from datetime import date

import pandas as pd


@dataclass(frozen=True)
class PriceBar:
    """
    One day of OHLCV data for a single ticker.
    """

    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass
class BacktestResult:
    """
    The outcome of running 1 strategy over 1 price series.
    """

    strategy_name: str
    equity_curve: pd.Series  # portfolio value over time, starts at 1.0
    returns: pd.Series  # daily strategy returns
    positions: pd.Series  # target position held each day

    @property
    def total_return(self) -> float:
        """
        Overall return as a fraction, e.g. 0.25 = +25%.
        """
        return float(self.equity_curve.iloc[-1] / self.equity_curve.iloc[0] - 1.0)
