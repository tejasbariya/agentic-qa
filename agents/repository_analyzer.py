from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from workflows.state import QAState
from agents.base import create_agent

SYSTEM_PROMPT = """You are the Repository Analyzer agent of SentinelQA.
Your job is to read the codebase structure and identify:
- Languages used (Python, JS, etc.)
- Frameworks (Django, React, FastAPI, etc.)
- Database technologies
- Package managers (npm, pip, poetry, etc.)
- Testing frameworks (pytest, jest, etc.)

Analyze the repository and output the detected technologies as a structured JSON.
"""

def analyze_repository_node(state: QAState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_agent(llm, [], SYSTEM_PROMPT)
    
    messages = state.get("messages", [])
    response = agent.invoke({"messages": messages})
    
    # In a real setup, we'd parse this properly and assign it.
    detected_tech = {"language": "python", "framework": "fastapi"} 
    
    return {
        "detected_tech": detected_tech,
        "current_step": "planning"
    }
