import requests
import time

USERNAME = "your_dockerhub_username"
PAT = "your_personal_access_token_here"  # the Docker Hub PAT

# Authenticate
auth_url = "https://hub.docker.com/v2/users/login/"
auth_data = {"username": USERNAME, "password": PAT}
r = requests.post(auth_url, json=auth_data)

if r.status_code != 200:
    print("Login failed:", r.status_code, r.text)
    exit()

token = r.json().get("token")
headers = {"Authorization": f"JWT {token}"}

# Get repos
repos_url = f"https://hub.docker.com/v2/repositories/{USERNAME}/?page_size=100"
repos = []

while repos_url:
    r = requests.get(repos_url, headers=headers)
    data = r.json()
    if "results" not in data:
        break
    repos.extend([repo["name"] for repo in data["results"]])
    repos_url = data.get("next")

print(f"Found {len(repos)} repositories.")

# Delete repos
for repo_name in repos:
    del_url = f"https://hub.docker.com/v2/repositories/{USERNAME}/{repo_name}/"
    r = requests.delete(del_url, headers=headers)

    if r.status_code == 204:
        print(f"Deleted {repo_name} immediately.")
    elif r.status_code in (202, 200):
        print(f"Deletion of {repo_name} is in progress...")
        # Poll until deleted
        while True:
            check = requests.get(del_url, headers=headers)
            if check.status_code == 404:
                print(f"{repo_name} finally deleted.")
                break
            time.sleep(2)  # Wait 2 seconds before retrying
    else:
        print(f"Failed to delete {repo_name}: {r.status_code} {r.text}")
