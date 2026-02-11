import re
import pandas as pd
from datetime import datetime

# -------- LOG PATTERNS --------

PATTERNS = [
    # Pattern 1: Standard logs
    {
        "regex": r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<level>INFO|WARN|ERROR)\s+(?P<message>.*)',
        "type": "standard"
    },

    # Pattern 2: HDFS / LogPai logs
    {
        "regex": r'(?P<date>\d{6})\s+(?P<time>\d{6})\s+\d+\s+(?P<level>INFO|WARN|ERROR)\s+(?P<message>.*)',
        "type": "hdfs"
    },
    # Pattern 3: Windows logs
    {
        "type": "windows_cbs",
        "regex": r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\s+(?P<level>Info|Warning|Error)\s+CBS\s+(?P<message>.*)'
    }
]

# -------- PARSER FUNCTION --------
def parse_logs(log_lines):
    records = []

    for line in log_lines:
        line = line.strip()

        for pattern in PATTERNS:
            match = re.match(pattern["regex"], line)
            if not match:
                continue

            data = match.groupdict()

            # ---- Timestamp handling ----
            if pattern["type"] == "standard":
                timestamp = datetime.strptime(
                    data["timestamp"], "%Y-%m-%d %H:%M:%S"
                )

            elif pattern["type"] == "hdfs":
                timestamp = datetime.strptime(
                    data["date"] + data["time"], "%y%m%d%H%M%S"
                )

            elif pattern["type"] == "windows_cbs":
                timestamp = datetime.strptime(
                    data["timestamp"], "%Y-%m-%d %H:%M:%S"
                )

            # ---- Normalize log level ----
            level = data["level"].upper()

            records.append({
                "timestamp": timestamp,
                "level": level,
                "message": data["message"],
                "log_type": pattern["type"]
            })

            break  # stop after first match

    return pd.DataFrame(records)