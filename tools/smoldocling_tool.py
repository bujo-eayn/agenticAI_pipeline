# tools/smoldocling_tool.py
import requests

SMOLDOCLING_URL = "http://localhost:5001/api/extract"

STATIC_PROMPT = "Convert this page to docling."


# def call_smoldocling(pdf_path):
#     files = {"file": open(pdf_path, "rb")}
#     data = {"prompt": STATIC_PROMPT}
#     response = requests.post(SMOLDOCLING_URL, files=files, data=data)
#     return response.json()
# This function calls the SmolDocling API to extract information from a PDF file.
# It sends the PDF file along with a static prompt and returns the JSON response.


# def call_smoldocling_with_feedback(pdf_path, feedback):
#     files = {"file": open(pdf_path, "rb")}
#     data = {
#         "prompt": f"{STATIC_PROMPT} Please improve the extraction on: {feedback}"
#     }
#     response = requests.post(SMOLDOCLING_URL, files=files, data=data)
#     return response.json()
# This function calls the SmolDocling API to extract information from a PDF file.
# It sends the PDF file along with a static prompt and returns the JSON response.

def call_smoldocling_with_custom_prompt(pdf_path, custom_prompt):
    files = {"file": open(pdf_path, "rb")}
    data = {"prompt": custom_prompt}
    response = requests.post(SMOLDOCLING_URL, files=files, data=data)
    return response.json()
# This function allows the user to provide a custom prompt for the SmolDocling extraction.
# It sends the PDF file and the custom prompt to the SmolDocling API and returns the response.


def call_smoldocling(pdf_path):
    return {
        "text": "This is a mock SmolDocling-extracted text.",
        "tables": [],
        "images": [],
        "structure": {"sections": ["Introduction", "Summary"]}
    }


def call_smoldocling_with_feedback(pdf_path, feedback):
    return {
        "text": "Improved mock text from SmolDocling.",
        "tables": [],
        "images": [],
        "structure": {"sections": ["Introduction", "Summary", "Conclusion"]}
    }
