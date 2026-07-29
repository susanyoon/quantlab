# QuantLab
![CI](https://github.com/susanyoon/quantlab/actions/workflows/ci.yml/badge.svg)

A configurable backtesting and strategy research platform for evaluating trading strategies against historical market data. Built around a pluggable strategy interface and a no-lookahead backtest engine, with risk-adjusted performance metrics.

## Features

- [x] Historical price data fetching with local caching
- [x] Pluggable strategy interface
- [x] Event-driven backtest engine with transaction costs
- [x] Performance metrics (Sharpe, max drawdown, CAGR, win rate)
- [ ] Walk-forward validation
- [ ] YAML-configured experiment runs
- [ ] Strategy comparison reports and equity curve charts

## Example

Comparing a moving-average crossover against buy-and-hold on AAPL (2020–2022):

| Strategy    | Total Return | Sharpe | Max Drawdown |
|-------------|-------------|--------|--------------|
| MA(20,50)   | +40.9%      | 0.61   | -25.4%       |
| Buy & Hold  | +76.4%      | 0.70   | -31.4%       |

Buy-and-hold earned more, but at higher risk — nearly identical Sharpe ratios
show the extra return was mostly compensation for volatility, not skill.