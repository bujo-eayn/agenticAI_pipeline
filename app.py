# agenticai_pipeline/app.py

from openai import OpenAI
import streamlit as st
import io
import sys
import traceback
import os
from IPython.display import Image, display

from graph.graph_builder import build_graph
from tools.storage import save_uploaded_file
from utils.logger import setup_logger, LOG_FILE_PATH, log_exception
from langchain_core.runnables import RunnableConfig

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in environment.")

client = OpenAI(api_key=OPENAI_API_KEY)


def main():
    st.set_page_config(page_title="📄DocSage📄", layout="wide")
    st.title("📄DocSage📄")
    st.write(
        "Upload a document and/or provide a prompt to begin the analysis pipeline.")

    st.sidebar.header("⚙️ Settings")
    debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=False)

    if st.sidebar.button("🧹 Clear Logs"):
        try:
            if os.path.exists(LOG_FILE_PATH):
                with open(LOG_FILE_PATH, "w"):
                    pass
                st.sidebar.success("✅ Logs cleared.")
            else:
                st.sidebar.info("ℹ️ No logs to clear.")
        except Exception as e:
            st.sidebar.error(f"Error clearing logs: {e}")

    logger = setup_logger(debug_mode=debug_mode)

    uploaded_file = st.file_uploader(
        "Choose a document", type=["pdf", "docx", "txt", "md", "doc", "csv", "xlsx", "png", "jpeg"],)
    user_prompt = st.text_area("Your prompt for the AI:")


    if st.button("Run Pipeline") and (uploaded_file or user_prompt):
        save_path = None
        if uploaded_file:
            save_path = save_uploaded_file(uploaded_file)
            st.success(f"File saved to {save_path}")
            logger.info(f"User uploaded file: {save_path}")

        input_type = ["file_or_both"] if uploaded_file else ["prompt_only"]

        state = {
            "file_path": [save_path] if save_path else [],
            "user_prompt": [user_prompt] if user_prompt else [],
            "retry_attempts": [0],
            "input_type": input_type,
        }

        log_output = io.StringIO()
        if debug_mode:
            sys.stdout = log_output
            sys.stderr = log_output

        try:
            logger.info("Building graph and starting pipeline.")
            graph = build_graph() # Carry on Evaluation from here
            display(Image(graph.get_graph().draw_mermaid_png()))
            config = RunnableConfig(recursion_limit=500)
            with st.spinner("Running agentic pipeline..."):
                result = graph.invoke(state, config=config)

                # Should contain tool calls if any
                print(result.get("intermediate_steps", "chat_history"))


                # show status updates
                st.subheader("📊 Pipeline Status")
                for update in result.get("status_updates", []):
                    st.markdown(f"- {update}")

            st.subheader("📝 Final Output")
            st.text_area("Output", result.get(
                "final_output_text", "No output generated."), height=300)

            if "final_doc" in result:
                with open(result["final_doc"], "rb") as f:
                    st.download_button(
                        "Download Final Document", f, file_name="final_output.docx")

        except Exception as e:
            logger.error("Pipeline failed with an exception.")
            log_exception(e)
            if debug_mode:
                st.error("🚨 An error occurred. See debug logs below.")
                st.code(traceback.format_exc())
            else:
                st.error("⚠️ Something went wrong while processing your document.")

        finally:
            if debug_mode:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                st.subheader("🐛 Debug Logs (Session)")
                st.code(log_output.getvalue())

                if os.path.exists(LOG_FILE_PATH):
                    st.subheader("🗂 Persistent Log File")
                    with open(LOG_FILE_PATH, "r") as f:
                        log_contents = f.read()
                    st.text_area("Log File", log_contents, height=300)


if __name__ == "__main__":
    main()
