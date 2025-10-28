from llama_index.core.agent import FunctionAgent

from config import get_llm
from tools import get_add_comment_to_state_tool


def get_commentator_agent() -> FunctionAgent:
    # Get the tools
    add_data_to_state_tool = get_add_comment_to_state_tool()

    # Get the llm
    llm = get_llm()

    # Prompt
    prompt = """
        You are the commentor agent that writes review comments for pull requests as a human reviewer would. \n 
        Ensure to do the following for a thorough review: 
            - Request for the PR details, changed files, and any other repo files you may need from the ContextAgent. 
            - Once you have asked for all the needed information, write a good ~200-300 word review in markdown format detailing: \n
            - What is good about the PR? \n
            - Did the author follow ALL contribution rules? What is missing? \n
            - Are there tests for new functionality? If there are new models, are there migrations for them? - use the diff to determine this. \n
            - Are new endpoints documented? - use the diff to determine this. \n 
            - Which lines could be improved upon? Quote these lines and offer suggestions the author could implement. \n
            - If you need any additional details, you must hand off to the ContextAgent. \n
            - You should directly address the author. So your comments should sound like: \n      
            "Thanks for fixing this. I think all places where we call quote should be fixed. Can you roll this fix out everywhere?"
         You must hand off to the ReviewAndPostingAgent once you are done drafting a review comment. \n
        """

    # Create ReActAgent
    commentor_agent = FunctionAgent(
        llm=llm,
        name='CommentorAgent',
        description="Uses the context gathered by the context agent to draft a pull request review comment .",
        tools=[add_data_to_state_tool],
        system_prompt=prompt,
        can_handoff_to=["ContextAgent", "ReviewAndPostingAgent"]
    )

    return commentor_agent
