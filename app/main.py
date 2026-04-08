from fastapi import FastAPI
from app.env import CrisisOpsEnv
from app.models import ActionInput

app = FastAPI(title="CrisisOpsEnv")

env = CrisisOpsEnv()

@app.get("/")
def root():
    return {"message": "CrisisOpsEnv is running"}

@app.post("/reset")
def reset(task_id: str):
    return env.reset(task_id)

@app.get("/state")
def state():
    return env.state()

@app.post("/step")
def step(action: ActionInput):
    return env.step(action)

@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            "easy_dispatch",
            "medium_priority",
            "hard_surge"
        ]
    }