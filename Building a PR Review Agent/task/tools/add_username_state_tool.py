from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context


async def add_username_to_state(ctx: Context, user_name: str) -> str:
    """
    Use this tool for adding the draft comment to the state.
    """
    current_state = await ctx.store.get("state")
    current_state["key"] = user_name
    await ctx.store.set("state", current_state)
    return f"State updated with {user_name} contexts. "


def get_add_username_to_state_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=add_username_to_state)
