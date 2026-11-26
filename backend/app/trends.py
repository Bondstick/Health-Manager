"""Trend rules for readings. Pure Python, no database, so they are easy to test.

The threshold is a demo assumption, not a clinical standard.
"""

from dataclasses import dataclass

RISING_THRESHOLD = 5  # change across the window that counts as a real rise or fall


@dataclass
class Trend:
    direction: str  # rising, falling, stable, not_enough_data
    change: float | None
    summary: str


def compute_trend(values: list[float], unit: str, label: str, days: int) -> Trend:
    """values must be in time order, oldest first."""
    if len(values) < 3:
        return Trend("not_enough_data", None, f"Not enough readings to show a trend for {label}.")

    change = values[-1] - values[0]
    if change >= RISING_THRESHOLD:
        direction = "rising"
        words = f"up {change:g} {unit}"
    elif change <= -RISING_THRESHOLD:
        direction = "falling"
        words = f"down {abs(change):g} {unit}"
    else:
        direction = "stable"
        words = f"stable (change {change:+g} {unit})"

    return Trend(direction, change, f"{label} {words} over {days} days")
