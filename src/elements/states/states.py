import operator
from typing import Annotated, Dict, Any
from typing_extensions import TypedDict, List
from dataclasses import dataclass

@dataclass
class State:
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """

    changeme: str = "example"
class TestState(TypedDict):
    changeme: str = ""
    l = Annotated[List, operator.add]