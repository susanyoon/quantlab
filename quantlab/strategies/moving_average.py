from __future__ import annotations

import pandas as pd

from quantlab.strategy import Strategy


class MovingAverageCrossover(Strategy):
    """
    Go long when a short moving average is above a long one, flat otherwise.

    A classic trend-following rule. Long-only: positions are 1.0 or 0.0.
    """

    def __init__(self, short_window: int = 20, long_window: int = 50):
        if short_window >= long_window:
            raise ValueError("short_window must be less than long_window.")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        short_ma = prices["close"].rolling(self.short_window).mean()
        long_ma = prices["close"].rolling(self.long_window).mean()

        signal = (short_ma > long_ma).astype(float)
        # Until the long window has enough data, stay flat
        signal[long_ma.isna()] = 0.0
        return signal

    @property
    def name(self) -> str:
        return f"MA({self.short_window},{self.long_window})"
