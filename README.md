# RAGDocs_Support_Docs_Copilot

### AI-Powered Retrieval-Augmented Generation Platform for Intelligent Support Document Search

RAGDocs_Support_Docs_Copilot is an AI-powered Retrieval-Augmented Generation (RAG) platform that allows users to upload support documents and interact with them using natural-language questions.

The system processes documents, generates semantic embeddings, stores them in ChromaDB, retrieves relevant document content, and uses Google's Gemini model to generate context-aware answers.

---

## 🚀 Project Overview

Traditional document search requires users to manually search through large documents to find relevant information.

RAGDocs_Support_Docs_Copilot provides an intelligent alternative by converting uploaded documents into a searchable semantic knowledge base.

The system allows users to:

- 📄 Upload PDF, DOCX, and TXT documents
- 🔍 Parse and extract document content
- 🧹 Clean extracted text
- ✂️ Split documents into smaller chunks
- 🧠 Generate semantic embeddings
- 🗄️ Store embeddings in ChromaDB
- 🔎 Perform semantic similarity search
- 📚 Retrieve relevant document chunks
- 💬 Ask questions using natural language
- 🤖 Generate context-aware answers using Gemini
- 📋 View uploaded documents
- 🗑️ Delete documents
- ⚡ Interact through a modern React frontend

---

# 🧠 System Architecture

```text
                         ┌──────────────────────────┐
                         │      React Frontend      │
                         │       Vite + React       │
                         └────────────┬─────────────┘
                                      │
                                      │ HTTP / REST API
                                      ▼
                         ┌──────────────────────────┐
                         │      FastAPI Backend     │
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
          ┌───────────────────┐              ┌───────────────────┐
          │  Document Upload  │              │   Chat / Query    │
          └─────────┬─────────┘              └─────────┬─────────┘
                    │                                  │
                    ▼                                  ▼
          ┌───────────────────┐              ┌───────────────────┐
          │  Document Parser  │              │ Query Embedding   │
          └─────────┬─────────┘              └─────────┬─────────┘
                    │                                  │
                    ▼                                  ▼
          ┌───────────────────┐              ┌───────────────────┐
          │   Text Cleaning   │              │ ChromaDB Search   │
          └─────────┬─────────┘              └─────────┬─────────┘
                    │                                  │
                    ▼                                  ▼
          ┌───────────────────┐              ┌───────────────────┐
          │   Text Chunking   │              │ Relevant Chunks   │
          └─────────┬─────────┘              └─────────┬─────────┘
                    │                                  │
                    ▼                                  │
          ┌───────────────────┐                        │
          │    Embeddings     │◄───────────────────────┘
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │     ChromaDB      │
          │    Vector Store   │
          └─────────┬─────────┘
                    │
                    │ Retrieved Context
                    ▼
          ┌──────────────────────────┐
          │   Prompt Construction    │
          └────────────┬─────────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │       Gemini LLM         │
          │   Response Generation    │
          └────────────┬─────────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │    Contextual Answer     │
          └──────────────────────────┘
