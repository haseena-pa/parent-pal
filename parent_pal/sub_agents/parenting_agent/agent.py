import os
import logging
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

# Configure logging
logger = logging.getLogger(__name__)

model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

parenting_agent = LlmAgent(
    model=model_name,
    name='parenting_agent',
    description='Specialized assistant for baby milestones and general parenting advice.',
    instruction='Find and provide comprehensive knowledge on baby milestones or parenting advice.',
    tools=[google_search]
)
logger.info("Parenting agent initialized with Google Search")