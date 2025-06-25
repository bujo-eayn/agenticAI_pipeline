# tools/gpt_tool.py
from openai import OpenAI
import os

# import magic
import chardet
import fitz  # PyMuPDF
import docx
import mimetypes
import pandas as pd

from utils.logger import log_exception, logger

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_EXTRACT_PROMPT = "You are a document parser. Extract all text, images, tables, and structural elements with layout preserved."
SYSTEM_APPLY_PROMPT = "You are a document summarizer. Apply the user's prompt to the extracted content and return a structured summary."
CHUNK_SIZE_TOKENS = 3000  # Leave headroom for system/user prompt and GPT response


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(10000)
    result = chardet.detect(raw_data)
    logger.info(f"Detected encoding for {file_path}: {result.get('encoding', 'utf-8')}")
    return result.get("encoding", "utf-8")


def extract_metadata(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    size = os.path.getsize(file_path)
    logger.info(f"Extracted metadata for {file_path}: mime_type={mime_type}, size={size} bytes")
    return {
        "file_name": os.path.basename(file_path),
        "mime_type": mime_type or "unknown",
        "file_size_bytes": size
    }


def extract_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".pdf"]:
        logger.info(f"Extracting content from PDF: {file_path}")
        return extract_from_pdf(file_path)
    elif ext in [".docx"]:
        return extract_from_docx(file_path)
    elif ext in [".csv", ".xlsx"]:
        return extract_from_table(file_path)
    elif ext in [".txt"]:
        encoding = detect_encoding(file_path)
        with open(file_path, "r", encoding=encoding, errors="ignore") as f:
            return [{"type": "Text", "content": f.read()}]
    else:
        return [{"type": "Text", "content": "[Unsupported file format for structured parsing]"}]


def extract_from_pdf(file_path):
    doc = fitz.open(file_path)
    content = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                text = "\n".join(
                    [" ".join([span["text"] for span in line["spans"]]) for line in block["lines"]])
                content.append(
                    {"type": "Text", "content": text, "page": page_num})
                logger.info(f"Extracted text from page {page_num}: {text[:100]}...")  # Log first 100 chars
            elif "image" in block:
                content.append({"type": "Image", "page": page_num})
                logger.info(f"Found image on page {page_num}")
    return content


def extract_from_docx(file_path):
    doc = docx.Document(file_path)
    content = []
    for para in doc.paragraphs:
        if para.text.strip():
            content.append({"type": "Text", "content": para.text})
    return content


def extract_from_table(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        return []
    return [{"type": "Table", "content": df.to_markdown()}]


def chunk_content(content_list, max_tokens=CHUNK_SIZE_TOKENS):
    chunks = []
    current_chunk = []
    current_length = 0

    for item in content_list:
        text = str(item)
        token_estimate = len(text) // 4  # Rough estimate

        if current_length + token_estimate > max_tokens:
            chunks.append(current_chunk)
            current_chunk = []
            current_length = 0

        current_chunk.append(item)
        current_length += token_estimate
        logger.info(f"Added item to chunk: {item.get('type')} (length: {token_estimate} tokens)")

    if current_chunk:
        chunks.append(current_chunk)
    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks


def extract_elements_with_gpt(file_path):
    logger.info(f"Starting extraction for file: {file_path}")
    try:
        metadata = extract_metadata(file_path)
        content_blocks = extract_content(file_path)
        content_chunks = chunk_content(content_blocks)

        cumulative_output = []
        for i, chunk in enumerate(content_chunks):
            chunk_str = "\n\n".join(
                [f"{item.get('type')}: {item.get('content')}" for item in chunk])

            messages = [
                {"role": "system", "content": SYSTEM_EXTRACT_PROMPT},
                {"role": "user",
                    "content": f"Chunk {i + 1}/{len(content_chunks)} of document '{metadata['file_name']}':\n\n{chunk_str}"}
            ]

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.3,
                max_tokens=1500
            )
            parsed_output = response.choices[0].message.content.strip()
            cumulative_output.append(parsed_output)

        return {
            "metadata": metadata,
            "structured_output": "\n\n".join(cumulative_output)
        }

    except Exception as e:
        log_exception(e)
        return {"error": str(e)}



def apply_user_prompt(prompt, extracted_content):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_APPLY_PROMPT},
            {"role": "user", "content": f"Prompt: {prompt}\n\nDocument:\n{extracted_content}"}
        ],
        temperature=0.5,
        max_tokens=1500
    )

    return response.choices[0].message.content.strip()


def call_gpt_tool(file_path, user_prompt):
    extracted_content = extract_elements_with_gpt(file_path)
    applied_content = apply_user_prompt(user_prompt, extracted_content)
    return applied_content
