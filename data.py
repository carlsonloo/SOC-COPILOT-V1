"""In-memory incident fixtures used by the demo and regression suite."""

incident_2001 = {
    "incident_id": "INC-2001",
    "incident_type": "Suspicious Login",
    "user": {
        "user_id": "FMD-3501",
        "privileged": False
    },
    "context": {
        "impossible_travel": True,
        "suspicious_ip": True,
        "outside_working_hours": True
    }
}


incident_2002 = {
    "incident_id": "INC-2002",
    "incident_type": "Malware Detection",
    "user": {
        "user_id": "PCC-003",
        "privileged": False
    },
    "context": {
        "malicious_file_reputation": True,
        "persistence": True,
        "suspicious_network_activity": False
    }
}


incident_2003 = {
    "incident_id": "INC-2003",
    "incident_type": "Malware Detection",
    "user": {
        "user_id": "ADM-003",
        "privileged": True
    },
    "context": {
        "malicious_file_reputation": True,
        "persistence": True,
        "suspicious_network_activity": True
    }
}


incident_2004 = {
    "incident_id": "INC-2004",
    "incident_type": "Suspicious Login",
    "user": {
        "user_id": "USR-2004",
        "privileged": False
    },
    "context": {
        "impossible_travel": True,
        "suspicious_ip": False,
        "outside_working_hours": True
    },
    "risk_assessment_history": []
}
