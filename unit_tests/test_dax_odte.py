import pandas as pd

from financepy.trading.dax_odte import create_environment, load_sample_prices, price_intraday_option
from financepy.utils.global_types import OptionTypes


def test_load_sample_prices():
    df = load_sample_prices()
    assert not df.empty
    assert "Close" in df.columns


def test_create_environment():
    env = create_environment(initial_cash=1000)
    assert env.current_price == env.data.loc[0, "Close"]
    assert env.cash == 1000


def test_price_intraday_option_zero_t_equals_intrinsic():
    price = price_intraday_option(16030, 16000, 0.0, 0.2, t=0)
    assert abs(price - (16030 - 16000)) < 1e-8
