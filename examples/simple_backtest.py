"""Example script demonstrating the TradingEnvironment."""

import pandas as pd
from financepy.trading.environment import TradingEnvironment

prices = pd.DataFrame({"Close": [10, 11, 12, 13, 14]})

def buy_every_step(env: TradingEnvironment) -> int:
    return 1

if __name__ == "__main__":
    env = TradingEnvironment(prices, initial_cash=100)
    history = env.run(buy_every_step)
    print(history)
    print("Final value:", env.portfolio_value())

