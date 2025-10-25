import warnings

from pydantic.warnings import UnsupportedFieldAttributeWarning, PydanticDeprecationWarning

warnings.filterwarnings("ignore", category=UnsupportedFieldAttributeWarning)
warnings.filterwarnings("ignore", category=PydanticDeprecationWarning)

from agents import get_context_agent

import asyncio
from llama_index.core.agent.workflow import AgentOutput, ToolCallResult
from llama_index.core.workflow import Context
from llama_index.core.prompts import RichPromptTemplate

# Recipe API GitHub repo url
repo_url = "https://github.com/Z-Kotliner/recipe-api.git"

async def main():
    # Accept user question
    query = input().strip()
    prompt = RichPromptTemplate(query)

    # Get the context agent
    agent = get_context_agent()
    context = Context(agent)

    # Run the agent
    handler = agent.run(prompt.format(), ctx=context)

    # Stream output
    current_agent = None
    async for event in handler.stream_events():
        if hasattr(event, "current_agent_name") and event.current_agent_name != current_agent:
            current_agent = event.current_agent_name
            print(f"Current agent: {current_agent}")
        elif isinstance(event, AgentOutput):
            if event.response.content:
                print(event.response.content)
        elif isinstance(event, ToolCallResult):
            print(f"Output from tool: {event.tool_output}")


if __name__ == "__main__":
    asyncio.run(main())
