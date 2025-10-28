from llama_index.core.agent import FunctionAgent

from config import get_llm
from tools import get_post_final_review_tool, get_add_final_review_to_state_tool


def get_review_and_post_agent() -> FunctionAgent:
    # Get the tools
    post_final_review_tool = get_post_final_review_tool()
    add_final_review_to_state_tool = get_add_final_review_to_state_tool()

    # Get the llm
    llm = get_llm()

    # Prompt
    prompt = """
        You are the Review and Posting agent. You must handoff to the CommentorAgent to create a review comment. 
        Once a review is generated, you need to run a final check and post it to GitHub.
            - The review must: \n
            - Be a ~200-300 word review in markdown format. \n
            - Specify what is good about the PR: \n
            - Did the author follow ALL contribution rules? What is missing? \n
            - Are there notes on test availability for new functionality? If there are new models, are there migrations for them? \n
            - Are there notes on whether new endpoints were documented? \n
            - Are there suggestions on which lines could be improved upon? Are these lines quoted? \n
         If the review does not meet this criteria, you must ask the CommentorAgent to rewrite and address these concerns. \n
         When you are satisfied, post the review to GitHub.  
           """

    # Create ReActAgent
    review_and_posting_agent = FunctionAgent(
        llm=llm,
        name='ReviewAndPostingAgent',
        description="Uses the comment by the CommentorAgent, check it, request re-write if necessary and post it to GitHub.",
        tools=[post_final_review_tool, add_final_review_to_state_tool],
        system_prompt=prompt,
        can_handoff_to=["CommentorAgent"]
    )

    return review_and_posting_agent
