import os
import logging
from google.adk.agents.llm_agent import LlmAgent
from ...tools.tools import mcp_tools

# Configure logging
logger = logging.getLogger(__name__)


model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
tools = [mcp_tools] if mcp_tools is not None else []

if mcp_tools:
    logger.info("Maps location agent: Google Maps MCP tools loaded")
else:
    logger.warning("Maps location agent: No MCP tools available (Google Maps API key may be missing)")

maps_location_agent = LlmAgent(
    model=model_name,
    name='maps_location_agent',
    description='Specialized assistant for finding nearby locations.',
    instruction='Find nearby locations or directions related to baby/parenting.',
    tools=tools,
)
logger.info(f"Maps location agent initialized with {len(tools)} tools")