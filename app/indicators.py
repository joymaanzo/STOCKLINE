from collections.abc import Sequence


def simple_moving_average(prices: Sequence[float], window: int = 20) -> float | None:
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window


def momentum(prices: Sequence[float], window: int = 20) -> float | None:
    if len(prices) < window:
        return None
    starting_price = prices[-window]
    if starting_price == 0:
        return None
    return (prices[-1] - starting_price) / starting_price * 100


def moving_average_trend(prices: Sequence[float]) -> float | None:
    if len(prices) < 20:
        return None
    short_average = simple_moving_average(prices, 5)
    long_average = simple_moving_average(prices, 20)
    if short_average is None or long_average in (None, 0):
        return None
    return (short_average - long_average) / long_average * 100