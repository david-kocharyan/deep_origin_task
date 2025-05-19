# ReAct Agent with Gemini + Streamlit

This project implements a ReAct-style agent using Google's Gemini API and integrates it with Streamlit.
The agent thinks step-by-step, uses tools like web search and calculator, and produces a final answer with transparent
reasoning.

---

## Tools

| Tool         | Description                                                                             |
|--------------|-----------------------------------------------------------------------------------------|
| `Search_Web` | Using this tool to search the web for up-to-date, real-time information (Tavily API)    |
| `Calculator` | Evaluate mathematical expressions (Small function do not handle some math expressions ) |

---

## Installation

### 1. Clone the repo

```bash
  git clone https://github.com/your-username/react-agent-gemini.git
  cd react-agent-gemini
```

### 2. Set up a virtual environment

```bash
  python -m venv venv
  source venv/bin/activate
```

### 3. Install dependencies

```bash
    pip install -r requirements.txt
```

---

## Configuration

Copy .env.example file in the project root as .evn

```text
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

* Note: I will provide the Tavily API key in .env.example file. You can use it to make more than 500 requests.

---

### Running the App

```bash
  streamlit run main.py
```

---

