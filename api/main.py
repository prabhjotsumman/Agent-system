from fastapi import FastAPI
from langgraph.graph import StateGraph

app = FastAPI()

class State(dict):
    pass

def planner(state):
    state["plan"] = f"Plan for: {state['idea']}"
    return state

def coder(state):
    state["code"] = "print('Hello iOS app')"
    return state

graph = StateGraph(State)
graph.add_node("planner", planner)
graph.add_node("coder", coder)

graph.set_entry_point("planner")
graph.add_edge("planner", "coder")

app_graph = graph.compile()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/run")
def run(idea: str):
    return app_graph.invoke({"idea": idea})
