from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search
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

summary_agent = LlmAgent(
    model=model_name,
    name='summary_agent',
    description='Synthesizes the parallel search results into a single, cohesive response for the user.',
    instruction="""
        You have received results from a knowledge agent and a location agent. 
        Combine these two pieces of information into a single, cohesive, and easy-to-read response for the user. 
        If one agent provided a helpful result and the other did not (e.g., location was not requested), focus on the helpful result.
    """,
    tools=[]
)


root_agent = SequentialAgent(
    name="ParentingWorkflow",
    description="Orchestrates the parenting request process by first fetching knowledge and location concurrently, then summarizing the details.",
    sub_agents=[
        parallel_search,
        summary_agent
    ]
)