from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context


async def add_final_review_to_state(ctx: Context, final_review: str) -> str:
    """
    Use this tool for adding the final review comment to the state.
    """
    current_state = await ctx.store.get("state")
    current_state["final_review_comment"] = final_review
    await ctx.store.set("state", current_state)
    return f"State updated with {final_review} contexts. "


def get_add_final_review_to_state_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=add_final_review_to_state)
