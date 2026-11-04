from dotenv import load_dotenv
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

def generate_report(topic, research, data_analysis=""):
    prompt = f"""
    You are an AI report generation assistant.

    Create a professional report using the information below.

    Topic:
    {topic}

    Research:
    {research}

    Data Analysis:
    {data_analysis}

    Report structure:
    1. Title
    2. Executive Summary
    3. Introduction
    4. Key Findings
    5. Analysis
    6. Conclusion

    Requirements:
    - Use clear professional language.
    - Do not invent facts or statistics.
    - Use only the provided information.
    - Mention when information is unavailable.
    - Format the report using Markdown.
    """

    response = llm.invoke(prompt)
    return response.content