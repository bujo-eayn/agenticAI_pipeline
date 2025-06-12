# agentic-doc-intel/app.py
import streamlit as st
import io
import sys
import traceback
import os

from graph.graph_builder import build_graph
from tools.storage import save_uploaded_file
from utils.logger import setup_logger, LOG_FILE_PATH


def main():
    st.set_page_config(page_title="2Sage - Agentic AI DocIntel", layout="wide")
    st.title("📄2Sage📄")
    st.write("Upload a document and provide a prompt to begin the analysis pipeline.")

    st.sidebar.header("⚙️ Settings")
    debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=False)

    # 🧹 Add Clear Logs Button
    if st.sidebar.button("🧹 Clear Logs"):
        try:
            if os.path.exists(LOG_FILE_PATH):
                with open(LOG_FILE_PATH, "w"):
                    pass  # Truncate file
                st.sidebar.success("✅ Logs cleared.")
            else:
                st.sidebar.info("ℹ️ No logs to clear.")
        except Exception as e:
            st.sidebar.error(f"Error clearing logs: {e}")

    # Re-initialize logger with debug setting
    logger = setup_logger(debug_mode=debug_mode)

    uploaded_file = st.file_uploader(
        "Choose a document", type=["pdf", "docx", "txt"])
    user_prompt = st.text_area("Your prompt for the AI:")

    if st.button("Run Pipeline") and uploaded_file and user_prompt:
        save_path = save_uploaded_file(uploaded_file)
        st.success(f"File saved to {save_path}")
        logger.info(f"User uploaded file: {save_path}")

        state = {
            "file_path": save_path,
            "user_prompt": user_prompt,
            "retry_attempts": 0,
        }

        # Capture printed output
        log_output = io.StringIO()
        if debug_mode:
            sys.stdout = log_output
            sys.stderr = log_output

        try:
            logger.info("Building graph and starting pipeline.")
            graph = build_graph()
            with st.spinner("Running agentic pipeline..."):
                result = graph.invoke(state)

            st.subheader("📝 Final Output")
            st.text_area("Output", result.get(
                "final_doc", "No output generated."), height=300)

            if "final_document_path" in result:
                with open(result["final_document_path"], "rb") as f:
                    st.download_button(
                        "Download Final Document", f, file_name="final_output.docx")

        except Exception as e:
            logger.error("Pipeline failed with an exception.")
            logger.exception(e)
            if debug_mode:
                st.error("🚨 An error occurred. See debug logs below.")
                st.code(traceback.format_exc())
            else:
                st.error("⚠️ Something went wrong while processing your document.")

        finally:
            # Restore stdout/stderr
            if debug_mode:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

                st.subheader("🐛 Debug Logs (Session)")
                st.code(log_output.getvalue())

                # Also show persistent log file
                if os.path.exists(LOG_FILE_PATH):
                    st.subheader("🗂 Persistent Log File")
                    with open(LOG_FILE_PATH, "r") as f:
                        log_contents = f.read()
                    st.text_area("Log File", log_contents, height=300)


if __name__ == "__main__":
    main()
