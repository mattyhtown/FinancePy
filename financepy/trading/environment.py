"""Simple algorithmic trading environment for backtesting strategies.

This utility is intentionally minimal.  It allows a strategy callback to
consume a ``TradingEnvironment`` instance and return a trade quantity at each
step.  Positive numbers buy units of the asset while negative numbers sell.
The environment records the portfolio state after each step and can return the
history as a :class:`pandas.DataFrame` for further analysis.
"""

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
        if "Close" not in data.columns:
            raise ValueError("data must contain a 'Close' column")

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
            Number of units to buy (positive) or sell (negative). ``0`` means no
            trade.
        """
        price = self.data.loc[self.current_step, "Close"]

        if action > 0:
            self.position += action
            self.cash -= price * action
        elif action < 0:
            self.position += action
            self.cash -= price * action
        else:
            pass

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

    def run(self, strategy: Callable[["TradingEnvironment"], int]) -> pd.DataFrame:
        """Run ``strategy`` until price data is exhausted.

        Parameters
        ----------
        strategy : Callable[[TradingEnvironment], int]
            Callback receiving the environment and returning an integer quantity
            to trade each step.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the history of the run.
        """
        self.reset()
        while self.current_step < len(self.data):
            action = strategy(self)
            self.step(action)

        return self.history_dataframe()

    def portfolio_value(self) -> float:
        """Return the latest portfolio value."""
        if not self.history:
            return self.initial_cash
        return self.history[-1]["value"]

    def history_dataframe(self) -> pd.DataFrame:
        """Return historical portfolio data as ``DataFrame``."""
        return pd.DataFrame(self.history)

    @property
    def current_price(self) -> float:
        """Return the current market price."""
        if self.current_step == 0:
            return self.data.loc[0, "Close"]
        return self.data.loc[min(self.current_step - 1, len(self.data) - 1), "Close"]
