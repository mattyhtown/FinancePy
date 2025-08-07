# FinancePy

[![PyPI version](https://badge.fury.io/py/financepy.svg)](https://badge.fury.io/py/financepy)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub Actions Status](https://github.com/domokane/FinancePy/workflows/run-unit-tests/badge.svg)](https://github.com/domokane/FinancePy/actions)

A Python-based library for financial securities valuation, covering a wide range of vanilla and exotic options, futures, and other derivatives.

## Key Features

*   **Comprehensive Product Coverage:** Value a wide range of equity, FX, interest rate, and credit derivatives.
*   **Variety of Models:** Includes Black-Scholes, local volatility, stochastic volatility, and multi-factor models.
*   **High Performance:** Achieves speeds comparable to C++ by leveraging Numba for just-in-time compilation.
*   **User-Friendly Design:** A product-based, intuitive API that is easy for both students and professionals to use.
*   **Extensive Documentation:** Over 60 Jupyter notebooks provide detailed examples and a full PDF manual is also available.

## Getting Started

### Installation

FinancePy can be installed from PyPI using `pip`:

```bash
pip install financepy
```

To upgrade an existing installation:

```bash
pip install --upgrade financepy
```

### Quick Start

Here is a simple example of how to value a European vanilla call option:

```python
from financepy.utils import *
from financepy.products.equity import *

# Define the option
valuation_date = Date(1, 1, 2015)
expiry_date = valuation_date.add_years(0.5)
strike_price = 50.0
call_option = EquityVanillaOption(expiry_date, strike_price, OptionTypes.EUROPEAN_CALL)

# Define the market
stock_price = 50.0
volatility = 0.20
interest_rate = 0.05
dividend_yield = 0.0
discount_curve = DiscountCurveFlat(valuation_date, interest_rate, FrequencyTypes.CONTINUOUS)
dividend_curve = DiscountCurveFlat(valuation_date, dividend_yield)

# Define the model
model = BlackScholes(volatility)

# Value the option
price = call_option.value(valuation_date, stock_price, discount_curve, dividend_curve, model)

print(f"Price of the call option: {price:.4f}")
```

## Dependencies

FinancePy has the following dependencies:

*   `numpy`
*   `numba`
*   `scipy`
*   `llvmlite`
*   `ipython`
*   `matplotlib`
*   `pandas`
*   `prettytable`

## Documentation

The `notebooks` and `book` directories in this repository contain over 60 Jupyter notebooks with detailed examples on how to use the library. There is also a comprehensive PDF manual, `FinancePyManual.pdf`, in the root directory.

## Contributing

If you have knowledge of Quantitative Finance and Python, please consider contributing. You can find tasks in the Issues section. Before you begin, please comment on the issue thread.

*   Code should be PEP8 compliant.
*   Comments are required for every class and function.
*   At least one broad test case and a set of unit tests must be provided for every function.
*   Readability and speed are the priorities.

## License

This project is licensed under the GPL-3.0 License. See the `LICENSE` file for details.

## Author

**Dominic O'Kane** is a Professor of Finance at the EDHEC Business School in Nice, France.

*   **Email:** dominic.okane@edhec.edu
*   **GitHub:** [domokane](https://github.com/domokane)
