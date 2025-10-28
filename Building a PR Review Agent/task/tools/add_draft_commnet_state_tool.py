from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context


async def add_comment_to_state(ctx: Context, draft_comment: str) -> str:
    """
    Use this tool for adding the review comment to the state.
    """
    current_state = await ctx.store.get("state")
    current_state["review_comment"] = draft_comment
    await ctx.store.set("state", current_state)
    return f"State updated with {draft_comment} contexts. "


def get_add_comment_to_state_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=add_comment_to_state)
