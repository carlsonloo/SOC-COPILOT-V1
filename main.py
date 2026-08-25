"""Orchestration layer for the SOC Copilot V1 pipeline."""

from assessment import get_latest_assessment, record_assessment
from recommendation import (
    build_recommendation_input,
    mock_recommendation
)
from summary import build_summary_input, mock_llm_summary


def run_soc_copilot(
    incident,
    create_new_assessment=False,
    score_stage="initial"
):
    if create_new_assessment:
        record_assessment(
            incident,
            score_stage=score_stage
        )

    assessment = get_latest_assessment(
        incident
    )

    summary_input = build_summary_input(
        incident
    )

    summary_output = mock_llm_summary(
        summary_input
    )

    recommendation_input = build_recommendation_input(
        incident,
        summary_output
    )

    recommendation_output = mock_recommendation(
        recommendation_input
    )

    recommendation_output[
        "recommendation_id"
    ] = (
        "REC-"
        + incident["incident_id"]
        + "-001"
    )

    return {
        "incident_id": incident["incident_id"],
        "risk_assessment": assessment,
        "summary": summary_output,
        "recommendation": recommendation_output
    }
