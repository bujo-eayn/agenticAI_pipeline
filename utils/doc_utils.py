# utils/doc_utils.py
from docx import Document
from fpdf import FPDF
import os
from pathlib import Path


def convert_to_pdf(file_path):
    # Dummy placeholder: assume PDF is already uploaded
    if file_path.endswith(".pdf"):
        return file_path
    pdf_path = file_path + ".converted.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n...mock content...")
    return pdf_path


def create_final_doc(extracted_data, source_pdf_path):
    doc = Document()
    doc.add_heading("Final Extracted Document", 0)
    doc.add_paragraph(str(extracted_data))

    # Determine directory for final output
    if source_pdf_path:
        base_path = Path(source_pdf_path).parent
        if not base_path.exists():
            base_path = Path("outputs")
    else:
        base_path = Path("outputs")

    # Create the directory if it does not exist
    os.makedirs(base_path, exist_ok=True)

    # Set final file name inside the chosen directory
    final_path = base_path / \
        (Path(source_pdf_path).stem if source_pdf_path else "final_output")
    final_path = final_path.with_suffix(".final.docx")

    # Save document
    doc.save(final_path)

    return str(final_path)



def create_text_doc(content: str, file_name="output.txt"):
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# This module provides utility functions for document processing.
# It includes converting documents to PDF and creating a final document from extracted data.