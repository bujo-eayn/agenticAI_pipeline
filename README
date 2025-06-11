# Agentic Document Intelligence with GPT-4 & SmolDocling

This project is an agentic AI pipeline that uses GPT-4 as the primary agent and integrates SmolDocling as a tool to deeply analyze uploaded documents. It allows users to upload various document formats and extract structured content automatically, with an intelligent evaluation and feedback loop.

---

## 🚀 Features

* Upload documents in multiple formats (PDF, Word, etc.)
* Automatic conversion to PDF if needed
* Dual extraction using GPT-4 and SmolDocling
* Evaluation of extracted content using BLEU, overlap, and Jaccard similarity
* Iterative feedback to SmolDocling to improve accuracy
* Final structured output in Word and PDF formats
* User prompt execution on final extracted document
* Streamlit UI for ease of use
* Dockerized for simple deployment

---

## 🧠 Pipeline Overview

1. **Upload Document**: User uploads a file and provides a prompt.
2. **Preprocessing**: The document is converted to PDF (if not already).
3. **GPT-4 Extraction**: Extracts text, tables, images, and structural elements.
4. **SmolDocling Extraction**: Sends static prompt to SmolDocling backend for extraction.
5. **Evaluation**: Compares GPT-4 vs SmolDocling outputs using:

   * Textual overlap ratio
   * BLEU score
   * Jaccard similarity
6. **Consistency Check**:

   * ✅ If consistent: build final doc and apply user prompt.
   * ❌ If inconsistent: identify differences and retry SmolDocling with feedback.
7. **Final Output**: Assemble and export the cleaned, structured document.

---

## 🗂️ Folder Structure

```
.
├── app.py                  # Streamlit UI
├── Dockerfile              # Docker configuration
├── requirements.txt
│
├── graph/                  # LangGraph logic
│   ├── graph_builder.py
│   └── nodes/              # Nodes in the pipeline
│       ├── user_input.py
│       ├── preprocess_doc.py
│       ├── gpt_extract.py
│       ├── smoldocling_call.py
│       ├── evaluate.py
│       ├── retry_node.py
│       ├── final_output.py
│       └── apply_prompt.py
│
├── tools/                  # Interfaces to external tools
│   ├── gpt_tool.py
│   ├── smoldocling_tool.py
│   └── storage.py
│
├── utils/                  # Utility modules
│   ├── evaluator.py
│   ├── doc_utils.py
│   └── logger.py
│
└── uploads/                # Uploaded files storage
```

---

## 🧪 Setup Instructions

### 🐳 Run with Docker

```bash
git clone https://github.com/yourname/agentic-doc-intel.git
cd agentic-doc-intel
docker build -t agentic-doc-intel .
docker run -p 8501:8501 agentic-doc-intel
```

### 🧰 Run Locally (Python ≥ 3.10)

```bash
git clone https://github.com/yourname/agentic-doc-intel.git
cd agentic-doc-intel
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Environment Variables

Create a `.env` or configure your environment:

```
OPENAI_API_KEY=your-key-here
SMOLDOCLING_URL=http://localhost:5001/api/extract
```

---

## 📦 Module Responsibilities

* **graph/nodes/**: Each node represents a modular stage in the LangGraph pipeline.
* **tools/gpt\_tool.py**: Manages interactions with GPT-4.
* **tools/smoldocling\_tool.py**: Manages API calls to SmolDocling backend.
* **utils/evaluator.py**: Compares GPT and SmolDocling outputs.
* **utils/doc\_utils.py**: Converts and builds documents.
* **utils/logger.py**: Sets up logging.
* **tools/storage.py**: Saves uploaded files.

---

## ✨ Example Use Cases

* Contract analysis
* Invoice parsing
* Research paper summarization
* Regulatory document extraction

---

## 📬 Contribute

PRs welcome. Open an issue to discuss changes or ideas.

---

## 📜 License

MIT
