"""Create and retain auditable point-in-time risk assessments."""

from copy import deepcopy
from datetime import datetime, timedelta, timezone

from risk_engine import calculate_risk


MYT = timezone(timedelta(hours=8))


def create_assessment(
    incident,
    score_stage="initial",
    calculated_at=None
):
    result = calculate_risk(incident)

    if calculated_at is None:
        calculated_at = datetime.now(
            MYT
        ).isoformat(timespec="seconds")

    result["score_stage"] = score_stage
    result["calculated_at"] = calculated_at

    result["evidence_snapshot"] = {
        "user_id": incident["user"].get(
            "user_id"
        ),
        "privileged": incident["user"].get(
            "privileged",
            False
        ),
        "context": deepcopy(
            incident.get("context", {})
        )
    }

    return result


def record_assessment(
    incident,
    score_stage="initial",
    calculated_at=None
):
    assessment = create_assessment(
        incident,
        score_stage=score_stage,
        calculated_at=calculated_at
    )

    if "risk_assessment_history" not in incident:
        incident["risk_assessment_history"] = []

    incident["risk_assessment_history"].append(
        assessment
    )

    return assessment


def get_latest_assessment(incident):
    history = incident.get(
        "risk_assessment_history",
        []
    )

    if not history:
        raise ValueError(
            "No risk assessment found"
        )

    return history[-1]
