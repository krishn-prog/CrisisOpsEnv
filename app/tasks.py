from app.models import Incident, Responder, Hospital

TASKS = {
    "easy_dispatch": {
        "description": "Handle one medical emergency using the nearest ambulance and valid hospital.",
        "incidents": [
            Incident(id="INC001", type="medical", severity="high", zone="A")
        ],
        "responders": [
            Responder(id="AMB01", type="ambulance", zone="A"),
            Responder(id="AMB02", type="ambulance", zone="C")
        ],
        "hospitals": [
            Hospital(id="HOSP1", zone="B", beds_available=2)
        ],
        "blocked_roads": []
    },

    "medium_priority": {
        "description": "Prioritize multiple incidents with limited responders.",
        "incidents": [
            Incident(id="INC101", type="medical", severity="critical", zone="A"),
            Incident(id="INC102", type="fire", severity="high", zone="B"),
            Incident(id="INC103", type="medical", severity="medium", zone="C")
        ],
        "responders": [
            Responder(id="AMB01", type="ambulance", zone="A"),
            Responder(id="FIRE01", type="fire_truck", zone="B")
        ],
        "hospitals": [
            Hospital(id="HOSP1", zone="A", beds_available=1),
            Hospital(id="HOSP2", zone="C", beds_available=1)
        ],
        "blocked_roads": ["B-C"]
    },

    "hard_surge": {
        "description": "Handle citywide emergency surge with road blocks and limited capacity.",
        "incidents": [
            Incident(id="INC201", type="medical", severity="critical", zone="A"),
            Incident(id="INC202", type="fire", severity="critical", zone="B"),
            Incident(id="INC203", type="medical", severity="high", zone="C"),
            Incident(id="INC204", type="police", severity="medium", zone="D")
        ],
        "responders": [
            Responder(id="AMB01", type="ambulance", zone="A"),
            Responder(id="FIRE01", type="fire_truck", zone="C"),
            Responder(id="POL01", type="police_unit", zone="D")
        ],
        "hospitals": [
            Hospital(id="HOSP1", zone="A", beds_available=1),
            Hospital(id="HOSP2", zone="D", beds_available=1)
        ],
        "blocked_roads": ["A-B", "B-C"]
    }
}