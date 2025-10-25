from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context


async def add_username_to_state(ctx: Context, username: str) -> str:
    """
    Use this tool for adding the username to the state.
    """
    current_state = await ctx.get("state")
    current_state["username"] = username
    await ctx.set("state", current_state)
    return "State updated with report contexts. "


def get_add_username_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=add_username_to_state)
