import streamlit as st
import pandas as pd
import os

from log_parser import parse_logs
from anomaly_model import detect_anomalies
from root_cause import tag_root_cause_with_confidence
from time_window_analyzer import detect_time_anomalies
from log_streamer import stream_logs

st.set_page_config(page_title="AI Log Analyzer", layout="wide")

st.title("🔍 Automated AI Log Analysis & Root Cause Detection System")
st.write("Upload log files or analyze existing system logs.")

log_files = st.file_uploader(
    "Upload one or more log files",
    type=["log", "txt"],
    accept_multiple_files=True
)

log_lines = []

if log_files:
    for file in log_files:
        log_lines.extend(file.read().decode("utf-8").splitlines())
else:
    for file in ["logs/application.log", "logs/server.log", "logs/system.log"]:
        if os.path.exists(file):
            with open(file) as f:
                log_lines.extend(f.readlines())

# ---- PARSE LOGS ----
df = parse_logs(log_lines)

if df.empty:
    st.error("No valid log entries found.")
    st.stop()

# ---- ANOMALY DETECTION (FIRST) ----
anomalies, features = detect_anomalies(df["message"])
df["anomaly"] = anomalies

# ---- ROOT CAUSE + CONFIDENCE (AFTER anomaly exists) ----
df[["root_cause", "confidence"]] = df.apply(
    lambda row: tag_root_cause_with_confidence(
        row["message"], row["anomaly"], row["level"]
    ),
    axis=1,
    result_type="expand"
)


# ---- SAVE OUTPUTS ----
os.makedirs("data", exist_ok=True)
df.to_csv("data/parsed_logs.csv", index=False)

features_df = pd.DataFrame(features)
features_df.to_csv("data/features.csv", index=False)

# ---- DISPLAY RESULTS ----
st.subheader("📊 Parsed Logs")
st.dataframe(df)

st.subheader("🚨 Anomalies Detected")
st.dataframe(df[df["anomaly"] == -1])

st.subheader("📈 Root Cause Distribution")
st.bar_chart(df["root_cause"].value_counts())

st.success("Analysis completed. Results saved in data/ folder.")

# ---- TIME WINDOW ANALYSIS ----
st.subheader("⏱ Time-Window Error Anomalies")
time_anomalies = detect_time_anomalies(df.copy())

if not time_anomalies.empty:
    st.dataframe(time_anomalies)
else:
    st.write("No abnormal error spikes detected.")

# ---- STREAMING SIMULATION ----
st.subheader("📡 Live Log Streaming")

if st.button("▶ Start Live Log Stream"):
    streamed_logs = []

    for log in stream_logs("logs/system.log"):
        streamed_logs.append(log)
        live_df = parse_logs(streamed_logs)

        if not live_df.empty:
            anomalies, _ = detect_anomalies(live_df["message"])
            live_df["anomaly"] = anomalies

            st.dataframe(live_df.tail(5))
