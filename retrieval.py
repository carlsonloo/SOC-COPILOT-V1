"""Retrieve active playbook chunks for an incident type."""

playbook_chunks = [
    {
        "chunk_id": "SL-001",
        "incident_type": "Suspicious Login",
        "section": "Investigation Steps",
        "version": "v2",
        "policy_status": "active",
        "content": (
            "Verify the user through an independent channel "
            "and review recent authentication activity."
        )
    },
    {
        "chunk_id": "SL-002",
        "incident_type": "Suspicious Login",
        "section": "Containment",
        "version": "v2",
        "policy_status": "active",
        "content": (
            "If the login is unauthorized, revoke suspicious "
            "sessions and require credential reset. "
            "Human approval is required."
        )
    },
    {
        "chunk_id": "SL-OLD",
        "incident_type": "Suspicious Login",
        "section": "Legacy Policy",
        "version": "v1",
        "policy_status": "retired",
        "content": "Automatically disable the account immediately."
    },
    {
        "chunk_id": "MW-001",
        "incident_type": "Malware Detection",
        "section": "Malware Investigation",
        "version": "v2",
        "policy_status": "active",
        "content": (
            "Validate the malicious artifact and inspect "
            "endpoint behavior before containment."
        )
    }
]


def retrieve_playbook(incident):
    retrieved = []

    for chunk in playbook_chunks:
        same_incident_type = (
            chunk["incident_type"]
            == incident["incident_type"]
        )

        active_policy = (
            chunk["policy_status"]
            == "active"
        )

        if same_incident_type and active_policy:
            retrieved.append(chunk)

    return retrieved
