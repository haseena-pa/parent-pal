from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins.logging_plugin import LoggingPlugin
from .agent import root_agent

logging_plugin = LoggingPlugin()

runner = Runner(
    agent=root_agent,
    app_name="baby_sleep_tracker",
    session_service=InMemorySessionService(),
    plugins=[logging_plugin]
)

# Expose the runner and agent for the ADK CLI
__all__ = ["runner", "root_agent"]