import pandas as pd
import pytest

from financepy.trading.environment import TradingEnvironment


def test_basic_trading_environment():
    data = pd.DataFrame({'Close': [10, 11, 12, 13, 14]})

    def buy_two(env: TradingEnvironment) -> int:
        return 2

    env = TradingEnvironment(data, initial_cash=100)
    df = env.run(buy_two)

    assert isinstance(df, pd.DataFrame)
    assert df.iloc[-1]['position'] == 10
    assert round(df.iloc[-1]['cash'], 2) == -20
    assert round(env.portfolio_value(), 2) == 120
    assert env.current_price == 14


def test_missing_close_column():
    with pytest.raises(ValueError):
        TradingEnvironment(pd.DataFrame({'Price': [1, 2, 3]}))

