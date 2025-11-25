import os
from google.adk.agents.llm_agent import LlmAgent
from ...tools.tools import mcp_tools


model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
tools = [mcp_tools] if mcp_tools is not None else []

maps_location_agent = LlmAgent(
    model=model_name,
    name='maps_location_agent',
    description='Specialized assistant for finding nearby locations.',
    instruction='Find nearby locations or directions related to baby/parenting.',
    tools=tools,
)