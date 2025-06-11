# agentic-doc-intel/app.py
# Entry point to launch the LangGraph app with Streamlit UI and real SmolDocling backend

# import os

import streamlit as st

from graph.graph_builder import build_graph
from tools.storage import save_uploaded_file
from utils.logger import setup_logger

logger = setup_logger()


def main():
    st.set_page_config(page_title="Agentic AI DocIntel", layout="wide")
    st.title("Agentic AI Document Intelligence")
    st.write("Upload a document and a prompt to begin the analysis pipeline.")

    uploaded_file = st.file_uploader(
        "Choose a document", type=["pdf", "docx", "txt"])
    user_prompt = st.text_area("Your prompt for the AI:")

    if st.button("Run Pipeline") and uploaded_file and user_prompt:
        save_path = save_uploaded_file(uploaded_file)
        st.success(f"File saved to {save_path}")

        # Build and invoke the graph
        graph = build_graph()
        state = {
            "file_path": save_path,
            "user_prompt": user_prompt,
        }

        with st.spinner("Running agentic pipeline..."):
            result = graph.invoke(state)

        st.subheader("Final Output")
        st.text_area("Output", result.get("final_output"), height=300)

        if "final_document_path" in result:
            st.download_button(
                label="Download Final Document",
                data=open(result["final_document_path"], "rb"),
                file_name="final_output.docx",
            )


if __name__ == "__main__":
    main()

# This is the main entry point for the Agentic AI Document Intelligence application.
# It sets up the Streamlit UI, handles file uploads, and runs the LangGraph pipeline.