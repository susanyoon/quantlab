from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from quantlab.engine import run_backtest  # noqa: E402
from quantlab.metrics import summarize  # noqa: E402
from quantlab.strategy import Strategy  # noqa: E402


def compare_strategies(
    strategies: list[Strategy], prices: pd.DataFrame
) -> pd.DataFrame:
    """
    Run several strategies over the same prices & tabulate their metrics.

    Returns:
        A DataFrame indexed by strategy name, 1 column per metric.
    """
    rows = {}
    for strat in strategies:
        result = run_backtest(strat, prices)
        rows[strat.name] = summarize(result.equity_curve, result.returns)
    return pd.DataFrame(rows).T


def plot_equity_curves(
    strategies: list[Strategy], prices: pd.DataFrame, output_path: str
) -> None:
    """
    Plot each strategy's equity curve on 1 chart & save as PNG.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for strat in strategies:
        result = run_backtest(strat, prices)
        ax.plot(result.equity_curve.index, result.equity_curve.values, label=strat.name)
    ax.set_title("Strategy Comparison - Equity Curves")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio value (growth of $1)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)
