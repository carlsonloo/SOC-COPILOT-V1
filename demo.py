"""Run a compact end-to-end SOC Copilot portfolio demonstration."""

import json

from assessment import record_assessment
from data import incident_2004
from feedback import record_analyst_feedback
from main import run_soc_copilot


def run_demo():
    incident_2004["risk_assessment_history"] = []
    incident_2004["feedback_history"] = []
    incident_2004["context"]["suspicious_ip"] = False

    record_assessment(
        incident_2004,
        score_stage="initial",
        calculated_at="2026-08-24T10:00:00+08:00"
    )

    incident_2004["context"]["suspicious_ip"] = True

    record_assessment(
        incident_2004,
        score_stage="updated",
        calculated_at="2026-08-24T10:06:00+08:00"
    )

    copilot_result = run_soc_copilot(
        incident_2004
    )

    feedback = record_analyst_feedback(
        incident_2004,
        copilot_result["recommendation"],
        decision="Modify",
        analyst_id="SOC-L1-001",
        reason="Analyst added MFA reset before credential reset.",
        final_action=(
            "Verified user, revoked suspicious session, reset MFA "
            "and required credential reset."
        ),
        outcome="Contained",
        reviewed_at="2026-08-24T10:20:00+08:00"
    )

    demo_output = {
        "copilot_result": copilot_result,
        "analyst_feedback": feedback
    }

    print(json.dumps(demo_output, indent=2))


if __name__ == "__main__":
    run_demo()
