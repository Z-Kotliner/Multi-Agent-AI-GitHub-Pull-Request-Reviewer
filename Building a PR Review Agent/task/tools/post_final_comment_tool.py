from llama_index.core.tools import FunctionTool

from config import get_github_repo


async def post_final_review_tool(pr_number: int, comment_text: str):
    """Use this tool to post the final Pull request review comment to GitHub."""

    # Get PullRequest object
    pull_request = get_github_repo().get_pull(pr_number)

    # Post the comment on the PR
    pr_review = pull_request.create_review(body=comment_text)

    return pr_review


def get_post_final_review_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=post_final_review_tool)
