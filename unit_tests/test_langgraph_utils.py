import sys
import pytest

from financepy.utils.langgraph_utils import build_black_scholes_graph


def test_build_graph_no_langgraph():
    """Ensure ImportError is raised when langgraph is missing."""
    if "langgraph" in sys.modules:
        pytest.skip("langgraph installed")

    def dummy_llm(prompt):
        return {}

    with pytest.raises(ImportError):
        build_black_scholes_graph(dummy_llm)
