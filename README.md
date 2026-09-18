# ContextBridge

> **AI Context Transfer & Continuation — انتقال کانتکست بین سشن‌های هوش مصنوعی**

ContextBridge یک ابزار Open Source و در حال توسعه است که برای **انتقال context مکالمات هوش مصنوعی از یک session به session دیگر** ساخته شده است.

ContextBridge can import supported **Claude** and **ChatGPT** conversation exports, parse and store them, summarize them with AI, and generate a **Ready Prompt** for continuing work in a new AI session.

---

## 🎯 ایده اصلی | Core Idea

وقتی چند ساعت با یک AI روی یک پروژه کار می‌کنید، conversation شما معمولاً شامل requirements، تصمیم‌ها، ساختار پروژه، bugها، راه‌حل‌ها، محدودیت‌ها و کارهای باقی‌مانده است.

When you move to a new AI session, important context can be lost. ContextBridge creates a bridge between the old and new sessions.

> **Your AI session shouldn't be a dead end.**

---

## ✨ قابلیت‌ها | Features

### 📥 Import Conversations | وارد کردن مکالمات

نسخه فعلی ساختارهای export مربوط به **Claude** و **ChatGPT** را پشتیبانی می‌کند.

The current MVP detects the supported Claude and ChatGPT JSON structures automatically.

### 🧠 AI Summarization | خلاصه‌سازی با هوش مصنوعی

Providerهای فعلی:
- Google Gemini
- OpenRouter

سبک‌های فعلی:

| Style | فارسی | توضیح |
|---|---|---|
| **Detailed** | کامل | خلاصه جامع‌تر |
| **Brief** | کوتاه | حدود ۳ تا ۴ جمله |
| **Bullets** | بولتی | نکات مهم به‌صورت bullet point |

### 🎯 Ready Prompt | پرامپت آماده

ContextBridge همراه با summary یک **Ready Prompt** تولید می‌کند که برای انتقال context مهم conversation قبلی به یک session جدید طراحی شده است.

### 💾 Local Storage | ذخیره‌سازی محلی

Conversationهای import شده در MVP فعلی به‌صورت JSON در storage محلی ذخیره می‌شوند.

### 🌐 Web Interface | رابط کاربری وب

رابط وب فعلی امکان upload، مشاهده conversationهای ذخیره‌شده، انتخاب provider، انتخاب summary style و تولید نتیجه را فراهم می‌کند.

---

## 🔄 Workflow | روند کار

```text
Claude / ChatGPT Export
        │
        ▼
   ContextBridge
        │
        ├── Parse conversation
        ├── Store conversation
        ├── Summarize with AI
        └── Generate Ready Prompt
                │
                ▼
        Continue in a new session
```

**Export → Import → Parse → Store → Summarize → Ready Prompt → Continue**

---

## 🛠️ Tech Stack | تکنولوژی‌ها

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
- Jinja2 Templates

### AI Providers
- Google Gemini
- OpenRouter

### Storage
- Local JSON storage

---

## 📁 Project Structure | ساختار پروژه

```text
contextbridge/
│
├── backend/
│   ├── main.py
│   ├── models/
│   │   └── schemas.py
│   ├── routers/
│   │   ├── projects.py
│   │   ├── summarize.py
│   │   └── upload.py
│   └── services/
│       ├── parser.py
│       ├── storage.py
│       └── summarizer.py
│
├── frontend/
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/index.html
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Requirements | پیش‌نیازها

- Python 3.10+ recommended
- pip
- API key for at least one supported AI provider for AI summarization

---

## 📦 Installation | نصب

### 1. Clone

**Run in Terminal / PowerShell:**

```bash
git clone https://github.com/Parham20121391/contextbridge.git
cd contextbridge
```

### 2. Virtual Environment

**Windows PowerShell / Terminal:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS / WSL:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

**Run in the project root:**

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables | تنظیم API Key

در root پروژه یک فایل `.env` بسازید.

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
```

> ⚠️ **Never commit real API keys to GitHub.**

---

## ▶️ Run | اجرای پروژه

**Run from the project root:**

```bash
cd backend
uvicorn main:app --reload --port 8000
```

سپس:

```text
http://localhost:8000
```

---

## 🧑‍💻 Usage | نحوه استفاده

### Step 1 — Export
از Claude یا ChatGPT conversation موردنظر را به‌صورت JSON export کنید.

Export a supported Claude or ChatGPT conversation as JSON.

### Step 2 — Import
فایل JSON را در ContextBridge آپلود کنید. Backend آن را می‌خواند، format را تشخیص می‌دهد، پیام‌ها را parse می‌کند و conversation را ذخیره می‌کند.

