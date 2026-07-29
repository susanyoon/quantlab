import pandas as pd

from quantlab.optimize import best_parameters
from quantlab.strategies.moving_average import MovingAverageCrossover
from quantlab.walkforward import walk_forward


def trending_prices(n: int) -> pd.DataFrame:
    idx = pd.date_range("2020-01-01", periods=n)
    return pd.DataFrame({"close": [100 + i for i in range(n)]}, index=idx)


def ma_factory(**params):
    return MovingAverageCrossover(**params)


GRID = [
    {"short_window": 5, "long_window": 10},
    {"short_window": 10, "long_window": 20},
]


def test_best_parameters_returns_a_grid_member():
    prices = trending_prices(100)
    best = best_parameters(ma_factory, GRID, prices)
    assert best in GRID


def test_best_parameters_empty_grid_raises():
    prices = trending_prices(50)
    try:
        best_parameters(ma_factory, [], prices)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_walk_forward_produces_out_of_sample_returns():
    prices = trending_prices(200)
    oos = walk_forward(ma_factory, GRID, prices, train_size=50, test_size=25)
    assert isinstance(oos, pd.Series)
    assert len(oos) > 0


def test_walk_forward_covers_multiple_windows():
    prices = trending_prices(200)
    oos = walk_forward(ma_factory, GRID, prices, train_size=50, test_size=25)
    # with 200 rows, train=50, test=25: windows tile several test blocks
    # each test block is 25 rows -> expect a multiple of 25
    assert len(oos) % 25 == 0
    assert len(oos) >= 50  # at least two test windows


def test_walk_forward_raises_when_too_little_data():
    prices = trending_prices(40)
    try:
        walk_forward(ma_factory, GRID, prices, train_size=50, test_size=25)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_walk_forward_test_windows_dont_overlap():
    prices = trending_prices(200)
    oos = walk_forward(ma_factory, GRID, prices, train_size=50, test_size=25)
    # no duplicate dates -> windows are disjoint
    assert oos.index.is_unique
