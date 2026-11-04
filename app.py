import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ResearchFlow AI",
    page_icon="🔬",
    layout="wide"
)

st.title("ResearchFlow AI")
st.caption("AI-powered Research, Data Analysis & Document Intelligence")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a Task",
    [
        "Home",
        "Research Assistant",
        "Data Analyst",
        "PDF Questioning Answering",
        "Reports"
    ]
)

if page == "Home":
    st.header("Welcome to ResearchFlow AI")
    st.write(
        "An AI-powered platform combining research, "
        "data analysis, document intelligence, "
        "and automated report generation."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Research")
        st.write("Research topics using AI Agents")

    with col2:
        st.subheader("Data Analysis")
        st.write("Analyze CSV Datasets")

    with col3:
        st.subheader("Document AI")
        st.write("Ask questions about PDF Documents")

elif page == "Research Assistant":
    st.header("Research Assistant")

    topic = st.text_input("Enter Research Topic: ")

    if st.button("Start Research"):
        st.info("Research Agent will be connected in the next step.")
    else:
        st.warning("Please enter a research topic.")

elif page == "Data Analyst":
    st.header("AI Data Analyst")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file:
        import pandas as pd

        df = pd.read_csv(uploaded_file)
        
        st.subheader("Dataset Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("Dataset Information")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

elif page == "PDF Questioning Answering":
    st.header("PDF Questioning Answering")

    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        question = st.text_input("Ask a question about document: ")

        if st.button("Ask Question"):
            if question.strip():
                st.info("RAG Agent will be connected in a later step")
            else:
                st.warning("Please enter a question")

elif page == "Reports":
    st.header("Generated Reports")

    st.write(
        "Your research and analysis reports "
        "will appear here."
    )