from typing import List, Tuple, Dict

from google import genai
from google.genai.types import GenerateContentConfig

from src.prompt import REACT_PROMPT_TEMPLATE
from src.utils import build_tools_description, extract_action, format_history
from src.tools import get_tools
from src.config import settings


class ReActAgent:
    def __init__(self, api_key: str = settings.google_api_key, model_name: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.tools = get_tools()
        self.tools_md, self.tool_names = build_tools_description(self.tools)

    def run(
            self,
            question: str,
            history: List[Dict[str, str]],
            max_steps: int = 10
    ) -> Tuple[str, List[Dict[str, str]], str]:
        agent_scratchpad = ""
        answer = None
        steps = 0

        while answer is None and steps < max_steps:
            steps += 1

            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=self.tools_md,
                tool_names=self.tool_names,
                history=format_history(history),
                input=question,
                agent_scratchpad=agent_scratchpad.strip()
            )

            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(stop_sequences=["Final Answer:"])
            )

            output = resp.text.strip()
            if "Final Answer:" in output:
                answer = output.split("Final Answer:")[-1].strip()
                break

            action, action_input = extract_action(output)
            if not action:
                break

            fn = self.tools.get(action, {}).get("fn")
            observation = fn(action_input) if fn else f"[Error] Unknown tool: {action}"
            agent_scratchpad += f"\n{output}\nObservation: {observation}\n"

        if answer is None:
            fallback_prompt = REACT_PROMPT_TEMPLATE.format(
                tools=self.tools_md,
                tool_names=self.tool_names,
                history=format_history(history),
                input=question,
                agent_scratchpad=agent_scratchpad.strip()
            ) + "\nFinal Answer:"

            final_resp = self.client.models.generate_content(
                model=self.model_name,
                contents=fallback_prompt,
                config=GenerateContentConfig(stop_sequences=["\n"])
            )
            fallback = final_resp.text.strip()
            answer = fallback.split("Final Answer:")[-1].strip() if "Final Answer:" in fallback else fallback

        history = history + [{"question": question, "answer": answer}]
        return answer, history, agent_scratchpad
