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

    final_path = str(Path(source_pdf_path).with_suffix(".final.docx"))
    doc.save(final_path)
    return final_path

# This module provides utility functions for document processing.
# It includes converting documents to PDF and creating a final document from extracted data.