import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

TASKS = ["easy_dispatch", "medium_priority", "hard_surge"]


def choose_action(state):
    prompt = f"""
You are an emergency response agent.

Choose the next best action in STRICT JSON format.

Allowed actions:
- dispatch_responder
- reserve_hospital
- mark_resolved
- reroute
- wait

State:
{json.dumps(state, indent=2)}

Respond ONLY with JSON.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()
        return json.loads(text)

    except Exception:
        return {"action_type": "wait"}


def run_task(task_id):
    print(f"[START] task={task_id}")

    reset = requests.post(f"{ENV_URL}/reset", params={"task_id": task_id})
    state = reset.json()

    done = False
    step = 0
    total_reward = 0.0

    while not done and step < 12:
        action = choose_action(state)

        try:
            res = requests.post(f"{ENV_URL}/step", json=action)
            data = res.json()
        except Exception:
            data = {"reward": 0.0, "done": True, "state": state}

        reward = data.get("reward", 0.0)
        done = data.get("done", True)
        state = data.get("state", state)

        total_reward += reward

        print(f"[STEP] task={task_id} step={step} action={action} reward={reward} done={done}")

        step += 1

    print(f"[END] task={task_id} total_reward={round(total_reward,3)}")


if __name__ == "__main__":
    for task in TASKS:
        run_task(task)