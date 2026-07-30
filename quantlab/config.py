from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ExperimentConfig:
    """
    A fully-specified backtest experiment, loaded from YAML.
    """

    ticker: str
    start: str
    end: str
    strategy: str
    params: dict = field(default_factory=dict)
    cost_per_trade: float = 0.001


def load_config(path: str) -> ExperimentConfig:
    """
    Load & validate an experiment config from a YAML file.
    """
    raw = yaml.safe_load(Path(path).read_text())
    if raw is None:
        raise ValueError(f"Config file {path!r} is empty.")

    required = {"ticker", "start", "end", "strategy"}
    missing = required - raw.keys()
    if missing:
        raise ValueError(f"Config missing required keys: {sorted(missing)}")

    return ExperimentConfig(
        ticker=raw["ticker"],
        start=raw["start"],
        end=raw["end"],
        strategy=raw["strategy"],
        params=raw.get("params", {}),
        cost_per_trade=raw.get("cost_per_trade", 0.001),
    )
