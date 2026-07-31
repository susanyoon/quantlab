import pandas as pd

from quantlab.report import compare_strategies, plot_equity_curves
from quantlab.strategies.buy_and_hold import BuyAndHold
from quantlab.strategies.moving_average import MovingAverageCrossover


def make_prices(n: int) -> pd.DataFrame:
    idx = pd.date_range("2020-01-01", periods=n)
    return pd.DataFrame({"close": [100 + i for i in range(n)]}, index=idx)


def test_compare_returns_row_per_strategy():
    prices = make_prices(100)
    strategies = [BuyAndHold(), MovingAverageCrossover(5, 20)]
    df = compare_strategies(strategies, prices)
    assert len(df) == 2
    assert "sharpe" in df.columns


def test_plot_creates_png(tmp_path):
    prices = make_prices(100)
    out = tmp_path / "chart.png"
    plot_equity_curves([BuyAndHold()], prices, str(out))
    assert out.exists()
    assert out.stat().st_size > 0
