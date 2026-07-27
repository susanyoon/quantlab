from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

CACHE_DIR = Path("data/cache")

EXPECTED_COLUMNS = ["open", "high", "low", "close", "volume"]


class DataError(Exception):
    """
    Raised when price data can't be fetched or is invalid.
    """


def _cache_path(ticker: str, start: str, end: str) -> Path:
    safe = f"{ticker.upper()}_{start}_{end}.parquet"
    return CACHE_DIR / safe


def fetch_prices(
    ticker: str,
    start: str,
    end: str,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Fetch daily OHLCV price data for a ticker.

    Args:
        ticker: Stock symbol, e.g. "AAPL".
        start: Start date, "YYYY-MM-DD" (inclusive).
        end: End date, "YYYY-MM-DD" (exclusive, per yfinance convention).
        use_cache: If True, read from and write to the local cache.

    Returns:
        A DataFrame indexed by date with columns:
        open, high, low, close, volume. Sorted ascending by date.

    Raises:
        DataError: If no data is returned for the ticker/date range.
    """
    cache_file = _cache_path(ticker, start, end)

    if use_cache and cache_file.exists():
        return pd.read_parquet(cache_file)

    raw = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=True,
    )

    if raw is None or raw.empty:
        raise DataError(f"No data returned for {ticker!r} between {start} and {end}.")

    df = _normalize(raw)

    if use_cache:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file)

    return df


def _normalize(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize yfinance output to lowercase OHLCV, sorted by date.
    """
    df = raw.copy()

    # yfinance can return a MultiIndex on columns for single tickers;
    # flatten it to just the price field name.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [str(c).lower() for c in df.columns]
    df = df[[c for c in EXPECTED_COLUMNS if c in df.columns]]
    df = df.sort_index()
    df.index.name = "date"

    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise DataError(f"Data missing expected columns: {sorted(missing)}")

    return df
