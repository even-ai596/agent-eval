from langgraph.types import Send
from src.elements.states.states import EvaluationState

def evaluation_edge(state: EvaluationState) -> Send:

    return [Send("get_intent_node", {"evaluation": i}) for i in state["evaluations"]]