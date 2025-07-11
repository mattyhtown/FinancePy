"""Optional utilities for integration with LangGraph."""

from typing import Dict, Any

try:
    from langgraph.graph import StateGraph, END
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    StateGraph = None
    END = None

from ..models.black_scholes_analytic import bs_value
from ..utils.global_types import OptionTypes


def build_black_scholes_graph(llm) -> "StateGraph":
    """Create a simple LangGraph workflow for pricing an option.

    Parameters
    ----------
    llm : callable
        Function taking a text prompt and returning a text response. Typically
        a language model from ``langgraph`` or ``langchain``.

    Returns
    -------
    StateGraph
        Compiled pricing graph.

    Notes
    -----
    This function requires :mod:`langgraph` to be installed.
    """
    if StateGraph is None or END is None:
        raise ImportError("langgraph is not installed")

    def request_parameters(state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = (
            "Provide option parameters as JSON with keys 'spot', 'strike',"
            " 'rate', 'div', 'vol', and 'maturity'."
        )
        response = llm(prompt)
        return {"params": llm.extract_json(response)}

    def price_option(state: Dict[str, Any]) -> Dict[str, Any]:
        p = state["params"]
        price = float(
            bs_value(
                float(p["spot"]),
                float(p["maturity"]),
                float(p["strike"]),
                float(p["rate"]),
                float(p.get("div", 0.0)),
                float(p["vol"]),
                OptionTypes.EUROPEAN_CALL.value,
            )
        )
        return {"price": price}

    graph = StateGraph()
    graph.add_node("params", request_parameters)
    graph.add_node("price", price_option)
    graph.add_edge("params", "price")
    graph.add_edge("price", END)
    return graph.compile()
