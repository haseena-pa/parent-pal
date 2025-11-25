from datetime import datetime
import os
import logging

from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


# ----- Function tool -----
def get_current_datetime():
    """
    Retrieves the current real-time date and time.
    Useful for resolving relative time references like 'today', 'now', or 'yesterday'.
    """
    current_time = datetime.now().strftime("%A, %B %d, %Y, %H:%M:%S")
    logger.debug(f"get_current_datetime called: {current_time}")
    return current_time


# ----- Google Cloud Tool (MCP Toolbox for Databases) -----
TOOLBOX_URL = os.getenv("MCP_TOOLBOX_URL", "http://127.0.0.1:5000")

# Initialize Toolbox client and load tools
# If the toolbox server is not available (e.g., in CI), set to empty list
try:
    logger.info(f"Connecting to Toolbox at {TOOLBOX_URL}")
    toolbox = ToolboxSyncClient(TOOLBOX_URL)
    toolbox_tools = toolbox.load_toolset("sleep_tracking_toolset")
    logger.info(f"Successfully loaded {len(toolbox_tools)} tools from sleep_tracking_toolset")
except Exception as e:
    # Toolbox server not available, set to empty list
    logger.warning(f"Failed to connect to Toolbox server: {e}")
    toolbox_tools = []


# ----- MCP Tool -----
# If Google map api key is not available (e.g., in CI), set to None
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
if google_maps_api_key:
    try:
        logger.info("Initializing Google Maps MCP toolset")
        mcp_tools = MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params = StdioServerParameters(
                        command='npx',
                        args=["-y", "@modelcontextprotocol/server-google-maps"],
                        env={"GOOGLE_MAPS_API_KEY": google_maps_api_key}
                    ),
                ),
            )
        logger.info("Google Maps MCP toolset initialized successfully")
    except Exception as e:
        # GitHub MCP server not available or token missing
        logger.error(f"Failed to initialize Google Maps MCP toolset: {e}")
        mcp_tools = None
else:
    # Google Maps API key not set
    logger.warning("Google Maps API key not set, MCP tools will not be available")
    mcp_tools = None