from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END

from agents.researcher import run_research
from agents.analyst import answer_question
from agents.rag import ask_pdf
from agents.report import generate_report

class WorkFlowState(TypedDict, total=False):
    task: str
    topic: str
    research: str
    df: Any
    question: str
    vector_store: Any
    data_analysis: str
    answer: str
    report: str
    sources: list

def research_node(state: WorkFlowState):
    result = run_research(state['topic'])
    return {"research":result, "answer":result}

def analyst_node(state: WorkFlowState):
    df = state["df"]

    result = answer_question(df, state["question"])
    return {"answer":result}

def pdf_node(state: WorkFlowState):
    result = ask_pdf(state["vector_store"], state["question"])
    return {"answer":result["answer"], "sources":result["sources"]}

def report_node(state: WorkFlowState):
    report = generate_report(state["topic"], state.get("research", ""), state.get("data_analysis", ""))
    return {"report":report}

def route_task(state: WorkFlowState):
    return state["task"]

workflow = StateGraph(WorkFlowState)

workflow.add_node("research", research_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("pdf", pdf_node)
workflow.add_node("report", report_node)

workflow.add_conditional_edges(
    START,
    route_task,
    {
        "research":"research",
        "analyst":"analyst",
        "pdf":"pdf",
        "report":"report"                
    }
)

workflow.add_edge("research", END)
workflow.add_edge("analyst", END)
workflow.add_edge("pdf", END)
workflow.add_edge("report", END)

researchflow_app = workflow.compile()

def run_workflow(inputs):
    return researchflow_app.invoke(inputs)