"""Simple algorithmic trading environment for backtesting strategies."""

import pandas as pd
from typing import Callable, List, Dict


class TradingEnvironment:
    """Environment to simulate simple trading strategies.

    Parameters
    ----------
    data : pandas.DataFrame
        Price data containing a ``Close`` column.
    initial_cash : float, optional
        Starting cash for the strategy, by default ``100000``.
    """

    def __init__(self, data: pd.DataFrame, initial_cash: float = 100000.0):
        self.data = data.reset_index(drop=True)
        self.initial_cash = initial_cash
        self.reset()

    def reset(self) -> None:
        """Reset the environment to the initial state."""
        self.current_step = 0
        self.cash = self.initial_cash
        self.position = 0
        self.history: List[Dict[str, float]] = []

    def step(self, action: int) -> None:
        """Move one time step applying ``action``.

        Parameters
        ----------
        action : int
            ``1`` to buy one unit, ``-1`` to sell one unit and ``0`` to hold.
        """
        price = self.data.loc[self.current_step, "Close"]

        if action == 1:
            self.position += 1
            self.cash -= price
        elif action == -1:
            self.position -= 1
            self.cash += price

        portfolio_value = self.cash + self.position * price
        self.history.append(
            {
                "step": self.current_step,
                "price": price,
                "cash": self.cash,
                "position": self.position,
                "value": portfolio_value,
            }
        )

        self.current_step += 1

    def run(self, strategy: Callable[["TradingEnvironment"], int]) -> None:
        """Run ``strategy`` until price data is exhausted."""
        self.reset()
        while self.current_step < len(self.data):
            action = strategy(self)
            self.step(action)

    def portfolio_value(self) -> float:
        """Return the latest portfolio value."""
        if not self.history:
            return self.initial_cash
        return self.history[-1]["value"]

    def history_dataframe(self) -> pd.DataFrame:
        """Return historical portfolio data as ``DataFrame``."""
        return pd.DataFrame(self.history)
