"""Capture human review decisions and final SOC outcomes."""

from datetime import datetime

from assessment import MYT


def record_analyst_feedback(
    incident,
    recommendation_output,
    decision,
    analyst_id,
    reason=None,
    final_action=None,
    outcome="pending",
    reviewed_at=None
):
    allowed_decisions = [
        "Accept",
        "Modify",
        "Reject"
    ]

    if decision not in allowed_decisions:
        raise ValueError(
            "Decision must be Accept, Modify or Reject"
        )

    if (
        decision in ["Modify", "Reject"]
        and not reason
    ):
        raise ValueError(
            "Reason is required for Modify or Reject"
        )

    if reviewed_at is None:
        reviewed_at = datetime.now(
            MYT
        ).isoformat(timespec="seconds")

    feedback = {
        "recommendation_id": recommendation_output[
            "recommendation_id"
        ],
        "decision": decision,
        "analyst_id": analyst_id,
        "reason": reason,
        "final_action": final_action,
        "outcome": outcome,
        "reviewed_at": reviewed_at
    }

    if "feedback_history" not in incident:
        incident["feedback_history"] = []

    incident["feedback_history"].append(
        feedback
    )

    return feedback
