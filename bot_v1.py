import httpx

URL = "https://api.github.com/repos/Fofanabakaou/chatops-bot/actions/runs"


def get_last_run():
    response = httpx.get(URL)
    data = response.json()
    return data["workflow_runs"][0]


def describe(run):
    if run["status"] != "completed":
        return f"Le pipeline est en cours ({run['status']})."
    if run["conclusion"] == "success":
        return f"Le dernier pipeline ('{run['display_title']}') a réussi."
    return f"Le dernier pipeline ('{run['display_title']}') a échoué."


def answer(question):
    question = question.lower()
    if "statut" in question or "status" in question:
        return describe(get_last_run())
    return "Je ne comprends pas encore cette question."


while True:
    question = input("Toi > ")
    if question == "quit":
        break
    print("Bot >", answer(question))
