from __future__ import annotations

import pandas as pd

from quantlab.strategy import Strategy


class BuyAndHold(Strategy):
    """
    Hold a full long position the entire period. The benchmark.
    """

    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        return pd.Series(1.0, index=prices.index)
