import math

import requests
from src.config import settings


def search_web(query: str) -> str:
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": "advanced",
    }
    headers = {
        "Authorization": f"Bearer {settings.tavily_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "[No answer found]")
    except Exception as e:
        return f"Search Web error: {e}"


def calculator(expression: str) -> str:
    try:
        allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        code = compile(expression, "<string>", "eval")
        return str(eval(code, {"__builtins__": {}}, allowed_names))
    except Exception as e:
        return f"Calculator error: {e}"


def get_tools():
    return {
        "Search_Web": {
            "fn": search_web,
            "description": (
                "Use this tool to search the web for up-to-date, real-time information. "
                "Best for recent events, trending topics, current news, or anything not covered by static knowledge."
            )
        },
        "Calculator": {
            "fn": calculator,
            "description": (
                "Use this tool to evaluate mathematical expressions. Supports arithmetic, functions like sin(), cos(), log(), "
                "square roots, and rounding with round(). Useful for unit conversions, financial calculations, or equations."
            )
        }
    }
