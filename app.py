
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile

from agents.analyst import analyze_csv, create_chart
from agents.rag import create_vector_store
from graph.workflow import run_workflow


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="ResearchFlow AI",
    page_icon="🔬",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("ResearchFlow AI")

st.caption(
    "AI-powered Research, Data Analysis & Document Intelligence"
)


# =========================
# NAVIGATION
# =========================

st.sidebar.title("Navigation")

page_options = [
    "Home",
    "Research Assistant",
    "Data Analyst",
    "PDF Question Answering",
    "Reports"
]


if "page_radio" not in st.session_state:
    st.session_state["page_radio"] = "Home"


def navigate_to(page):
    st.session_state["page_radio"] = page


page = st.sidebar.radio(
    "Choose a Task",
    page_options,
    key="page_radio"
)


# =========================
# HOME DASHBOARD
# =========================

if page == "Home":

    st.header("Welcome to ResearchFlow AI")

    st.write(
        "Your intelligent workspace for research, "
        "data analysis, document understanding, "
        "and automated report generation."
    )

    st.divider()

    # Project statistics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("AI Agents", "4")

    with col2:
        st.metric("Research", "Available")

    with col3:
        st.metric("Data Analysis", "Available")

    with col4:
        st.metric("PDF Intelligence", "Available")

    st.divider()

    st.subheader("Explore Features")

    col1, col2 = st.columns(2)

    # Research Assistant

    with col1:

        st.markdown("### Research Assistant")

        st.write(
            "Generate AI-powered research "
            "on different topics."
        )

        st.button(
            "Open Research",
            key="home_research",
            on_click=navigate_to,
            args=("Research Assistant",)
        )

        # Data Analyst

        st.markdown("### Data Analyst")

        st.write(
            "Explore datasets, analyze statistics, "
            "and generate charts."
        )

        st.button(
            "Open Data Analyst",
            key="home_analyst",
            on_click=navigate_to,
            args=("Data Analyst",)
        )

    # PDF and Reports

    with col2:

        st.markdown("### PDF Question Answering")

        st.write(
            "Ask questions about documents "
            "and retrieve relevant information."
        )

        st.button(
            "Open PDF AI",
            key="home_pdf",
            on_click=navigate_to,
            args=("PDF Question Answering",)
        )

        # Report Generator

        st.markdown("### Report Generator")

        st.write(
            "Generate downloadable reports "
            "using research and dataset analysis."
        )

        st.button(
            "Open Reports",
            key="home_reports",
            on_click=navigate_to,
            args=("Reports",)
        )


# =========================
# RESEARCH ASSISTANT
# =========================

elif page == "Research Assistant":

    st.header("Research Assistant")

    topic = st.text_input(
        "Enter Research Topic"
    )

    if st.button("Start Research"):

        if topic.strip():

            try:

                with st.spinner("Researching..."):

                    result = run_workflow({
                        "task": "research",
                        "topic": topic
                    })

                    st.session_state["research_result"] = (
                        result["research"]
                    )

                    st.session_state["research_topic"] = topic

                st.success("Research completed!")

            except Exception as e:

                st.error(
                    f"Research failed: {e}"
                )

        else:

            st.warning(
                "Please enter a research topic."
            )

    if "research_result" in st.session_state:

        st.subheader(
            st.session_state["research_topic"]
        )

        st.markdown(
            st.session_state["research_result"]
        )

        st.download_button(
            label="Download Research",
            data=st.session_state["research_result"],
            file_name="research_report.md",
            mime="text/markdown"
        )


# =========================
# DATA ANALYST
# =========================

