# tools/smoldocling_tool.py
import requests

SMOLDOCLING_URL = "http://localhost:40000/docling"
STATIC_PROMPT = "Convert this page to docling."


def call_smoldocling(file_path):
    files = {"file": open(file_path, "rb")}
    data = {"prompt": STATIC_PROMPT}
    response = requests.post(SMOLDOCLING_URL, files=files, data=data)
    return response.json()

# This function calls the SmolDocling API to extract information from a PDF file.
# It sends the PDF file along with a static prompt and returns the JSON response.


def call_smoldocling_with_feedback(file_path, feedback):
    files = {"file": open(file_path, "rb")}
    data = {
        "prompt": f"{STATIC_PROMPT} Please improve the extraction on: {feedback}"
    }
    response = requests.post(SMOLDOCLING_URL, files=files, data=data)
    return response.json()

