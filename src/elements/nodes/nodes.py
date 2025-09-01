from src.elements.states.states import EvaluationState

def get_intent_node(state: EvaluationState) -> EvaluationState:
    if state["evaluation"].history_qa:
        history_qa = state["evaluation"].history_qa.split("||||||")
    return state