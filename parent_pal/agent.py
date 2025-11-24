import os
import datetime
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents import ParallelAgent
from google.adk.tools import google_search, AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from toolbox_core import ToolboxSyncClient
from .sub_agents.sleep_track_agent import sleep_track_agent

# --- Configuration ---
model_name = os.environ.get("MODEL_NAME", "gemini-2.5-pro")
google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")

# =============================================================================
# COMPONENT 1: Sleep Tracker Sub-Agent
# =============================================================================

sleep_tracker_tool = AgentTool(agent=sleep_track_agent)


# =============================================================================
# COMPONENT 2: Parenting Info & Location Sub-Agents
# =============================================================================

baby_parenting_knowledge_agent = LlmAgent(
    model=model_name,
    name='baby_parenting_knowledge_agent',
    description='Specialized assistant for baby milestones and general parenting advice.',
    instruction='Find and provide comprehensive knowledge on baby milestones or parenting advice.',
    tools=[google_search]
)

maps_location_assistant = LlmAgent(
    model=model_name,
    name='maps_location_assistant',
    description='Specialized assistant for finding nearby locations.',
    instruction='Find nearby locations or directions related to baby/parenting.',
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='npx',
                    args=["-y", "@modelcontextprotocol/server-google-maps"],
                    env={"GOOGLE_MAPS_API_KEY": google_maps_api_key}
                ),
            ),
        )
    ],
)

# Combine Info and Maps into a Parallel Agent (they run simultaneously)
parallel_search = ParallelAgent(
    name='parallel_knowledge_and_location',
    description='Executes both the baby knowledge and location-finding agents simultaneously.',
    sub_agents=[baby_parenting_knowledge_agent, maps_location_assistant]
)

# Wrap the parallel agent as a tool
info_location_tool = AgentTool(agent=parallel_search)


# =============================================================================
# ROOT AGENT: The Coordinator
# =============================================================================

root_agent = LlmAgent(
    model=model_name,
    name='parent_pal_coordinator',
    description='The main interface for Parent Pal that coordinates sleep tracking and parenting advice.',
    tools=[sleep_tracker_tool, info_location_tool],
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