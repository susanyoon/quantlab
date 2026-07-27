from dataclasses import dataclass
from datetime import date


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
