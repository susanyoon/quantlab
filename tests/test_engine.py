import pandas as pd

from quantlab.engine import run_backtest
from quantlab.strategies.buy_and_hold import BuyAndHold
from quantlab.strategy import Strategy


def make_prices(closes: list[float]) -> pd.DataFrame:
    idx = pd.date_range("2023-01-01", periods=len(closes), freq="D")
    return pd.DataFrame({"close": closes}, index=idx)


class AlwaysFlat(Strategy):
    def generate_signals(self, prices):
        return pd.Series(0.0, index=prices.index)


def test_flat_strategy_never_moves():
    prices = make_prices([100, 110, 121, 133])
    result = run_backtest(AlwaysFlat(), prices, cost_per_trade=0.0)
    # never invested -> equity stays flat
    assert result.equity_curve.iloc[-1] == result.equity_curve.iloc[0]
    assert result.total_return == 0.0


def test_buy_and_hold_matches_price_return_minus_first_day():
    # prices double from 100 to 200 oer the held period
    prices = make_prices([100, 200])
    result = run_backtest(BuyAndHold(), prices, cost_per_trade=0.0)
    # day 1 position is 1.0, shifted -> day 2 earns the +100% return
    assert abs(result.total_return - 1.0) < 1e-9


def test_lookahead_shift_applied():
    """
    Position on day N earns return on day N+1, not day N.
    """
    prices = make_prices([100, 100, 200, 200])

    # go long only on a day index 1 (the jump to 200 happens on index 2)
    class LongOnDayOne(Strategy):
        def generate_signals(self, prices):
            s = pd.Series(0.0, index=prices.index)
            s.iloc[1] = 1.0
            return s

    result = run_backtest(LongOnDayOne(), prices, cost_per_trade=0.0)
    # position on index 1 -> earns index 2's +100% return. Captured.
    assert abs(result.total_return - 1.0) < 1e-9


def test_transaction_costs_reduce_returns():
    prices = make_prices([100, 100, 100])
    result_free = run_backtest(BuyAndHold(), prices, cost_per_trade=0.0)
    result_costly = run_backtest(BuyAndHold(), prices, cost_per_trade=0.01)
    # with flat prices, only cost differentiates them
    assert result_costly.total_return < result_free.total_return


def test_result_series_aligned():
    prices = make_prices([100, 101, 102])
    result = run_backtest(BuyAndHold(), prices)
    assert result.equity_curve.index.equals(prices.index)
    assert len(result.returns) == len(prices)
