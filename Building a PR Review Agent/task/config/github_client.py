import os

import dotenv

from github import Github, Auth
from github.GithubException import GithubException
from .logging_config import setup_logger

# Load env variables
dotenv.load_dotenv()

# Get evn variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')

# Set up logger
logger = setup_logger("app", "DEBUG")


# Get GitHub Repository object
def get_github_repo():
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN not set")
    if not GITHUB_REPO:
        raise ValueError("GITHUB_REPO not set")

    try:
        github_client = Github(auth=Auth.Token(GITHUB_TOKEN))
        github_repo = github_client.get_repo(GITHUB_REPO)
        return github_repo
    except GithubException as error:
        logger.error("Error=%s", error)
        raise error
