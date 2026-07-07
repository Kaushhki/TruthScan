# 📰 TruthScan

An AI-powered fact-checking tool that verifies news claims in **Hindi, English, and Hinglish** against real web sources — instead of just guessing from language patterns.

Built with Streamlit, [Groq](https://groq.com) (Llama 3.3 70B) for reasoning, and [Tavily](https://tavily.com) for live web search.

---

## ✨ Features

- **Bilingual input** — paste news in English, Hindi, or mixed Hinglish
- **Real evidence, not guesswork** — extracts the core claim, searches the live web, and weighs actual sources before giving a verdict
- **Transparent sourcing** — every verdict shows the exact links it checked, so you can verify it yourself
- **Honest uncertainty** — says "no clear evidence" instead of forcing a fake/real guess when sources are thin
- **Surface-level warning signs** — flags sensational language, viral-forward phrasing, and excessive caps/exclamation as a supplementary signal
- Clean, aesthetic dark gradient UI

---

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| Reasoning / claim extraction | [Groq API](https://groq.com) — `llama-3.3-70b-versatile` |
| Web search | [Tavily API](https://tavily.com) |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/truthscan.git
cd truthscan
```

### 2. Install dependencies

```bash
pip install streamlit groq tavily-python
```

### 3. Add your API keys

Create a file at `.streamlit/secrets.toml` (this file is **git-ignored** and never pushed):

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
TAVILY_API_KEY = "tvly_your_actual_key_here"
```

Get free keys from:
- Groq → https://console.groq.com
- Tavily → https://tavily.com

### 4. Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 📁 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── .streamlit/
│   └── secrets.toml         # Your API keys (not committed)
├── .gitignore
└── README.md
```

---

## ⚠️ Disclaimer

This tool provides an AI-generated assessment based on web search results. It is **not a substitute for professional fact-checking**. Always verify important claims through multiple trusted sources before sharing or acting on them.

---

## 📄 License

MIT — feel free to use, modify, and share.
