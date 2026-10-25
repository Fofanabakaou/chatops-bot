import httpx

URL = "https://api.github.com/repos/Fofanabakaou/chatops-bot/actions/runs"

STEP_HELP = {
    "Run actions/checkout@v4": "скачивает код проекта",
    "Run actions/setup-python@v5": "устанавливает Python",
    "Run pip install -r requirements.txt": "устанавливает нужные библиотеки",
    "Run pytest": "запускает тесты",
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
        return f"Пайплайн сейчас работает ({run['status']})."
    if run["conclusion"] == "success":
        return f"Последний пайплайн ('{run['display_title']}') прошёл успешно."
    return f"Последний пайплайн ('{run['display_title']}') завершился с ошибкой."

def explain_failure():
    run = get_last_failed_run()
    if run is None:
        return "Ошибок пока не было."
    step = get_failed_step(run)
    return f"Последняя ошибка: '{run['display_title']}'. Не прошёл шаг '{step}'."

def explain_steps():
    run = get_last_run()
    response = httpx.get(run["jobs_url"])
    lines = []
    for job in response.json()["jobs"]:
        for step in job["steps"]:
            if step["name"] in STEP_HELP:
                lines.append(f"- {step['name']} : {STEP_HELP[step['name']]}")
    return "Шаги пайплайна:\n" + "\n".join(lines)

def answer(question):
    question = question.lower()
    if "статус" in question or "statut" in question or "status" in question:
        return describe(get_last_run())
    if ("почему" in question or "ошибк" in question or "pourquoi" in question
            or "erreur" in question or "échou" in question or "echou" in question):
        return explain_failure()
    if ("шаг" in question or "этап" in question or "объясни" in question
            or "étape" in question or "etape" in question or "explique" in question):
        return explain_steps()
    return "Я пока не понимаю этот вопрос."

if __name__ == "__main__":
    while True:
        question = input("Ты > ")
        if question == "quit":
            break
        print("Бот >", answer(question))
