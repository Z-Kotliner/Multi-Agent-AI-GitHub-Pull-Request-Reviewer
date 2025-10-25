import os
import re
import sys

import dotenv
from github import Github
from github import GithubException
from hstest import StageTest, CheckResult, dynamic_test

dotenv.load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import repo_url


class AgentTest(StageTest):
    g = Github(os.getenv("GITHUB_TOKEN")) if os.getenv("GITHUB_TOKEN") else Github()
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    username = repo_url.split('/')[-2]
    full_repo_name = f"{username}/{repo_name}"
    repo = g.get_repo(full_repo_name)

    @dynamic_test
    def check_url_set(self):
        if repo_url == "":
            return CheckResult.wrong("The URL in main.py is not set.")
        pattern = r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git$"
        if not re.match(pattern, repo_url):
            return CheckResult.wrong(
                "Your `repo_url` must be of the form "
                "`https://github.com/username/repo.git`."
            )
        if self.g is None:
            return CheckResult.wrong("Please add the GitHub PAT you created in your .env file. ")
        return CheckResult.correct()

    @dynamic_test(time_limit=0)
    def check_repo(self):

        try:
            repo = self.g.get_repo(self.full_repo_name)
            if repo.private:
                return CheckResult.wrong("The repository is private. Make sure it's public.")

            expected_files = {"README.md", ".gitignore", "app/models.py", "app/tests/test_views.py",
                              "pyproject.toml", "CONTRIBUTING.md", "app/views.py", "recipes/settings.py",
                              ".github/workflows/ci.yml", "manage.py"}

            repo_contents = set()

            def check_directory_contents(contents_url, path=""):
                contents = repo.get_contents(path)
                for content in contents:
                    if content.type == "dir":
                        check_directory_contents(contents_url, content.path)
                    else:
                        repo_contents.add(content.path)

            check_directory_contents(repo.get_contents(""))

            missing_files = expected_files - repo_contents
            if missing_files:
                missing_files_str = ', '.join(missing_files)
                return CheckResult.wrong(f"The repository is missing the following expected file(s): {missing_files_str}")

            pull_requests = repo.get_pulls(state="open", sort="created")

            if pull_requests.totalCount == 0:
                return CheckResult.wrong("No open pull requests found — please open one with the specified changes "
                                         "to app/models.py and app/serializers.py in a new branch. ")

            latest_pull = pull_requests[0]
            modified_files = [f.filename for f in latest_pull.get_files()]
            required = {"app/serializers.py", "app/models.py"}
            present = set(modified_files)
            missing_required = required - present
            if missing_required:
                missing_str = ', '.join(missing_required)
                return CheckResult.wrong(f"The PR must modify the following files: {missing_str}. Found: {modified_files}")

            pr_number = latest_pull.number
            pr = self.repo.get_pull(pr_number)

            comments = pr.get_issue_comments()

            if comments.totalCount == 0:
                return CheckResult.wrong("Test results from workflow not found. Ensure that you didn't modify and that you committed the .github/workflows/ci.yml file.")
            found = any(comment.user.login == "github-actions[bot]" for comment in comments)
            if not found:
                return CheckResult.wrong("There should be at least one issue comment created when you opened a new PR containing the test results.")

            return CheckResult.correct()

        except GithubException as e:
            if e.status == 404:
                return CheckResult.wrong("The repository does not exist or is private.")
            if e.status == 403:
                return CheckResult.wrong(f"Encountered a resource denied error: {e.data.get('message', 'No error message')}" )
            else:
                return CheckResult.wrong(f"An error occurred while accessing the repository: {e.data.get('message', 'No error message')}")
        except Exception as e:
            return CheckResult.wrong(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    AgentTest().run_tests()
    