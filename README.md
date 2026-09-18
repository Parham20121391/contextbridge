# ContextBridge

> **Move your AI context from one session to another — without starting from zero.**

ContextBridge is an open-source MVP for importing exported conversations from **Claude** and **ChatGPT**, turning them into structured conversation data, summarizing them with AI, and generating a **Ready Prompt** that can be used to continue the work in a new AI session.

The goal is simple: **preserve the important context of a conversation so you can keep working instead of rebuilding everything from scratch.**

---

## ✨ What is ContextBridge?

AI conversations often contain a lot of useful context:

- project requirements
- decisions and preferences
- technical details
- previous attempts
- important constraints
- unfinished tasks
- useful explanations

When you move that work to another AI session, much of that context can be lost.

ContextBridge is designed to solve that problem.

### The current workflow

```text
Claude / ChatGPT Export
        │
        ▼
   ContextBridge
        │
        ├── Parse conversation
        │
        ├── Store conversation
        │
        ├── Summarize with AI
        │
        └── Generate Ready Prompt
                │
                ▼
        Continue in a new session
```

---

## 🚀 Current Features

### 📥 Import conversations

ContextBridge currently supports conversation exports based on the structures used by:

- **Claude**
- **ChatGPT**

You upload the exported JSON file through the web interface and ContextBridge detects the supported format automatically.

### 🧠 AI summarization

Imported conversations can be summarized using:

- **Google Gemini**
- **OpenRouter**

Three summary styles are currently available:

| Style | Description |
|---|---|
| **Detailed** | A more comprehensive summary of the conversation |
| **Brief** | A short summary in roughly 3–4 sentences |
| **Bullets** | Clear, compact bullet points |

### 🎯 Ready Prompt

ContextBridge generates a **Ready Prompt** alongside the summary.

The idea is to turn the important context of the old conversation into something you can provide to a new AI session so it can understand what happened and continue the work.

### 💾 Local conversation storage

Imported conversations are stored locally by the backend as JSON data.

### 🌐 Simple web interface

The project includes a Persian, RTL-friendly web interface for:

1. uploading conversations
2. viewing stored conversations
3. selecting an AI provider
4. selecting a summary style
5. generating the summary

---

## 🧩 Why does ContextBridge exist?

Imagine you've spent several hours building a project with an AI.

The conversation contains:

> requirements + architecture + decisions + bugs + fixes + preferences + unfinished work

Then you need to start a new session.

Instead of explaining everything again, ContextBridge is intended to give you a structured bridge between the old session and the new one.

**That bridge is ContextBridge.**

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Jinja2
- HTTPX
- python-dotenv
- aiofiles
- python-multipart

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 templates

### AI Providers

- Google Gemini
- OpenRouter

### Storage

The current MVP uses local JSON-based storage.

---

## 📁 Project Structure

```text
contextbridge/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── projects.py
│   │   ├── summarize.py
│   │   └── upload.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── parser.py
│       ├── storage.py
│       └── summarizer.py
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   │
│   └── templates/
│       └── index.html
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Requirements

Before running ContextBridge, make sure you have:

- Python 3.10+ recommended
- pip
- an API key for at least one supported AI provider if you want AI summarization

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Parham20121391/contextbridge.git
cd contextbridge
```

### 2. Create a virtual environment

**Windows PowerShell / Terminal:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS / WSL:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Run this in the **project root**:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a file named:

```text
.env
```

in the **project root**.

