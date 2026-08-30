# NexusRAG
### Enterprise Document Intelligence & Retrieval-Augmented Generation Platform

NexusRAG is an AI-powered document intelligence platform that enables users to upload support documents and interact with them through natural-language questions.

The system combines document processing, semantic embeddings, vector search, Retrieval-Augmented Generation (RAG), and Gemini-powered response generation to provide context-aware answers based on the uploaded documents.

---

## 🚀 Overview

Traditional document search requires users to manually scan large documents to find relevant information.

NexusRAG solves this problem by transforming uploaded documents into searchable semantic knowledge.

Users can:

- Upload PDF, DOCX, and TXT documents
- Automatically parse and clean document content
- Split documents into optimized text chunks
- Generate semantic embeddings
- Store embeddings in ChromaDB
- Perform semantic similarity search
- Retrieve the most relevant document sections
- Ask natural-language questions
- Generate context-aware answers using Gemini
- View and manage uploaded documents
- Delete documents from the system

---

## 🧠 Core Architecture

```text
                    ┌─────────────────────────┐
                    │       React Frontend    │
                    │     Vite + React UI     │
                    └────────────┬────────────┘
                                 │
                         HTTP / REST API
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend    │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
        ┌─────────────────┐             ┌─────────────────┐
        │ Document Upload │             │   Chat / Query  │
        └────────┬────────┘             └────────┬────────┘
                 │                               │
                 ▼                               ▼
        ┌─────────────────┐             ┌─────────────────┐
        │ Document Parser │             │ Query Embedding │
        └────────┬────────┘             └────────┬────────┘
                 │                               │
                 ▼                               ▼
        ┌─────────────────┐             ┌─────────────────┐
        │ Text Cleaning   │             │ ChromaDB Search │
        └────────┬────────┘             └────────┬────────┘
                 │                               │
                 ▼                               ▼
        ┌─────────────────┐             ┌─────────────────┐
        │ Text Chunking   │             │ Relevant Chunks │
        └────────┬────────┘             └────────┬────────┘
                 │                               │
                 ▼                               ▼
        ┌─────────────────┐                      │
        │    Embeddings   │◄─────────────────────┘
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    ChromaDB     │
        │  Vector Store   │
        └─────────────────┘

                         Retrieved Context
                                │
                                ▼
                    ┌─────────────────────────┐
                    │    Prompt Construction  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       Gemini LLM        │
                    │    Response Generation  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Contextual Answer    │
                    └─────────────────────────┘
