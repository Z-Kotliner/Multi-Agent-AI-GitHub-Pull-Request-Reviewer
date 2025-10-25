from llama_index.core.tools import FunctionTool

from config import get_github_repo


async def get_pr_commit_details(commit_sha):
    """Use this tool to fetch the commit info of a given commit using commit SHA."""

    # Get Commit object
    commit = get_github_repo().get_commit(commit_sha)

    # put everything in a dict
    changed_files: list[dict[str, any]] = []
    for f in commit.files:
        changed_files.append({
            "filename": f.filename,
            "status": f.status,
            "additions": f.additions,
            "deletions": f.deletions,
            "changes": f.changes,
            "patch": f.patch,
        })

    return changed_files


def get_commit_details_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=get_pr_commit_details)
