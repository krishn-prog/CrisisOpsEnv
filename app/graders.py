from app.models import EnvState

SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

def grade_task(state: EnvState) -> float:
    total = len(state.incidents)
    resolved = sum(1 for i in state.incidents if i.status == "resolved")

    if total == 0:
        return 0.0

    base_score = resolved / total

    unresolved_critical = sum(
        1 for i in state.incidents
        if i.status != "resolved" and i.severity == "critical"
    )

    penalty = 0.2 * unresolved_critical
    score = max(0.0, min(1.0, base_score - penalty))
    return round(score, 3)