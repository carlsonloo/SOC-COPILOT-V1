"""Prepare structured facts and turn them into a mock analyst summary."""

from assessment import get_latest_assessment


def build_summary_input(incident):
    assessment = get_latest_assessment(
        incident
    )

    return {
        "incident_id": incident["incident_id"],
        "incident_type": incident["incident_type"],
        "user_id": incident["user"]["user_id"],
        "risk_score": assessment["score"],
        "severity": assessment["final_severity"],
        "risk_factors": [
            factor["factor"]
            for factor in assessment["factors"]
        ],
        "evidence": assessment["evidence_snapshot"],
        "assessment_time": assessment["calculated_at"],
        "ruleset_version": assessment["ruleset_version"]
    }


def mock_llm_summary(summary_input):
    factors = ", ".join(
        summary_input["risk_factors"]
    )

    summary = (
        f'{summary_input["incident_type"]} '
        f'incident for user '
        f'{summary_input["user_id"]}. '
        f'Risk score is '
        f'{summary_input["risk_score"]} '
        f'with '
        f'{summary_input["severity"]} '
        f'severity. '
        f'Key risk factors: '
        f'{factors}.'
    )

    return {
        "incident_id": summary_input["incident_id"],
        "summary": summary,
        "generated_from_assessment": summary_input[
            "assessment_time"
        ],
        "ruleset_version": summary_input[
            "ruleset_version"
        ]
    }
