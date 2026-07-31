from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from quantlab.config import load_config
from quantlab.data import fetch_prices
from quantlab.engine import run_backtest
from quantlab.metrics import summarize
from quantlab.report import compare_strategies, plot_equity_curves
from quantlab.strategies import build_strategy

app = typer.Typer(help="QuantLab: a backtesting research platform.")
console = Console()


@app.callback()
def main():
    """
    QuantLab: a backtesting research platform.
    """
    pass


@app.command()
def run(config_file: str):
    """
    Run a backtest from a YAML config file.
    """
    cfg = load_config(config_file)
    prices = fetch_prices(cfg.ticker, cfg.start, cfg.end)
    strategy = build_strategy(cfg.strategy, cfg.params)
    result = run_backtest(strategy, prices, cost_per_trade=cfg.cost_per_trade)
    metrics = summarize(result.equity_curve, result.returns)

    console.print(
        f"\n[bold]{strategy.name}[/bold] on {cfg.ticker} ({cfg.start} to {cfg.end})\n"
    )
    table = Table()
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Total Return", f"{result.total_return:+.1%}")
    table.add_row("CAGR", f"{metrics['cagr']:+.1%}")
    table.add_row("Volatility", f"{metrics['volatility']:.1%}")
    table.add_row("Sharpe", f"{metrics['sharpe']:.2f}")
    table.add_row("Max Drawdown", f"{metrics['max_drawdown']:.1%}")
    table.add_row("Win Rate", f"{metrics['win_rate']:.1%}")
    console.print(table)


@app.command()
def compare(config_file: str, chart: str = "charts/comparison.png"):
    """
    Compare all strategies from a config against the same data.
    """
    cfg = load_config(config_file)
    prices = fetch_prices(cfg.ticker, cfg.start, cfg.end)

    from quantlab.strategies import STRATEGY_REGISTRY

    strategies = [cls() for cls in STRATEGY_REGISTRY.values()]

    table_df = compare_strategies(strategies, prices)
    console.print(table_df.to_string(float_format=lambda x: f"{x:.3f}"))

    plot_equity_curves(strategies, prices, chart)
    console.print(f"\n[green]Chart saved to {chart}[/green]")


if __name__ == "__main__":
    app()
