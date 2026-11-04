import streamlit as st
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import tempfile

from agents.researcher import run_research
from agents.analyst import analyze_csv, answer_question, create_chart
from agents.rag import create_vector_store, ask_pdf
from agents.report import generate_report

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
        "PDF Question Answering",
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
        if topic.strip():
            try:
                with st.spinner("Researching...."):
                    result = run_research(topic)

                    st.session_state["research_result"] = result
                    st.session_state["research_topic"] = topic

                    st.success("Research Completed")
            except Exception as e:
                st.error(f"Research failed")
        else:
            st.warning("Please enter a research topic")
    
    if "research_result" in st.session_state:
        st.subheader(f"Research: {st.session_state['research_topic']}")
        st.markdown(st.session_state["research_result"])

        st.download_button(
            label="Download Research",
            data=st.session_state["research_result"],
            file_name="research_report.md",
            mime="text/markdown"
        )

elif page == "Data Analyst":
    st.title("📊 Data Analyst Agent")
    st.write("Upload a CSV file to automatically analyze your dataset.")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df, analysis = analyze_csv(uploaded_file)

            st.success("Dataset loaded successfully!")

            col1, col2 = st.columns(2)

            col1.metric("Rows", analysis["rows"])
            col2.metric("Columns", analysis["columns"])

            st.subheader("Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)

            st.subheader("Column Information")

            info_df = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Missing Values": df.isnull().sum().values
            })

            st.dataframe(info_df, use_container_width=True)

            st.subheader("Summary Statistics")
            st.dataframe(
                df.describe(include="all").fillna(""),
                use_container_width=True
            )

            st.subheader("Ask Your Dataset")

            question = st.text_input(
                "Ask a question",
                placeholder="Example: What is the average sales?"
            )

            if st.button("Analyze Question"):
                if question.strip():
                    answer = answer_question(df, question)
                    st.write(answer)
                else:
                    st.warning("Please enter a question.")

            st.subheader("Generate Chart")

            column = st.selectbox(
                "Select a column",
                df.columns
            )

            if st.button("Generate Chart"):
                fig = create_chart(df, column)

                if fig is not None:
                    st.pyplot(fig)
                    plt.close(fig)

        except Exception as e:
            st.error(f"Error analyzing CSV: {e}")



elif page == "PDF Question Answering":
    st.title("📄 PDF Question Answering Agent")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf is not None:
        if st.button("Process PDF"):
            try:
                with st.spinner("Processing PDF..."):

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(uploaded_pdf.getvalue())
                        pdf_path = temp_file.name

                    vector_store = create_vector_store(pdf_path)

                    st.session_state["vector_store"] = vector_store
                    st.success("PDF processed successfully!")

            except Exception as e:
                st.error(f"Error processing PDF: {e}")

    if "vector_store" in st.session_state:

        st.subheader("Ask Questions")

        question = st.text_input("Enter your question about the PDF")

        if st.button("Ask PDF"):
            if question.strip():
                try:
                    with st.spinner("Finding answer..."):

                        answer = ask_pdf(st.session_state["vector_store"],question)

                    st.markdown("### Answer")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error answering question: {e}")

            else:
                st.warning("Please enter a question.")


elif page == "Reports":
    st.header("Report Generator")

    topic = st.text_input("Report Topic")

    research = st.session_state.get(
        "research_result", ""
    )

    if research:
        st.success("Research results available")

    if st.button("Generate Report"):

        if topic.strip():

            try:
                with st.spinner("Generating report..."):

                    report = generate_report(
                        topic,
                        research
                    )

                    st.session_state["generated_report"] = report

                st.success("Report generated!")

            except Exception as e:
                st.error(f"Report generation failed: {e}")

        else:
            st.warning("Enter a report topic.")

    if "generated_report" in st.session_state:

        st.subheader("Generated Report")

        st.markdown(
            st.session_state["generated_report"]
        )

        st.download_button(
            "Download Report",
            data=st.session_state["generated_report"],
            file_name="researchflow_report.md",
            mime="text/markdown"
        )