### Step 3 — Choose Provider
Gemini یا OpenRouter را انتخاب کنید.

### Step 4 — Choose Style
Detailed، Brief یا Bullets را انتخاب کنید.

### Step 5 — Generate
خلاصه و Ready Prompt تولید می‌شوند.

```json
{
  "summary": "...",
  "key_points": ["...", "...", "..."],
  "ready_prompt": "..."
}
```

### Step 6 — Continue
Ready Prompt را در session جدید AI استفاده کنید.

---

## 🔌 API Reference | مرجع API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/upload/` | Upload and parse conversation |
| GET | `/api/upload/list` | List stored conversations |
| POST | `/api/summarize/` | Generate AI summary |
| POST | `/api/projects/` | Create project |
| GET | `/api/projects/` | List projects |

---

## 🧠 Parsing | نحوه تشخیص Export

### Claude
ساختار `chat_messages` برای تشخیص export مربوط به Claude استفاده می‌شود.

### ChatGPT
ساختار `mapping` برای تشخیص export مربوط به ChatGPT استفاده می‌شود.

اگر هیچ‌کدام پیدا نشوند، format فایل شناخته‌شده نیست.

---

## 🤖 AI Summarization | سیستم خلاصه‌سازی

### Gemini
Implementation فعلی از `gemini-1.5-flash` استفاده می‌کند.

### OpenRouter
مدل از طریق `OPENROUTER_MODEL` قابل تنظیم است و implementation فعلی یک default model دارد.

---

## ⚠️ Limitations | محدودیت‌های فعلی

- **8,000 characters:** در summarization فعلی، متن conversation ارسال‌شده به AI به ۸۰۰۰ کاراکتر اول محدود می‌شود.
- **Export formats:** فقط ساختارهای فعلی Claude و ChatGPT پشتیبانی می‌شوند.
- **Authentication:** سیستم authentication وجود ندارد.
- **Storage:** storage فعلی JSON محلی است.
- **Deployment:** پروژه فعلی عمدتاً برای اجرای local طراحی شده است.
- **Browser Extension:** ContextBridge هنوز Chrome Extension نیست.

---

## 🗺️ Roadmap | مسیر توسعه

هدف آینده تبدیل ContextBridge به یک **AI Context Management System** است.

- [ ] Chrome / Chromium Extension
- [ ] Direct browser context capture
- [ ] پشتیبانی از exportهای بیشتر
- [ ] Multi-export import
- [ ] Project-based context management
- [ ] Database storage
- [ ] Better long-conversation handling
- [ ] Advanced context extraction
- [ ] Authentication & user accounts
- [ ] Production deployment
- [ ] More AI providers
- [ ] Improved Ready Prompt generation
- [ ] Context history & versioning

> Roadmap items are future plans, not current features.

---

## 🔒 Privacy & Security | حریم خصوصی و امنیت

ContextBridge در حال حاضر یک MVP محلی است. هنگام استفاده از Gemini یا OpenRouter، conversation برای پردازش به provider انتخاب‌شده ارسال می‌شود.

Best practices:
- API keyها را در `.env` نگه دارید.
- secretها را commit نکنید.
- قبل از ارسال اطلاعات حساس، محتوای conversation را بررسی کنید.
- به نبود authentication در MVP فعلی توجه کنید.

---

## 🏗️ Architecture | معماری

پروژه در سطح کلی از سه بخش تشکیل شده است:

- **Frontend:** رابط کاربری و browser interactions
- **Backend / API:** FastAPI و HTTP endpoints
- **Services:** Parser، Storage و Summarizer

این جداسازی، توسعه قابلیت‌های آینده را ساده‌تر می‌کند.

---

## 🤝 Contributing | مشارکت

```text
Fork
  ↓
Create a branch
  ↓
Make changes
  ↓
Test locally
  ↓
Open Pull Request
```

لطفاً ساختار پروژه را حفظ کنید، dependency غیرضروری اضافه نکنید، تغییرات را مستند کنید و secretها را commit نکنید.

---

## 📜 License | مجوز

در حال حاضر repository license مشخصی ندارد.

Until a license is added, the repository should not be assumed to grant broad permissions to copy, modify, distribute, or commercially use the code.

---

## 👤 Author | سازنده

**Parham RahimPour** [@GitHub](plugin://github@openai-curated-remote)

---

## 💡 Philosophy | فلسفه پروژه

**Context should be portable.**

کانتکست نباید در یک conversation گیر کند.

**Move → Preserve → Summarize → Continue**

---

## ⭐ Support the Project

اگر ContextBridge برایتان مفید بود، repository را ⭐ کنید و feedback یا contribution خود را از طریق GitHub ارائه دهید.

**Repository:** https://github.com/Parham20121391/contextbridge