from google.adk.agents.llm_agent import LlmAgent
import os
from . import prompt
from ...tools.tools import get_current_datetime, toolbox_tools

model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

tools = [get_current_datetime]

if toolbox_tools:  # Only add if not empty list
    tools.extend(toolbox_tools)

sleep_track_agent = LlmAgent(
    model=model_name,
    name='sleep_track_agent',
    description='A supportive assistant for parents to track and manage their baby\'s sleep patterns.',
    instruction=prompt.SLEEP_TRACK_PROMPT,
    tools=tools
)