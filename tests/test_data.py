import pandas as pd
import pytest

from quantlab.data import DataError, _normalize, fetch_prices


def test_normalize_lowercases_and_sorts():
    raw = pd.DataFrame(
        {
            "Open": [1.0, 2.0],
            "High": [1.0, 2.0],
            "Low": [1.0, 2.0],
            "Close": [1.0, 2.0],
            "Volume": [10, 20],
        },
        index=pd.to_datetime(["2023-01-04", "2023-01-03"]),
    )
    df = _normalize(raw)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.index[0] < df.index[1]


def test_normalize_raises_on_missing_columns():
    raw = pd.DataFrame(
        {"Open": [1.0], "Close": [1.0]}, index=pd.to_datetime(["2023-01-03"])
    )
    with pytest.raises(DataError):
        _normalize(raw)


def test_fetch_reads_from_cache(monkeypatch, tmp_path):
    import quantlab.data as data_module

    monkeypatch.setattr(data_module, "CACHE_DIR", data_module.Path("tests/data"))
    df = fetch_prices("AAPL", "2023-01-03", "2023-01-06")
    assert len(df) == 3
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df["close"].iloc[-1] == 104.0


def test_fetch_cache_avoids_network(monkeypatch):
    """
    If the cache hit works, yf.download must never be called.
    """
    import quantlab.data as data_module

    monkeypatch.setattr(data_module, "CACHE_DIR", data_module.Path("tests/data"))

    def explode(*args, **kwargs):
        raise AssertionError("Network should not be hit on a cache hit.")

    monkeypatch.setattr(data_module.yf, "download", explode)
    df = fetch_prices("AAPL", "2023-01-03", "2023-01-06")
    assert not df.empty
