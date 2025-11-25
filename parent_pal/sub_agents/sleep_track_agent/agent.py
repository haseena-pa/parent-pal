from google.adk.agents.llm_agent import LlmAgent
import os
import logging
from . import prompt
from ...tools.tools import get_current_datetime, toolbox_tools

# Configure logging
logger = logging.getLogger(__name__)

model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

tools = [get_current_datetime]

if toolbox_tools:  # Only add if not empty list
    tools.extend(toolbox_tools)
    logger.info(f"Sleep tracker agent loaded {len(toolbox_tools)} toolbox tools")
else:
    logger.warning("Sleep tracker agent: No toolbox tools available")

sleep_track_agent = LlmAgent(
    model=model_name,
    name='sleep_track_agent',
    description='A supportive assistant for parents to track and manage their baby\'s sleep patterns.',
    instruction=prompt.SLEEP_TRACK_PROMPT,
    tools=tools
)
logger.info(f"Sleep track agent initialized with {len(tools)} tools")