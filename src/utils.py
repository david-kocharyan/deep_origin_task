import re

from typing import Tuple, List, Dict


def build_tools_description(registry: dict) -> Tuple[str, str]:
    lines = [f"> {name}: {info['description']}" for name, info in registry.items()]
    names = ", ".join(registry.keys())
    return "\n".join(lines), names


def extract_action(text: str):
    action_pattern = re.compile(r"Action:\s*(?P<action>\w+)\s*\nAction Input:\s*(?P<input>.+)")
    m = action_pattern.search(text)
    return (m.group('action'), m.group('input').strip()) if m else (None, None)


def format_history(history: List[Dict[str, str]]) -> str:
    if not history:
        return "No previous conversation."
    return "\n".join([
        f"- Q: {item['question']}\n  A: {item['answer']}" for item in history
    ])
