# CrisisOpsEnv

CrisisOpsEnv is a real-world OpenEnv-compatible environment where an AI agent coordinates emergency response operations across incidents, responders, hospitals, and road disruptions.

## Features
- Real-world emergency dispatch simulation
- Typed action / state models
- Standard step() / reset() / state() APIs
- 3 benchmark tasks (easy, medium, hard)
- Partial progress reward function
- Baseline inference script using OpenAI client
- Docker + Hugging Face Spaces ready

## Tasks
### 1. easy_dispatch
Handle one medical emergency correctly.

### 2. medium_priority
Prioritize multiple incidents with limited responders.

### 3. hard_surge
Manage a citywide emergency surge with blocked roads and limited capacity.

## Action Space
- dispatch_responder
- reserve_hospital
- reroute
- mark_resolved
- wait

## Observation Space
The environment state includes:
- active incidents
- responders
- hospitals
- blocked roads
- time
- completion status

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7860