elif page == "Data Analyst":

    st.header("Data Analyst Agent")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df, analysis = analyze_csv(uploaded_file)

            if df.empty:

                st.warning(
                    "The CSV file contains no records."
                )

            else:

                # Store dataset summary

                st.session_state["data_analysis"] = (
                    df.describe(include="all")
                    .fillna("")
                    .to_string()
                )

                st.success(
                    "Dataset loaded successfully!"
                )

                # Dataset metrics

                col1, col2 = st.columns(2)

                col1.metric(
                    "Rows",
                    analysis["rows"]
                )

                col2.metric(
                    "Columns",
                    analysis["columns"]
                )

                # Dataset preview

                st.subheader("Dataset Preview")

                st.dataframe(
                    df.head(10),
                    use_container_width=True
                )

                # Column information

                st.subheader("Column Information")

                info_df = pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str).values,
                    "Missing Values": df.isnull().sum().values
                })

                st.dataframe(
                    info_df,
                    use_container_width=True
                )

                # Summary statistics

                st.subheader("Summary Statistics")

                st.dataframe(
                    df.describe(include="all").fillna(""),
                    use_container_width=True
                )

                # Ask dataset

                st.subheader("Ask Your Dataset")

                question = st.text_input(
                    "Enter your question",
                    key="csv_question"
                )

                if st.button("Analyze Question"):

                    if question.strip():

                        try:

                            with st.spinner(
                                "Analyzing dataset..."
                            ):

                                result = run_workflow({
                                    "task": "analyst",
                                    "df": df,
                                    "question": question
                                })

                            st.markdown("### Answer")

                            st.write(
                                result["answer"]
                            )

                        except Exception as e:

                            st.error(
                                f"Data analysis failed: {e}"
                            )

                    else:

                        st.warning(
                            "Please enter a question."
                        )

                # Generate chart

                st.subheader("Generate Chart")

                column = st.selectbox(
                    "Select a column",
                    df.columns
                )

                if st.button("Generate Chart"):

                    try:

                        fig = create_chart(
                            df,
                            column
                        )

                        if fig is not None:

                            st.pyplot(fig)

                            plt.close(fig)

                        else:

                            st.warning(
                                "Unable to generate chart."
                            )

                    except Exception as e:

                        st.error(
                            f"Chart generation failed: {e}"
                        )

        except Exception as e:

            st.error(
                f"CSV processing failed: {e}"
            )


# =========================
# PDF QUESTION ANSWERING
# =========================

elif page == "PDF Question Answering":

    st.header("PDF Question Answering Agent")

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:

        if st.button("Process PDF"):

            try:

                with st.spinner("Processing PDF..."):

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            uploaded_pdf.getvalue()
                        )

                        pdf_path = temp_file.name

                    vector_store = create_vector_store(
                        pdf_path
                    )

                    st.session_state["vector_store"] = (
                        vector_store
                    )

                st.success(
                    "PDF processed successfully!"
                )

            except Exception as e:

                st.error(
                    f"PDF processing failed: {e}"
                )

    if "vector_store" in st.session_state:

        st.subheader("Ask Questions")

        question = st.text_input(
            "Ask a question about your PDF",
            key="pdf_question"
        )

        if st.button("Ask PDF"):

            if question.strip():

                try:

                    with st.spinner("Finding answer..."):

                        result = run_workflow({
                            "task": "pdf",
                            "vector_store": st.session_state[
                                "vector_store"
                            ],
                            "question": question
                        })

                    # Answer

                    st.markdown("### Answer")

                    st.write(
                        result["answer"]
                    )

                    # Sources

                    st.markdown("### PDF Sources")

                    for source in result.get(
                        "sources", []
                    ):

                        with st.expander(
                            f"Page {source['page']}"
                        ):

                            st.write(
                                source["content"]
                            )

                except Exception as e:

                    st.error(
                        f"PDF question failed: {e}"
                    )

            else:

                st.warning(
                    "Please enter a question."
                )


# =========================
# REPORT GENERATOR
# =========================

elif page == "Reports":

    st.header("Report Generator")

    topic = st.text_input(
        "Enter Report Topic"
    )

    if st.button("Generate Report"):

        if topic.strip():

            research = st.session_state.get(
                "research_result",
                ""
            )

            data_analysis = st.session_state.get(
                "data_analysis",
                ""
            )

            if not research and not data_analysis:

                st.warning(
                    "Generate research or upload a CSV "
                    "before creating a report."
                )

            else:

                try:

                    with st.spinner("Generating report..."):

                        result = run_workflow({
                            "task": "report",
                            "topic": topic,
                            "research": research,
                            "data_analysis": data_analysis
                        })

                        st.session_state[
                            "generated_report"
                        ] = result["report"]

                        st.session_state[
                            "generated_report_topic"
                        ] = topic

                    st.success(
                        "Report generated successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Report generation failed: {e}"
                    )

        else:

            st.warning(
                "Please enter a report topic."
            )

    # Display generated report

    if "generated_report" in st.session_state:

        st.subheader(
            st.session_state.get(
                "generated_report_topic",
                "Generated Report"
            )
        )

        st.markdown(
            st.session_state["generated_report"]
        )

        st.download_button(
            label="Download Report",
            data=st.session_state["generated_report"],
            file_name="researchflow_report.md",
            mime="text/markdown"
        )
