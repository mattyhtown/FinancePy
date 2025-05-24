"""Simple algorithmic trading environment for backtesting strategies."""

import pandas as pd
from typing import Callable, List, Dict, Union


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
            raise KeyError("data must contain 'Close' column")
        self.data = data.reset_index(drop=True)
        self.initial_cash = initial_cash
        self.reset()

    def reset(self) -> None:
        """Reset the environment to the initial state."""
        self.current_step = 0
        self.cash = self.initial_cash
        self.position = 0
        self.history: List[Dict[str, float]] = []

    def step(self, action: Union[int, float]) -> None:
        """Move one time step executing ``action`` units.

        Parameters
        ----------
        action : int or float
            The number of units to buy (positive) or sell (negative).

        Raises
        ------
        TypeError
            If action is not an int or float and cannot be coerced to float.
        """
        # Runtime type checking or coercion for action
        if not isinstance(action, (int, float)):
            try:
                action = float(action)
            except (TypeError, ValueError):
                raise TypeError(f"Action must be an int or float, got {type(action).__name__}")

        Parameters
        ----------
        action : int or float
            Positive values buy units, negative values sell units and ``0`` holds.
        """
        price = self.data.loc[self.current_step, "Close"]

        if action != 0:
            self.position += action
            self.cash -= action * price

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

    def run(self, strategy: Callable[["TradingEnvironment"], Union[int, float]]) -> pd.DataFrame:
        """Run ``strategy`` until price data is exhausted.

        Parameters
        ----------
        strategy : callable
            Function returning the quantity to trade each step.

        Returns
        -------
        pandas.DataFrame
            Historical portfolio data for the run.
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

    @property
    def current_price(self) -> float:
        """Return the price at the current step."""
        if self.current_step == 0:
            return float(self.data.loc[0, "Close"])
        step = min(self.current_step, len(self.data) - 1)
        return float(self.data.loc[step, "Close"])

    def history_dataframe(self) -> pd.DataFrame:
        """Return historical portfolio data as ``DataFrame``."""
        return pd.DataFrame(self.history)
