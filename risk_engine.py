"""Deterministic risk scoring for supported SOC incident types."""


def get_severity(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"


def calculate_suspicious_login_risk(incident):
    score = 0
    factors = []

    context = incident["context"]

    if context.get("impossible_travel"):
        score += 30
        factors.append({
            "factor": "impossible_travel",
            "contribution": 30
        })

    if context.get("suspicious_ip"):
        score += 25
        factors.append({
            "factor": "suspicious_ip",
            "contribution": 25
        })

    if context.get("outside_working_hours"):
        score += 10
        factors.append({
            "factor": "outside_working_hours",
            "contribution": 10
        })

    score = max(0, min(100, score))

    base_severity = get_severity(score)
    final_severity = base_severity

    if incident["user"].get("privileged"):
        if final_severity in ["Low", "Medium"]:
            final_severity = "High"

    return {
        "score": score,
        "base_severity": base_severity,
        "final_severity": final_severity,
        "factors": factors,
        "ruleset_version": "v0.1"
    }


def calculate_malware_risk(incident):
    score = 0
    factors = []

    context = incident["context"]

    if context.get("malicious_file_reputation"):
        score += 30
        factors.append({
            "factor": "malicious_file_reputation",
            "contribution": 30
        })

    if context.get("persistence"):
        score += 30
        factors.append({
            "factor": "persistence",
            "contribution": 30
        })

    if context.get("suspicious_network_activity"):
        score += 20
        factors.append({
            "factor": "suspicious_network_activity",
            "contribution": 20
        })

    score = max(0, min(100, score))

    base_severity = get_severity(score)
    final_severity = base_severity

    if incident["user"].get("privileged"):
        if final_severity in ["Low", "Medium"]:
            final_severity = "High"

    return {
        "score": score,
        "base_severity": base_severity,
        "final_severity": final_severity,
        "factors": factors,
        "ruleset_version": "v0.1"
    }


def calculate_risk(incident):
    if incident["incident_type"] == "Suspicious Login":
        return calculate_suspicious_login_risk(incident)
    elif incident["incident_type"] == "Malware Detection":
        return calculate_malware_risk(incident)
    else:
        raise ValueError("Unsupported incident type")
