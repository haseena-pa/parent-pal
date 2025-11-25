import os
import logging
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents import ParallelAgent
from google.adk.tools import AgentTool
from .sub_agents.sleep_track_agent import sleep_track_agent
from .sub_agents.maps_location_agent import maps_location_agent
from .sub_agents.parenting_agent import parenting_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Configuration ---
model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
logger.info(f"Initializing Parent Pal with model: {model_name}")


# =============================================================================
# COMPONENT 1: Sleep Tracker Sub-Agent
# =============================================================================

sleep_tracker_tool = AgentTool(agent=sleep_track_agent)
logger.info("Sleep tracker tool initialized")


# =============================================================================
# COMPONENT 2: Parenting Info & Location Sub-Agents
# =============================================================================

# Combine Parenting info and Maps into a Parallel Agent (they run simultaneously)
parallel_search = ParallelAgent(
    name='parallel_knowledge_and_location',
    description='Executes both the baby knowledge and location-finding agents simultaneously.',
    sub_agents=[parenting_agent, maps_location_agent]
)
logger.info("Parallel agent (parenting + maps) initialized")

# Wrap the parallel agent as a tool
parenting_and_location_tool = AgentTool(agent=parallel_search)


# =============================================================================
# ROOT AGENT: The Coordinator
# =============================================================================

root_agent = LlmAgent(
    model=model_name,
    name='parent_pal_coordinator',
    description='The main interface for Parent Pal that coordinates sleep tracking and parenting advice.',
    tools=[sleep_tracker_tool, parenting_and_location_tool],
    instruction="""
        You are **Parent Pal**, an all-in-one parenting assistant.

        **LOGIC & ROUTING:**

        1. **General Greeting / Chat:**
           - If the user says "Hello" or asks generic questions: Greet them warmly and explain your capabilities (Sleep Tracking & Parenting Advice).
           - **DO NOT** ask for their name or email yet. Keep it casual.

        2. **Parenting Info / Locations:**
           - If the user asks a question (e.g., "Why is baby crying?", "Find a park"): Call the `parallel_knowledge_and_location` tool.
           - Do not ask for identity.

        3. **Sleep Tracking Requests (The Only Time to Identify):**
           - If the user wants to **log sleep**, **check history**, or **manage records**: Call the `sleep_track_agent` tool.
           - **Context Passing:** - If you *already know* the user's Name/Email from previous turns, pass it in the instructions (e.g., "User is Haseena (h@gmail.com)").
             - If you *do not* know their Name/Email, just pass the request. The sub-agent will handle asking for it.
             - **Important:** If the user provides their name/email in response to a request, strictly **remember it** for future calls.
    """
)
logger.info("Root agent (parent_pal_coordinator) initialized successfully")