from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    """
    Base class for all trading strategies.

    A strategy inspects price history & emits a target position for each day:
    a value in [-1.0, 1.0] representing the fraction of the portfolio to
    allocate (1.0 = fully long, 0.0 = flat, -1.0 = fully short).

    Subclasses implement 'generate_signals', which must not use any information
    from the future (no lookahead).
    """

    @abstractmethod
    def generate_signals(self, prices: pd.DataFrame) -> pd.Series:
        """
        Compute target positions for each day in 'prices'.

        Args:
            prices: OHLCV DataFrame indexed by date, ascending.

        Returns:
            A Series indexed identically to 'prices', with values in
            [-1.0, 1.0]. Each value is the target position to hold going
            into the NEXT day, computed using only data up to and including that day.
        """
        ...

    @property
    def name(self) -> str:
        """
        Human-readable strategy name, used in reports.
        """
        return self.__class__.__name__
