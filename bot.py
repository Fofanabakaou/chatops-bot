import httpx

URL = "https://api.github.com/repos/Fofanabakaou/chatops-bot/actions/runs"

STEP_HELP = {
    "Run actions/checkout@v4": "télécharge le code du projet",
    "Run actions/setup-python@v5": "installe Python",
    "Run pip install -r requirements.txt": "installe les outils du projet",
    "Run pytest": "lance les tests",
}


def get_runs():
    response = httpx.get(URL)
    return response.json()["workflow_runs"]


def get_last_run():
    return get_runs()[0]


def get_last_failed_run():
    for run in get_runs():
        if run["conclusion"] == "failure":
            return run
    return None


def get_failed_step(run):
    response = httpx.get(run["jobs_url"])
    for job in response.json()["jobs"]:
        for step in job["steps"]:
            if step["conclusion"] == "failure":
                return step["name"]
    return None


def describe(run):
    if run["status"] != "completed":
        return f"Le pipeline est en cours ({run['status']})."
    if run["conclusion"] == "success":
        return f"Le dernier pipeline ('{run['display_title']}') a réussi."
    return f"Le dernier pipeline ('{run['display_title']}') a échoué."


def explain_failure():
    run = get_last_failed_run()
    if run is None:
        return "Aucun pipeline n'a échoué."
    step = get_failed_step(run)
    return f"Le dernier échec est '{run['display_title']}' : l'étape '{step}' a échoué."


def explain_steps():
    run = get_last_run()
    response = httpx.get(run["jobs_url"])
    lines = []
    for job in response.json()["jobs"]:
        for step in job["steps"]:
            if step["name"] in STEP_HELP:
                lines.append(f"- {step['name']} : {STEP_HELP[step['name']]}")
    return "Voici les étapes du pipeline :\n" + "\n".join(lines)


def answer(question):
    question = question.lower()
    if "statut" in question or "status" in question:
        return describe(get_last_run())
    if "pourquoi" in question or "erreur" in question or "échou" in question or "echou" in question:
        return explain_failure()
    if "étape" in question or "etape" in question or "explique" in question:
        return explain_steps()
    return "Je ne comprends pas encore cette question."


if __name__ == "__main__":
    while True:
        question = input("Toi > ")
        if question == "quit":
            break
        print("Bot >", answer(question))
