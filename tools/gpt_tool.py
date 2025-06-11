# tools/gpt_tool.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_EXTRACT_PROMPT = "You are a document parser. Extract all text, images, tables, and structural elements."

SYSTEM_APPLY_PROMPT = "You are an AI assistant. Given a document structure, fulfill the user's prompt."


def extract_elements_with_gpt(pdf_path):
    with open(pdf_path, "rb") as f:
        content = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_EXTRACT_PROMPT},
            # partial content or convert to text
            {"role": "user",
                "content": f"Extract this PDF:\n{content[:1000]}..."}
        ]
    )
    return response.choices[0].message.content


def apply_user_prompt(prompt, extracted_content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_APPLY_PROMPT},
            {"role": "user", "content": f"Prompt: {prompt}\nContent: {extracted_content}"}
        ]
    )
    return response.choices[0].message.content

# This module provides functions to interact with the GPT API for document extraction and user prompt application.

def call_gpt_tool(pdf_path, user_prompt):
    extracted_content = extract_elements_with_gpt(pdf_path)
    applied_content = apply_user_prompt(user_prompt, extracted_content)
    return applied_content


def extract_from_doc(pdf_path):
    # Mock GPT extraction result
    return {
        "text": "This is a mock GPT-extracted text.",
        "tables": [],
        "images": [],
        "structure": {"sections": ["Introduction", "Summary"]}
    }
