from quantlab.strategies.buy_and_hold import BuyAndHold
from quantlab.strategies.moving_average import MovingAverageCrossover

STRATEGY_REGISTRY = {
    "moving_average": MovingAverageCrossover,
    "buy_and_hold": BuyAndHold,
}


def build_strategy(name: str, params: dict):
    """Instantiate a registered strategy by name."""
    if name not in STRATEGY_REGISTRY:
        raise ValueError(
            f"Unknown strategy {name!r}. Available: {sorted(STRATEGY_REGISTRY)}"
        )
    return STRATEGY_REGISTRY[name](**params)
