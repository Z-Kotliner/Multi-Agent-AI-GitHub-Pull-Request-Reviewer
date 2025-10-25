from llama_index.core.tools import FunctionTool

from config import get_github_repo


async def get_pr_details(pr_number: int):
    """Use this tool to fetch the pull request(PR) info with given pull request(PR) number.
      i.e Given a pull request number, get the pull request details.
    """

    # Get PullRequest object
    pull_request = get_github_repo().get_pull(pr_number)

    # put everything in a dict
    pr_details = {
        'author': pull_request.user.login,
        'title': pull_request.title,
        'body': pull_request.body,
        'diff_url': pull_request.diff_url,
        'state': pull_request.state
    }

    # Get commit SHAs
    commit_shas = []
    commits = pull_request.get_commits()

    for c in commits:
        commit_shas.append(c.sha)

    pr_details['commit_sha'] = commit_shas

    return pr_details


def get_pr_details_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=get_pr_details)
