from llama_index.core.agent import FunctionAgent

from tools import get_file_contents_tool, get_pr_details_tool, get_commit_details_tool, get_add_username_to_state_tool
from config import get_llm


def get_context_agent() -> FunctionAgent:
    # Get the tools
    pr_details_tool = get_pr_details_tool()
    commit_details_tool = get_commit_details_tool()
    file_contents_tool = get_file_contents_tool()
    add_state_tool = get_add_username_to_state_tool()

    # Get the llm
    llm = get_llm()

    # Prompt
    prompt = """
        You are the context gathering agent. When gathering context, you MUST gather \n: 
        - The details: author, title, body, diff_url, state, and head_sha; \n
        - Changed files; \n
        - Any requested for files; \n
        Once you gather the requested info, you MUST hand control back to the Commentor Agent. 
    """

    # Create FunctionAgent
    context_agent = FunctionAgent(
        llm=llm,
        name='ContextAgent',
        description="Gathers all the needed context information",
        tools=[pr_details_tool, commit_details_tool, file_contents_tool, add_state_tool],
        system_prompt=prompt,
        can_handoff_to=["CommentorAgent"],
    )

    return context_agent
