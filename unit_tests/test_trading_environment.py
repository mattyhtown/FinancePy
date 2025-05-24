import sys
sys.path.append("..")
import pandas as pd
from financepy.trading.environment import TradingEnvironment


def test_basic_trading_environment():
    data = pd.DataFrame({'Close': [10, 11, 12, 13, 14]})

    def buy_every_step(env: TradingEnvironment):
        return 1

    env = TradingEnvironment(data, initial_cash=100)
    env.run(buy_every_step)
    df = env.history_dataframe()
    assert df.iloc[-1]['position'] == 5
    assert round(df.iloc[-1]['cash'], 2) == 40
    assert round(env.portfolio_value(), 2) == 110

