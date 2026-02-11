def tag_root_cause_with_confidence(message, anomaly_flag, level=None):
    msg = message.lower()

    # ---- BASE CONFIDENCE ----
    confidence = 0.0

    # ---- INFO LOGS SHOULD NOT BE ANOMALIES ----
    if level == "INFO":
        return "Normal Operation", 0.1

    # ---- WARN LOGS ----
    if level == "WARN":
        if anomaly_flag == -1:
            return "Warning Pattern Detected", 0.4
        else:
            return "Normal Warning", 0.2

    # ---- ERROR LOGS (REAL ANALYSIS) ----
    if level == "ERROR":
        confidence = 0.6

        if "timeout" in msg or "latency" in msg:
            return "Network Issue", confidence + 0.2

        if "memory" in msg or "heap" in msg:
            return "Memory Leak", confidence + 0.3

        if "connection refused" in msg or "unreachable" in msg:
            return "Service Down", confidence + 0.3

        if anomaly_flag == -1:
            return "Unknown Error Anomaly", confidence

        return "Known Error Pattern", 0.4

    # ---- FALLBACK ----
    return "Unclassified", 0.1
