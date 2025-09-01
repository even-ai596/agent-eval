import operator
from typing import Annotated, Dict, Any, Literal
from typing_extensions import TypedDict, List
from dataclasses import dataclass
from src.elements.pymodels.pymodels import Evaluation
@dataclass
class State:
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """

    changeme: str = "example"
class EvaluationState(TypedDict):
    evaluations: Evaluation

    attribution: str
    # l = Annotated[List, operator.add]