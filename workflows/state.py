from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class QAState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    repository_path: str
    detected_tech: Dict[str, Any]
    test_plan: List[Dict[str, Any]]
    execution_results: List[Dict[str, Any]]
    current_step: str
    errors: List[str]
