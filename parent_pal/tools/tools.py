from datetime import datetime
import os

from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ----- Function tool -----
def get_current_datetime():
    """
    Retrieves the current real-time date and time. 
    Useful for resolving relative time references like 'today', 'now', or 'yesterday'.
    """
    return datetime.now().strftime("%A, %B %d, %Y, %H:%M:%S")


# ----- Google Cloud Tool (MCP Toolbox for Databases) -----
TOOLBOX_URL = os.getenv("MCP_TOOLBOX_URL", "http://127.0.0.1:5000")

# Initialize Toolbox client and load tools
# If the toolbox server is not available (e.g., in CI), set to empty list
try:
    toolbox = ToolboxSyncClient(TOOLBOX_URL)
    toolbox_tools = toolbox.load_toolset("sleep_tracking_toolset")
except Exception:
    # Toolbox server not available, set to empty list
    toolbox_tools = []


# ----- MCP Tool -----
# If Google map api key is not available (e.g., in CI), set to None
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
if google_maps_api_key:
    try:
        mcp_tools = MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params = StdioServerParameters(
                        command='npx',
                        args=["-y", "@modelcontextprotocol/server-google-maps"],
                        env={"GOOGLE_MAPS_API_KEY": google_maps_api_key}
                    ),
                ),
            )
    except Exception:
        # GitHub MCP server not available or token missing
        mcp_tools = None
else:
    # Google Maps API key not set
    mcp_tools = None