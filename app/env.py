from copy import deepcopy
from app.models import EnvState, ActionInput, StepResponse
from app.tasks import TASKS
from app.graders import grade_task

RESPONDER_MAP = {
    "medical": "ambulance",
    "fire": "fire_truck",
    "police": "police_unit"
}

class CrisisOpsEnv:
    def __init__(self):
        self.state_data = None

    def reset(self, task_id: str) -> EnvState:
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id: {task_id}")

        task = TASKS[task_id]
        self.state_data = EnvState(
            task_id=task_id,
            time=0,
            incidents=deepcopy(task["incidents"]),
            responders=deepcopy(task["responders"]),
            hospitals=deepcopy(task["hospitals"]),
            blocked_roads=deepcopy(task["blocked_roads"]),
            steps_taken=0,
            done=False
        )
        return self.state_data

    def state(self) -> EnvState:
        return self.state_data

    def step(self, action: ActionInput) -> StepResponse:
        if self.state_data.done:
            return StepResponse(
                reward=grade_task(self.state_data),
                done=True,
                message="Episode already finished.",
                state=self.state_data
            )

        reward = 0.0
        message = "No-op"

        incidents = {i.id: i for i in self.state_data.incidents}
        responders = {r.id: r for r in self.state_data.responders}
        hospitals = {h.id: h for h in self.state_data.hospitals}

        if action.action_type == "dispatch_responder":
            if action.incident_id in incidents and action.responder_id in responders:
                inc = incidents[action.incident_id]
                res = responders[action.responder_id]

                if res.available:
                    expected = RESPONDER_MAP[inc.type]
                    if res.type == expected:
                        inc.status = "assigned"
                        res.available = False
                        reward += 0.3
                        message = f"{res.id} assigned to {inc.id}"
                    else:
                        reward -= 0.2
                        message = "Wrong responder type"
                else:
                    reward -= 0.1
                    message = "Responder unavailable"

        elif action.action_type == "reserve_hospital":
            if action.hospital_id in hospitals and action.incident_id in incidents:
                inc = incidents[action.incident_id]
                hosp = hospitals[action.hospital_id]
                if inc.type == "medical" and hosp.beds_available > 0:
                    hosp.beds_available -= 1
                    reward += 0.2
                    message = f"Reserved {hosp.id} for {inc.id}"
                else:
                    reward -= 0.1
                    message = "Hospital reservation invalid"

        elif action.action_type == "mark_resolved":
            if action.incident_id in incidents:
                inc = incidents[action.incident_id]
                if inc.status == "assigned":
                    inc.status = "resolved"
                    reward += 0.4
                    message = f"{inc.id} resolved"
                else:
                    reward -= 0.1
                    message = "Incident not yet assigned"

        elif action.action_type == "reroute":
            reward += 0.1
            message = "Reroute acknowledged"

        elif action.action_type == "wait":
            reward -= 0.05
            message = "Waiting wastes time"

        # Time penalty
        self.state_data.time += 1
        self.state_data.steps_taken += 1

        unresolved_critical = sum(
            1 for i in self.state_data.incidents
            if i.status != "resolved" and i.severity == "critical"
        )
        reward -= unresolved_critical * 0.1

        # Done condition
        if all(i.status == "resolved" for i in self.state_data.incidents) or self.state_data.steps_taken >= 12:
            self.state_data.done = True

        final_score = max(0.0, min(1.0, reward))

        return StepResponse(
            reward=round(final_score, 3),
            done=self.state_data.done,
            message=message,
            state=self.state_data
        )