Depending on the provider you use, configure the corresponding API credentials.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
```

> Never commit your real API keys to GitHub.

The repository's `.gitignore` is configured to ignore `.env`.

---

## ▶️ Run ContextBridge

From the **project root**, start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Then open:

**http://localhost:8000**

The application is served by the FastAPI backend.

---

## 🧑‍💻 How to Use It

### Step 1 — Export your conversation

Export a conversation from Claude or ChatGPT as JSON.

ContextBridge currently expects supported export structures from these platforms.

### Step 2 — Import the JSON

Open ContextBridge in your browser and upload the exported JSON file.

The backend will:

1. read the JSON
2. detect the conversation format
3. parse the messages
4. store the conversation
5. return the conversation information

### Step 3 — Choose an AI provider

Select:

- Gemini
- OpenRouter

### Step 4 — Choose a summary style

Choose one of:

- Detailed
- Brief
- Bullets

### Step 5 — Generate the summary

ContextBridge sends the conversation content to the selected AI provider.

The result contains:

```json
{
  "summary": "...",
  "key_points": [
    "...",
    "...",
    "..."
  ],
  "ready_prompt": "..."
}
```

### Step 6 — Continue your work

Use the generated **Ready Prompt** as the starting context for a new AI session.

---

## 🔌 API

ContextBridge exposes several API endpoints through FastAPI.

### Upload conversation

```http
POST /api/upload/
```

Uploads and parses a conversation export.

### List uploaded conversations

```http
GET /api/upload/list
```

Returns stored conversations.

### Summarize a conversation

```http
POST /api/summarize/
```

Generates an AI-powered summary for a stored conversation.

### Create a project

```http
POST /api/projects/
```

Creates a project entry.

### List projects

```http
GET /api/projects/
```

Returns available project entries.

---

## 🧠 How Parsing Works

ContextBridge detects the structure of an uploaded JSON file.

### Claude

Claude exports are detected using the `chat_messages` structure.

### ChatGPT

ChatGPT exports are detected using the `mapping` structure.

If neither supported structure is found, ContextBridge returns an unsupported-format error.

This means the current MVP is intentionally focused on known export formats rather than attempting to parse arbitrary JSON files.

---

## 🤖 How Summarization Works

The summarization service prepares the conversation and sends it to the selected provider.

The current implementation supports:

### Gemini

The current Gemini integration uses:

```text
gemini-1.5-flash
```

### OpenRouter

The OpenRouter model can be configured through:

```env
OPENROUTER_MODEL=...
```

If no model is configured, the current implementation has a default OpenRouter model.

---

## ⚠️ Current Limitations

ContextBridge is currently an **MVP**, so there are important limitations.

### Conversation length

The current summarization implementation limits the conversation text sent to the AI to the first **8,000 characters**.

Very large conversations therefore may not be fully represented in the generated summary.

### Supported formats

Only the currently implemented Claude and ChatGPT export structures are supported.

### Authentication

There is currently no user authentication system.

### Storage

The MVP currently uses local JSON-based storage rather than a production database.

### Deployment

The current project is primarily designed to run locally.

### Browser extension

ContextBridge is **not currently a Chrome extension**.

A browser extension is part of the planned future direction.

---

## 🗺️ Roadmap

The project is intended to evolve from a simple conversation importer into a broader **AI context management system**.

Potential future work includes:

- [ ] Chrome / Chromium browser extension
- [ ] Direct browser-based context capture
- [ ] Better conversation import support
- [ ] Multi-export import
- [ ] Project-based context management
- [ ] Persistent database storage
- [ ] Improved long-conversation handling
- [ ] Better context extraction
- [ ] Authentication and user accounts
- [ ] Production deployment
- [ ] More AI providers
- [ ] Improved Ready Prompt generation
- [ ] Context history and versioning

> Roadmap items are planned directions, not features currently guaranteed to exist.

---

## 🔒 Privacy & Security

ContextBridge is currently designed as a local MVP.

However, when you use an external AI provider such as Gemini or OpenRouter, conversation content sent to that provider is subject to that provider's policies and processing.

For local development:

- keep your API keys in `.env`
- do not commit secrets
- review the conversation before sending sensitive information to an external AI provider
- remember that the current project does not provide authentication

---

## 🧪 Error Handling

The current backend handles several common cases, including:

- invalid JSON uploads
- unsupported conversation formats
- missing conversations
- unavailable or unsuccessful summarization responses

For unsupported uploads, the parser reports that the file format was not recognized and asks for a Claude or ChatGPT export.

---

## 🏗️ Architecture

At a high level, ContextBridge is organized into three layers:

### Frontend

Responsible for the user interface and browser interactions.

```text
frontend/
├── templates/
└── static/
```

### API / Backend

FastAPI exposes the application's HTTP endpoints.

```text
backend/main.py
backend/routers/
```

### Services

Application logic is separated into services for:

- parsing
- storage
- summarization

```text
backend/services/
```

This separation makes the MVP easier to extend as the project grows.

---

## 🤝 Contributing

Contributions are welcome.

A typical contribution workflow is:

```text
Fork
  ↓
Create a feature branch
  ↓
Make your changes
  ↓
Test locally
  ↓
Open a Pull Request
```

When contributing, try to:

- keep the existing project structure
- avoid unnecessary dependencies
- keep features focused
- document meaningful changes
- avoid committing secrets or local data

---

## 📜 License

No license has currently been declared for this repository.

Until a license is added, the repository should not be assumed to grant broad permission to copy, modify, distribute, or commercially use the code.

---

## 👤 Author

**Parham RahimPour** [@GitHub](plugin://github@openai-curated-remote)

---

## 💡 Project Idea

ContextBridge started from a simple problem:

> **Your AI session shouldn't be a dead end.**

The project is built around the idea that conversation context should be portable.

Instead of treating every AI session as an isolated chat, ContextBridge aims to make context something you can **move, preserve, summarize, and continue**.

---

## ⭐ Support

If ContextBridge is useful to you, consider giving the repository a ⭐ on GitHub and sharing feedback through Issues.

**Repository:** https://github.com/Parham20121391/contextbridge
