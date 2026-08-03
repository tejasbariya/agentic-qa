from langgraph.graph import StateGraph, END
from workflows.state import QAState
from agents.repository_analyzer import analyze_repository_node
from agents.test_planner import plan_tests_node

def create_qa_workflow():
    workflow = StateGraph(QAState)
    
    workflow.add_node("analyze_repo", analyze_repository_node)
    workflow.add_node("plan_tests", plan_tests_node)
    
    def execute_tests_node(state: QAState):
        return {"current_step": "completed"}
        
    workflow.add_node("execute_tests", execute_tests_node)
    
    workflow.set_entry_point("analyze_repo")
    
    workflow.add_edge("analyze_repo", "plan_tests")
    workflow.add_edge("plan_tests", "execute_tests")
    workflow.add_edge("execute_tests", END)
    
    return workflow.compile()
