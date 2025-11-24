from google.adk.agents.llm_agent import Agent
from toolbox_core import ToolboxSyncClient
import datetime
from . import prompt

# --- 1. Define the Tool Locally ---
def get_current_datetime():
    """
    Retrieves the current real-time date and time. 
    Useful for resolving relative time references like 'today', 'now', or 'yesterday'.
    """
    return datetime.datetime.now().strftime("%A, %B %d, %Y, %H:%M:%S")

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# --- 2. Load and Append Tools ---
remote_tools = toolbox.load_toolset("sleep_tracking_toolset")
all_tools = remote_tools + [get_current_datetime]

sleep_track_agent = Agent(
    model='gemini-2.5-pro',
    name='sleep_track_agent',
    description='A supportive assistant for parents to track and manage their baby\'s sleep patterns.',
    instruction=prompt.SLEEP_TRACK_PROMPT,
    tools=all_tools 
)