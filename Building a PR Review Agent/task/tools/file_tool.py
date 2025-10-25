from llama_index.core.tools import FunctionTool

from config import get_github_repo


async def get_file_contents(file_path: str):
    """Use this tool to fetch the contents of a file from a repository."""

    # Get ContentFile object
    file_content = get_github_repo().get_contents(file_path)

    return file_content.decoded_content.decode("utf-8")


def get_file_contents_tool() -> FunctionTool:
    return FunctionTool.from_defaults(fn=get_file_contents)
