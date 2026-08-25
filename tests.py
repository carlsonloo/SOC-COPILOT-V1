"""Dependency-free regression suite for SOC Copilot V1."""

from assessment import get_latest_assessment, record_assessment
from data import (
    incident_2001,
    incident_2002,
    incident_2003,
    incident_2004
)
from feedback import record_analyst_feedback
from main import run_soc_copilot
from recommendation import (
    build_recommendation_input,
    mock_recommendation
)
from retrieval import retrieve_playbook
from risk_engine import calculate_risk
from summary import build_summary_input, mock_llm_summary


test_cases = [
    {
        "name": "INC-2001 Suspicious Login",
        "incident": incident_2001,
        "expected_score": 65,
        "expected_severity": "High"
    },
    {
        "name": "INC-2002 Malware Detection",
        "incident": incident_2002,
        "expected_score": 60,
        "expected_severity": "High"
    },
    {
        "name": "INC-2003 Privileged Malware",
        "incident": incident_2003,
        "expected_score": 80,
        "expected_severity": "Critical"
    }
]


def run_evaluation(cases):
    passed = 0
    failed = 0

    for test in cases:
        result = calculate_risk(
            test["incident"]
        )

        score_pass = (
            result["score"]
            == test["expected_score"]
        )
        severity_pass = (
            result["final_severity"]
            == test["expected_severity"]
        )
        test_pass = score_pass and severity_pass

        if test_pass:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1

        print("----------------------------")
        print(test["name"])
        print("Status:", status)
        print("Expected Score:", test["expected_score"])
        print("Actual Score:", result["score"])
        print("Expected Severity:", test["expected_severity"])
        print("Actual Severity:", result["final_severity"])

    print("============================")
    print("Passed:", passed)
    print("Failed:", failed)

    assert failed == 0, f"{failed} deterministic risk test(s) failed"


def run_all_tests():
    run_evaluation(test_cases)

    print("\n=== Assessment History Test ===")

    incident_2004["risk_assessment_history"] = []
    incident_2004["context"]["suspicious_ip"] = False

    initial = record_assessment(
        incident_2004,
        score_stage="initial",
        calculated_at="2026-08-24T10:00:00+08:00"
    )

    incident_2004["context"]["suspicious_ip"] = True

    updated = record_assessment(
        incident_2004,
        score_stage="updated",
        calculated_at="2026-08-24T10:06:00+08:00"
    )

    latest = get_latest_assessment(
        incident_2004
    )

    assert initial["score"] == 40
    assert initial["final_severity"] == "Medium"
    assert updated["score"] == 65
    assert updated["final_severity"] == "High"
    assert len(incident_2004["risk_assessment_history"]) == 2
    assert (
        initial["evidence_snapshot"]["context"]["suspicious_ip"]
        is False
    )
    assert (
        updated["evidence_snapshot"]["context"]["suspicious_ip"]
        is True
    )
    assert latest["score_stage"] == "updated"

    print("Assessment history test: PASS")

    print("\n=== Summary Module Test ===")

    summary_input = build_summary_input(
        incident_2004
    )
    summary_output = mock_llm_summary(
        summary_input
    )

    assert summary_input["risk_score"] == 65
    assert summary_input["severity"] == "High"
    assert (
        summary_input["assessment_time"]
        == "2026-08-24T10:06:00+08:00"
    )
    assert "65" in summary_output["summary"]
    assert "High" in summary_output["summary"]

    print("Summary:", summary_output["summary"])
    print("Summary module test: PASS")

    print("\n=== Retrieval Module Test ===")

    retrieved_chunks = retrieve_playbook(
        incident_2004
    )
    retrieved_ids = [
        chunk["chunk_id"]
        for chunk in retrieved_chunks
    ]

    assert "SL-001" in retrieved_ids
    assert "SL-002" in retrieved_ids
    assert "SL-OLD" not in retrieved_ids
    assert "MW-001" not in retrieved_ids
    assert len(retrieved_ids) == 2

    print("Retrieved:", retrieved_ids)
    print("Retrieval module test: PASS")

    print("\n=== Recommendation Module Test ===")

    recommendation_input = build_recommendation_input(
        incident_2004,
        summary_output
    )
    recommendation_output = mock_recommendation(
        recommendation_input
    )

    assert recommendation_output["risk_score"] == 65
    assert recommendation_output["severity"] == "High"
    assert recommendation_output["human_review_required"] is True
    assert (
        recommendation_output["supported_by"]
        == ["SL-001", "SL-002"]
    )

    print("Recommendation:", recommendation_output["recommendation"])
    print("Supported by:", recommendation_output["supported_by"])
    print("Human review:", recommendation_output["human_review_required"])
    print("Recommendation module test: PASS")

    recommendation_output[
        "recommendation_id"
    ] = "REC-INC-2004-001"

    print("\n=== Feedback Module Test ===")

    incident_2004["feedback_history"] = []

    feedback = record_analyst_feedback(
        incident_2004,
        recommendation_output,
        decision="Modify",
        analyst_id="SOC-L1-001",
        reason=(
            "Analyst added MFA reset "
            "before credential reset."
        ),
        final_action=(
            "Verified user, revoked suspicious session, reset MFA "
            "and required credential reset."
        ),
        outcome="Contained",
        reviewed_at="2026-08-24T10:20:00+08:00"
    )

    assert feedback["decision"] == "Modify"
    assert feedback["outcome"] == "Contained"
    assert len(incident_2004["feedback_history"]) == 1

    print("Decision:", feedback["decision"])
    print("Outcome:", feedback["outcome"])
    print("Feedback history:", len(incident_2004["feedback_history"]))
    print("Feedback module test: PASS")

    print("\n=== End-to-End Copilot Test ===")

    copilot_result = run_soc_copilot(
        incident_2004
    )

    assert copilot_result["incident_id"] == "INC-2004"
    assert copilot_result["risk_assessment"]["score"] == 65
    assert (
        copilot_result["risk_assessment"]["final_severity"]
        == "High"
    )
    assert "65" in copilot_result["summary"]["summary"]
    assert (
        copilot_result["recommendation"]["supported_by"]
        == ["SL-001", "SL-002"]
    )
    assert (
        copilot_result["recommendation"]["human_review_required"]
        is True
    )

    print("Risk:", copilot_result["risk_assessment"]["score"])
    print("Severity:", copilot_result["risk_assessment"]["final_severity"])
    print("Summary:", copilot_result["summary"]["summary"])
    print("Supported by:", copilot_result["recommendation"]["supported_by"])
    print("End-to-end Copilot test: PASS")


if __name__ == "__main__":
    run_all_tests()
