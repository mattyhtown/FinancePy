"""Utilities for DAX 0DTE trading examples."""

from pathlib import Path
import pandas as pd

from .environment import TradingEnvironment
from ..models.black_scholes_analytic import bs_value
from ..utils.global_types import OptionTypes

_DATA_PATH = Path(__file__).resolve().parents[2] / "unit_tests" / "data" / "dax_odte.csv"


def load_sample_prices() -> pd.DataFrame:
    """Return sample DAX intraday prices used for 0DTE examples."""
    return pd.read_csv(_DATA_PATH)


def create_environment(initial_cash: float = 100000.0) -> TradingEnvironment:
    """Return a :class:`TradingEnvironment` with sample DAX prices."""
    data = load_sample_prices()
    return TradingEnvironment(data, initial_cash)


def price_intraday_option(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    option_type: OptionTypes = OptionTypes.EUROPEAN_CALL,
    div: float = 0.0,
    t: float = 1 / 252,
) -> float:
    """Price a DAX option expiring today using Black-Scholes."""
    return float(bs_value(spot, t, strike, rate, div, vol, option_type.value))
