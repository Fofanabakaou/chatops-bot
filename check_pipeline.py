import httpx

URL = "https://api.github.com/repos/Fofanabakaou/chatops-bot/actions/runs"

response = httpx.get(URL)
data = response.json()

for run in data["workflow_runs"]:
    print(run["run_number"], run["display_title"], run["status"], run["conclusion"])
