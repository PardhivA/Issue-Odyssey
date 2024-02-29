repo_owner = "shosetsuorg"
repo_name = "shosetsu"
auth_key = "YOUR KEY HERE"
#GITHUB FTW
import requests
import json
import os


def get_all_items(auth_key, url, item_type, per_page=100):
    """
    Fetches all items from a paginated GitHub API endpoint, handling pagination
    and authentication.

    Args:
        auth_key (str): GitHub API authentication token.
        url (str): URL of the API endpoint.
        item_type (str): Type of items to fetch (e.g., "commits", "issues").
        per_page (int, optional): Number of items to fetch per page. Defaults to 100.

    Returns:
        list: List of all fetched items.
    """

    items = []
    page = 1
    while True:
        headers = {"Authorization": f"Bearer {auth_key}"}
        params = {"page": page, "per_page": per_page}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()

        if not data:
            break
        else :
            print(f"Fetched {len(data)} {item_type} from page {page}")
        items.extend(data)
        page += 1

    return items


def get_all_commits_and_issues(auth_key, repo_owner, repo_name):
    """
    Fetches all commits and issues from a GitHub repository, saving them to JSON files.

    Args:
        auth_key (str): GitHub API authentication token.
        repo_owner (str): Owner of the repository.
        repo_name (str): Name of the repository.
    """

    commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    issues_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"

    commits = get_all_items(auth_key, commits_url, "commits")
    issues = get_all_items(auth_key, issues_url, "issues")
    os.mkdir("data")
    with open("./data/commits.json", "w") as file:
        json.dump(commits, file, indent=4)  # Add indentation for readability

    with open("./data/issues.json", "w") as file:
        json.dump(issues, file, indent=4)


if __name__ == "__main__":
    get_all_commits_and_issues(auth_key, repo_owner, repo_name)

    print("Commits and issues saved to JSON files successfully!")
