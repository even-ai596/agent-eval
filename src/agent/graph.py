"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""
from __future__ import annotations
import os
import sys
sys.path.append(os.getcwd())


from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from src.elements.states.states import EvaluationState
from src.elements.nodes.nodes import get_intent_node
from src.elements.pymodels.pymodels import Evaluation

# Define the graph
graph = (
    StateGraph(EvaluationState)
    .add_node(get_intent_node)
    .add_edge("__start__", "get_intent_node")
    .add_edge("get_intent_node", "__end__")
    .compile(name="Evaluation Graph")
)
s = graph.invoke({"evaluations": [Evaluation(), Evaluation(), Evaluation()]})
print(s)
