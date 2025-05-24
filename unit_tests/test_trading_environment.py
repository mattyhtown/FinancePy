import sys
sys.path.append("..")
import pandas as pd
import pytest

from financepy.trading.environment import TradingEnvironment


def test_run_returns_dataframe_and_multiple_units():
    data = pd.DataFrame({'Close': [10, 11, 12, 13, 14]})

    def buy_two(env: TradingEnvironment):
        return 2

    env = TradingEnvironment(data, initial_cash=100)
    df = env.run(buy_two)

    # final position should be 10 units with cash -20
    assert df.iloc[-1]["position"] == 10
    assert round(df.iloc[-1]["cash"], 2) == -20
    assert round(env.portfolio_value(), 2) == 120
    # run should return same dataframe as history_dataframe
    pd.testing.assert_frame_equal(df, env.history_dataframe())


def test_missing_close_column_raises():
    data = pd.DataFrame({'price': [1, 2, 3]})
    with pytest.raises(KeyError):
        TradingEnvironment(data)

