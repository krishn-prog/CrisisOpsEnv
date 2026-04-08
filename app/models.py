from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class Incident(BaseModel):
    id: str
    type: Literal["medical", "fire", "police"]
    severity: Literal["low", "medium", "high", "critical"]
    zone: str
    status: Literal["pending", "assigned", "resolved"] = "pending"


class Responder(BaseModel):
    id: str
    type: Literal["ambulance", "fire_truck", "police_unit"]
    zone: str
    available: bool = True


class Hospital(BaseModel):
    id: str
    zone: str
    beds_available: int


class EnvState(BaseModel):
    task_id: str
    time: int
    incidents: List[Incident]
    responders: List[Responder]
    hospitals: List[Hospital]
    blocked_roads: List[str]
    steps_taken: int
    done: bool = False


class ActionInput(BaseModel):
    action_type: Literal[
        "dispatch_responder",
        "reserve_hospital",
        "reroute",
        "mark_resolved",
        "wait"
    ]
    incident_id: Optional[str] = None
    responder_id: Optional[str] = None
    hospital_id: Optional[str] = None
    new_path: Optional[List[str]] = None


class StepResponse(BaseModel):
    reward: float = Field(ge=0.0, le=1.0)
    done: bool
    message: str
    state: EnvState