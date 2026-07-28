import pandas as pd
import pytest

from quantlab.strategy import Strategy
from quantlab.strategies.buy_and_hold import BuyAndHold
from quantlab.strategies.moving_average import MovingAverageCrossover


def make_prices(closes: list[float]) -> pd.DataFrame:
    idx = pd.date_range("2023-01-01", periods=len(closes), freq="D")
    return pd.DataFrame({"close": closes}, index=idx)


def test_strategy_is_abstract():
    with pytest.raises(TypeError):
        Strategy()


def test_buy_and_hold_always_full_long():
    prices = make_prices([10, 11, 12, 13])
    signals = BuyAndHold().generate_signals(prices)
    assert (signals == 1.0).all()
    assert len(signals) == len(prices)


def test_ma_crossover_validates_windows():
    with pytest.raises(ValueError):
        MovingAverageCrossover(short_window=50, long_window=20)


def test_ma_crossover_flat_until_enough_data():
    prices = make_prices(list(range(100)))
    strat = MovingAverageCrossover(short_window=5, long_window=10)
    signals = strat.generate_signals(prices)
    # First 9 days can't have a 10-day average -> flat.
    assert (signals.iloc[:9] == 0.0).all()


def test_ma_crossover_goes_long_in_uptrend():
    # steadily rising prices -> short MA above long MA -> long
    prices = make_prices(list(range(100)))
    strat = MovingAverageCrossover(short_window=5, long_window=10)
    signals = strat.generate_signals(prices)
    assert signals.iloc[-1] == 1.0


def test_signals_indexed_like_prices():
    prices = make_prices([10, 11, 12, 13, 14])
    signals = MovingAverageCrossover(2, 3).generate_signals(prices)
    assert signals.index.equals(prices.index)


def test_name_property():
    assert MovingAverageCrossover(20, 50).name == "MA(20,50)"
    assert BuyAndHold().name == "BuyAndHold"
