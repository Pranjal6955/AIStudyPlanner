# 🎓 AI Study Planner

An intelligent, multi-agent study planner powered by **LangChain**, **LangGraph**, and **Groq** (free & blazing fast inference). Give it your learning goal and it generates a personalised, week-by-week study plan complete with curated resources.

---

## 🧠 How It Works

The system uses a **4-agent pipeline** orchestrated by LangGraph:

```
User Input
    │
    ▼
┌─────────────────┐
│  Goal Analyzer  │  → Extracts objective, duration & skill level
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Planner Agent  │  → Builds weekly & daily study breakdown
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Resource Agent  │  → Recommends YouTube, docs & courses
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reviewer Agent  │  → Polishes plan to be clear & motivating
└─────────────────┘
         │
         ▼
    Final Output
```

---

## 📁 Project Structure

```
AIStudyPlanner/
├── multi_agent_system.py  # Main application — agents & LangGraph workflow
├── .env                   # Your local secrets (not committed)
├── .env.example           # Template for required environment variables
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Clone / navigate to the project

```bash
cd AIStudyPlanner
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up / log in (free, no credit card needed)
3. Click **Create API Key** and copy it

### 5. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and paste your key:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 Usage

```bash
python multi_agent_system.py
```

Example session:

```
🚀 AI Study Planner (Multi-Agent System)
Enter your goal: Learn machine learning from scratch in 3 months as a beginner

📌 FINAL OUTPUT:

Week 1-2: Python & Math Foundations
  - Day 1: Python basics — variables, loops, functions ...
  ...
```

---

## 🔧 Environment Variables

| Variable           | Required | Default                    | Description                                      |
|--------------------|----------|----------------------------|--------------------------------------------------|
| `GROQ_API_KEY`     | ✅ Yes   | —                          | Your Groq API key (free at console.groq.com)     |
| `GROQ_MODEL`       | No       | `llama-3.3-70b-versatile`  | Groq model to use                                |
| `GROQ_TEMPERATURE` | No       | `0.7`                      | Sampling temperature (0 = focused, 2 = creative) |

---

## 📦 Dependencies

| Package          | Purpose                              |
|------------------|--------------------------------------|
| `langchain`      | LLM abstraction & message schemas    |
| `langchain-groq` | Groq integration for LangChain       |
| `langgraph`      | Multi-agent graph orchestration      |
| `python-dotenv`  | `.env` file loading                  |

---

## 🛡️ Security

- **Never commit `.env`** — add it to `.gitignore`:
  ```
  .env
  ```
- Use `.env.example` as the checked-in reference for collaborators.
