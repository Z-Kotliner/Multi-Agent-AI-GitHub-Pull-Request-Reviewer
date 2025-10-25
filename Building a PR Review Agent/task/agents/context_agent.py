from llama_index.core.agent import ReActAgent

from tools import get_file_contents_tool, get_pr_details_tool, get_commit_details_tool, get_add_username_tool
from config import get_llm


def get_context_agent() -> ReActAgent:
    # Get the tools
    pr_details_tool = get_pr_details_tool()
    commit_details_tool = get_commit_details_tool()
    file_contents_tool = get_file_contents_tool()
    add_username_tool = get_add_username_tool()

    # Get the llm
    llm = get_llm()

    # Prompt
    prompt = """
    You are the context gathering agent from GITHUB. When gathering context, you MUST gather \n: 
    - The details: author, title, body, diff_url, state, and head_sha; \n
    - Changed files; \n
    - Any requested for files; \n]
    
    You have access to the following tools:
    1. get_pr_info - to get pull request information  \n
    2. get_commit_info - to get commit information  \n
    3. get_file_contents - to get file contents  \n
    
    Use the tools provided when answering questions.
    """

    # Create ReActAgent
    context_agent = ReActAgent(
        llm=llm,
        name='ContextAgent',
        tools=[pr_details_tool, commit_details_tool, file_contents_tool, add_username_tool],
        system_prompt=prompt
    )

    return context_agent
