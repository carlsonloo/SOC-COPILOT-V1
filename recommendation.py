"""Build a policy-grounded mock recommendation for analyst review."""

from assessment import get_latest_assessment
from retrieval import retrieve_playbook


def build_recommendation_input(
    incident,
    summary_output
):
    assessment = get_latest_assessment(
        incident
    )

    policies = retrieve_playbook(
        incident
    )

    return {
        "incident_id": incident["incident_id"],
        "summary": summary_output["summary"],
        "risk_score": assessment["score"],
        "severity": assessment["final_severity"],
        "policy_context": [
            {
                "chunk_id": chunk["chunk_id"],
                "section": chunk["section"],
                "content": chunk["content"]
            }
            for chunk in policies
        ]
    }


def mock_recommendation(recommendation_input):
    policy_context = recommendation_input[
        "policy_context"
    ]

    policy_ids = [
        chunk["chunk_id"]
        for chunk in policy_context
    ]

    recommendation = (
        "Verify the user through an independent channel. "
        "Review recent authentication activity. "
        "If the login is confirmed as unauthorized, "
        "revoke suspicious sessions and require "
        "credential reset. "
        "Human approval is required before containment."
    )

    return {
        "incident_id": recommendation_input[
            "incident_id"
        ],
        "risk_score": recommendation_input[
            "risk_score"
        ],
        "severity": recommendation_input[
            "severity"
        ],
        "recommendation": recommendation,
        "supported_by": policy_ids,
        "human_review_required": True
    }
