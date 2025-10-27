import warnings

from pydantic.warnings import UnsupportedFieldAttributeWarning, PydanticDeprecationWarning

warnings.filterwarnings("ignore", category=UnsupportedFieldAttributeWarning)
warnings.filterwarnings("ignore", category=PydanticDeprecationWarning)

from workflow import get_workflow_agent

import asyncio
from llama_index.core.agent import AgentOutput, ToolCallResult, ToolCall
from llama_index.core.prompts import RichPromptTemplate
from llama_index.core.workflow import Context

# Recipe API GitHub repo url
repo_url = "https://github.com/Z-Kotliner/recipe-api.git"


async def main():
    # Accept user question
    query = input().strip()
    prompt = RichPromptTemplate(query)

    # Get the workflow agent
    workflow_agent = get_workflow_agent()

    # Get the context
    context = Context(workflow_agent)

    # Run the agent
    handler = workflow_agent.run(prompt.format(), ctx=context)

    # Stream the output
    current_agent = None
    async for event in handler.stream_events():
        if hasattr(event, "current_agent_name") and event.current_agent_name != current_agent:
            current_agent = event.current_agent_name
            print(f"Current agent: {current_agent}")
        elif isinstance(event, AgentOutput):
            if event.response.content:
                print("\\n\\nFinal response:", event.response.content)
            if event.tool_calls:
                print("Selected tools: ", [call.tool_name for call in event.tool_calls])
        elif isinstance(event, ToolCallResult):
            print(f"Output from tool: {event.tool_output}")
        elif isinstance(event, ToolCall):
            print(f"Calling selected tool: {event.tool_name}, with arguments: {event.tool_kwargs}")


if __name__ == "__main__":
    asyncio.run(main())
