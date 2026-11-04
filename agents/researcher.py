from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()

# ---------------- STATE ----------------
class ResearchState(TypedDict):
    topic: str
    research: str

# ---------------- LLM ----------------
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# ---------------- NODE ----------------
def research_topic(state: ResearchState):
    prompt = f"""
    You are an AI research assistant.

    Research topic:
    {state['topic']}

    Provide a structured research overview containing:

    1. Introduction
    2. Key Concepts
    3. Important Applications
    4. Benefits
    5. Challenges
    6. Conclusion

    Requirements:
    - Use clear and simple language.
    - Keep the response under 700 words.
    - Do not invent statistics.
    - Do not fabricate citations or sources.
    - If information is uncertain, clearly mention it.
    """

    response = llm.invoke(prompt)
    return {"research":response.content}

# ---------------- GRAPH ----------------
graph = StateGraph(ResearchState)

graph.add_node("research", research_topic)

graph.add_edge(START, "research")
graph.add_edge("research", END)

research_app = graph.compile()

# ---------------- FUNCTION ----------------
def run_research(topic: str):
    result = research_app.invoke({
        "topic":topic,
        "research":""
    })
    return result['research']