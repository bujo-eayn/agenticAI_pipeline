# Agentic AI for Deep Scientific Research

## 🔍 Summary

Agentic AI systems have the potential to transform deep scientific research by modeling and automating complex workflows. This project implements a multi-agent architecture that leverages foundational and specialized language models to parse, extract, and analyze scientific documents.

## 🚀 Features

* Supervisor-worker architecture using GPT-4o
* Document Parsing Agent using Smoldocling
* Visual Interpreter Agent using Gemini
* Modular and extensible framework
* Workflow planning and error correction
* Tools for external actions by agents

## 📦 Module Responsibilities

| Module                    | Responsibility                                                         |
| ------------------------- | ---------------------------------------------------------------------- |
| `graph/nodes/`            | LangGraph node definitions representing stages in the AI workflow      |
| `graph/agents/`           | Individual agent implementations with modular logic and interactivity  |
| `tools/`                  | Tool definitions used by agents to accomplish specific sub-tasks       |
| `utils/`                  | Utility functions for data formatting, logging, and support operations |
| `uploads/`                | Temporary storage for uploaded documents or files                      |
| `debug/`                  | GPT reasoning traces and execution logs for Version 2                  |
| `outputs/pdf_only_tests/` | Output results from Version 1's evaluation phase                       |
| `findings/`               | Discovered patterns and emergent behaviors from Version 2 experiments  |
| `tests/`                  | Unit tests for validating individual module functionality              |

## 🧪 Versions

### 🔖 Version 1 (Main Branch)

* Stable MVP implementation of LangGraph workflow
* Basic task driven logic with a static pipeline
* Available at: [main branch](https://github.com/bujo-eayn/agenticAI_pipeline/tree/main)

### 🧪 Version 2 (Current Branch)

* Advanced Agentic workflow with supervisor-worker pattern
* True agents built (Supervisor) with tool and agent calling capacity
* Abstract and research documentation added
* You are currently viewing **Version 2** in this branch

## 📄 Abstract & Research

The scientific abstract detailing the research scope, system design, and results is available in [`about.md`](./about.md).

## ⚙️ Setup Instructions

```bash
# Clone the repository
$ git clone https://github.com/bujo-eayn/agenticAI_pipeline
$ cd agenticAI_pipeline

# Set up a virtual environment (recommended)
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
$ pip install -r requirements.txt
```

### 🔐 Environment Variables

Create a `.env` file in the root directory and include the following:

```env
OPENAI_API_KEY=your_openai_key_here
SMOLDOCLING_API_URL=http://localhost:8080
GEMINI_API_KEY=your_gemini_key_here
```

## 👥 Contributors

We gratefully acknowledge contributions from the following GitHub users:

* [@Daniela Patricia Cheng Rodriguez](https://github.com/DanielaCh257)
* [@Faith Wangui Njoroge](https://github.com/WanguiMps)
* [@Wesley McGinn](https://github.com/WesleyMcGinn)
* [@Job Ian Onyango](https://github.com/bujo-eayn)

## 📜 License

This project is licensed under the [MIT License](./LICENSE).
