from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search, AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os
from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.sessions import InMemorySessionService

model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

baby_parenting_knowledge_agent = LlmAgent(
    model=model_name,
    name='baby_parenting_knowledge_agent',
    description='Specialized assistant for user questions related ONLY to baby milestones and general parenting advice.',
    instruction='Find and provide comprehensive knowledge on baby milestones or parenting advice.',
    tools=[google_search]
)

google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")

maps_location_assistant = LlmAgent(
    model=model_name,
    name='maps_location_assistant',
    description='Specialized assistant for finding nearby locations related to babies and parenting.',
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


parallel_search = ParallelAgent(
    name='parallel_knowledge_and_location',
    description='Executes both the baby knowledge and location-finding agents simultaneously.',
    sub_agents=[
        baby_parenting_knowledge_agent, 
        maps_location_assistant
    ] 
)

parallel_search_tool = AgentTool(agent=parallel_search)

summary_agent = LlmAgent(
    model=model_name,
    name='summary_agent',
    description='Coordinator that handles greetings or fetches data for specific requests.',
    tools=[parallel_search_tool], # The parallel agent wrapped as a tool
    instruction="""
        You are a helpful parenting assistant capable of providing advice and finding local resources simultaneously.

        **Logic Flow:**
        1. **Greetings:** If the user says "hello", "hi", or introduces themselves:
           - Do NOT call any tools.
           - Reply warmly.
           - Explain your capabilities: "I can answer questions about baby milestones and parenting advice while simultaneously finding relevant nearby locations (like parks, pediatricians, or stores) for you."
        
        2. **Requests:** If the user asks a question or makes a request (e.g., "Where can I buy diapers?" or "Why is my baby crying?"):
           - Call the `parallel_knowledge_and_location` tool to gather data.
           - Synthesize the tool outputs into a single, helpful response.
    """
)
root_agent = summary_agent