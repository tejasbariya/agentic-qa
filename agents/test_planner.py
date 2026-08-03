from langchain_openai import ChatOpenAI
from workflows.state import QAState
from agents.base import create_agent

SYSTEM_PROMPT = """You are the Test Planner agent of SentinelQA.
Based on the detected technologies, you will formulate a complete test execution plan.
You decide:
- Which test suites to run
- Execution order (e.g., run unit tests before integration tests)
- Parallel execution strategy

Output a list of steps representing the test plan.
"""

def plan_tests_node(state: QAState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_agent(llm, [], SYSTEM_PROMPT)
    
    messages = state.get("messages", [])
    response = agent.invoke({"messages": messages})
    
    # Mocked output for the test plan
    test_plan = [
        {"id": "unit", "command": "pytest tests/unit", "type": "unit"},
        {"id": "api", "command": "pytest tests/api", "type": "api"}
    ]
    
    return {
        "test_plan": test_plan,
        "current_step": "executing"
    }
