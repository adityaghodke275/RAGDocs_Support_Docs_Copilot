import { useEffect, useState } from "react";
import {
  Bot,
  FileText,
  Settings,
  Info,
  MessageSquare,
  Upload,
  Send,
  Trash2,
  RefreshCw,
  User,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [documents, setDocuments] = useState([]);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  // Load documents when page opens
  useEffect(() => {
    loadDocuments();
  }, []);

  // -----------------------------
  // GET DOCUMENTS
  // -----------------------------
  const loadDocuments = async () => {
    try {
      const response = await fetch(`${API_URL}/documents`);

      if (!response.ok) {
        throw new Error("Failed to load documents");
      }

      const data = await response.json();
      setDocuments(data);
    } catch (error) {
      console.error("Error loading documents:", error);
    }
  };

  // -----------------------------
  // FILE SELECTION
  // -----------------------------
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const allowedTypes = [".pdf", ".docx", ".txt"];
    const extension = "." + file.name.split(".").pop().toLowerCase();

    if (!allowedTypes.includes(extension)) {
      alert("Please select a PDF, DOCX, or TXT file.");
      return;
    }

    if (file.size > 20 * 1024 * 1024) {
      alert("File size must be less than 20MB.");
      return;
    }

    setSelectedFile(file);
  };

  // -----------------------------
  // UPLOAD DOCUMENT
  // -----------------------------
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a document first.");
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      alert("Document uploaded successfully.");

      setSelectedFile(null);

      // Refresh document list
      await loadDocuments();
    } catch (error) {
      console.error("Upload error:", error);
      alert(error.message);
    } finally {
      setUploading(false);
    }
  };

  // -----------------------------
  // DELETE DOCUMENT
  // -----------------------------
  const handleDelete = async (documentId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmed) return;

    try {
      const response = await fetch(
        `${API_URL}/documents/${documentId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Delete failed");
      }

      await loadDocuments();
    } catch (error) {
      console.error("Delete error:", error);
      alert(error.message);
    }
  };

  // -----------------------------
  // ASK QUESTION
  // -----------------------------
  const handleAskQuestion = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) return;

    // Add user message immediately
    const userMessage = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previous) => [...previous, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to get answer");
      }

      const assistantMessage = {
        role: "assistant",
        content: data.answer || "No answer was returned.",
        sources: data.sources || [],
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I could not process your question. Please make sure the backend is running.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // ENTER KEY
  // -----------------------------
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAskQuestion();
    }
  };

  // -----------------------------
  // FILE ICON
  // -----------------------------
  const getFileIcon = (filename) => {
    const extension = filename
      ?.split(".")
      .pop()
      ?.toLowerCase();

    if (extension === "pdf") {
      return "PDF";
    }

    if (extension === "docx") {
      return "W";
    }

    return "TXT";
  };

  return (
    <div className="app">

      {/* =========================
          SIDEBAR
      ========================== */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            <Bot size={27} />
          </div>

          <div>
            <div className="brand-title">Support Docs</div>
            <div className="brand-subtitle">Copilot</div>
          </div>
        </div>

        <nav className="navigation">

          <button className="nav-item active">
            <MessageSquare size={20} />
            <span>Ask Copilot</span>
          </button>

          <button className="nav-item">
            <FileText size={20} />
            <span>Documents</span>
          </button>

          <button className="nav-item">
            <Settings size={20} />
            <span>Settings</span>
          </button>

          <button className="nav-item">
            <Info size={20} />
            <span>About</span>
          </button>

        </nav>

        <div className="sidebar-bottom">

          <button className="theme-button">
            ☼
          </button>

          <div className="sidebar-footer">
            © 2026 Support Docs Copilot
          </div>

        </div>

      </aside>


      {/* =========================
          MAIN CONTENT
      ========================== */}
      <main className="main-content">

        {/* HEADER */}
        <header className="top-header">

          <div>
            <h1>Ask Copilot</h1>

            <p>
              Get answers from your support documents.
            </p>
          </div>

          <div className="profile">

            <div className="profile-avatar">
              A
            </div>

            <span>Admin</span>

            <span className="profile-arrow">
              ˅
            </span>

          </div>

        </header>


        {/* =========================
            TOP CARDS
        ========================== */}
        <section className="top-cards">

          {/* UPLOAD CARD */}
          <div className="card upload-card">

            <h2>Upload Document</h2>

            <div
              className="upload-area"
              onClick={() =>
                document.getElementById("file-input").click()
              }
            >

              <Upload
                className="upload-icon"
                size={48}
              />

              <h3>
                Drag & drop your file here
              </h3>

              <p className="browse-text">
                or click to browse
              </p>

              <p className="file-info">
                PDF, DOCX, TXT (Max 20MB)
              </p>

              <button
                className="choose-button"
                type="button"
              >
                <Upload size={18} />
                Choose File
              </button>

              {selectedFile && (
                <div className="selected-file">
                  Selected: {selectedFile.name}
                </div>
              )}

            </div>

            <input
              id="file-input"
              type="file"
              accept=".pdf,.docx,.txt"
              hidden
              onChange={handleFileChange}
            />

            {selectedFile && (
              <button
                className="upload-button"
                onClick={handleUpload}
                disabled={uploading}
              >
                {uploading
                  ? "Uploading..."
                  : "Upload Document"}
              </button>
            )}

          </div>


          {/* DOCUMENTS CARD */}
          <div className="card documents-card">

            <div className="card-heading">

              <h2>Your Documents</h2>

              <button
                className="refresh-button"
                onClick={loadDocuments}
              >
                <RefreshCw size={17} />
                Refresh
              </button>

            </div>

            <div className="documents-list">

              {documents.length === 0 ? (

                <div className="empty-documents">
                  <FileText size={30} />
                  <p>No documents uploaded yet.</p>
                </div>

              ) : (

                documents.map((document) => (

                  <div
                    className="document-row"
                    key={document.id}
                  >

                    <div className="document-info">

                      <div
                        className={`file-icon ${
                          document.file_type === "pdf"
                            ? "pdf-icon"
                            : document.file_type === "docx"
                            ? "word-icon"
                            : "txt-icon"
                        }`}
                      >
                        {getFileIcon(
                          document.original_filename ||
                          document.filename
                        )}
                      </div>

                      <div>

                        <div className="document-name">
                          {document.original_filename ||
                            document.filename}
                        </div>

                        <div className="document-date">
                          Uploaded{" "}
                          {document.uploaded_at
                            ? new Date(
                                document.uploaded_at
                              ).toLocaleDateString(
                                "en-GB",
                                {
                                  day: "2-digit",
                                  month: "short",
                                  year: "numeric",
                                }
                              )
                            : "Recently"}
                        </div>

                      </div>

                    </div>


                    <div className="document-actions">

                      <span className="status-badge">
                        {document.status || "Indexed"}
                      </span>

                      <button
                        className="delete-button"
                        onClick={() =>
                          handleDelete(document.id)
                        }
                        title="Delete document"
                      >
                        <Trash2 size={19} />
                      </button>

                    </div>

                  </div>

                ))

              )}

            </div>

          </div>

        </section>


        {/* =========================
            CHAT SECTION
        ========================== */}
        <section className="card chat-card">

          <div className="chat-heading">

            <h2>Ask a Question</h2>

            <p>
              Ask anything about your documents and get
              accurate answers.
            </p>

          </div>


          {/* CHAT MESSAGES */}
          <div className="chat-messages">

            {messages.length === 0 ? (

              <div className="chat-empty">

                <div className="chat-empty-icon">
                  <Bot size={30} />
                </div>

                <h3>
                  Ask something about your documents
                </h3>

                <p>
                  Your AI assistant will search your
                  documents and provide an answer.
                </p>

              </div>

            ) : (

              messages.map((message, index) => (

                <div
                  className={`message-row ${
                    message.role === "user"
                      ? "user-row"
                      : "assistant-row"
                  }`}
                  key={index}
                >

                  {message.role === "assistant" && (
                    <div className="message-avatar bot-avatar">
                      <Bot size={21} />
                    </div>
                  )}

                  <div
                    className={`message ${
                      message.role === "user"
                        ? "user-message"
                        : "assistant-message"
                    }`}
                  >

                    <div className="message-content">
                      {message.content}
                    </div>

                   
                  </div>

                  {message.role === "user" && (
                    <div className="message-avatar user-avatar">
                      <User size={20} />
                    </div>
                  )}

                </div>

              ))

            )}

            {loading && (

              <div className="message-row assistant-row">

                <div className="message-avatar bot-avatar">
                  <Bot size={21} />
                </div>

                <div className="message assistant-message">
                  <div className="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>

              </div>

            )}

          </div>


          {/* QUESTION INPUT */}
          <div className="question-input-wrapper">

            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about your documents..."
              rows="1"
              disabled={loading}
            />

            <button
              className="send-button"
              onClick={handleAskQuestion}
              disabled={
                loading || !question.trim()
              }
            >
              <Send size={19} />
              Send
            </button>

          </div>

        </section>

      </main>

    </div>
  );
}

export default App;