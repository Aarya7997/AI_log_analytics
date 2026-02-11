# AI_log_analytics
This project implements an AI-driven log analysis system that automatically parses heterogeneous logs, detects anomalous behavior using machine learning, and infers probable root causes with confidence scoring, all through an interactive web interface.


Modern software systems generate massive volumes of logs, making manual debugging slow and error-prone.
This project implements an AI-driven log analysis system that automatically parses heterogeneous logs, detects anomalous behavior using machine learning, and infers probable root causes with confidence scoring, all through an interactive web interface.

The system is designed to be format-agnostic, explainable, and production-oriented, reflecting real-world observability and monitoring use cases.

Key Features

✅ Supports multiple log formats (Application logs, HDFS/LogPai logs, Windows CBS logs)

✅ Unsupervised anomaly detection (no labeled data required)

✅ Domain-aware severity & root cause inference

✅ Batch and simulated real-time log ingestion

✅ Interactive Streamlit dashboard

✅ Fault-tolerant ML pipeline with model persistence

System Architecture
Log Files
   ↓
Multi-Pattern Log Parser
   ↓
Structured Log Data
   ↓
NLP Feature Extraction
   ↓
Anomaly Detection (ML)
   ↓
Root Cause & Severity Inference
   ↓
Visualization Dashboard

Project Structure
ai_log_analyser/
│
├── logs/                  # Sample log files
├── data/                  # Parsed logs & feature outputs
├── models/                # Saved ML models
│
├── app.py                 # Streamlit application
├── log_parser.py          # Multi-format log parser
├── anomaly_model.py       # ML anomaly detection logic
├── root_cause.py          # Root cause & severity inference
├── time_window_analyzer.py# Temporal anomaly detection
├── log_streamer.py        # Streaming log simulation
├── requirements.txt       # Dependencies

Log Parsing (log_parser.py)
Problem
Logs come in different formats, timestamps, and structures.

Solution
Implemented a multi-pattern regex-based parser that automatically detects and normalizes logs into a unified schema.

Supported Formats
1. Standard application logs
2025-01-10 10:22:30 ERROR Database timeout


2. HDFS / LogPai logs
081109 203615 148 INFO dfs.DataNode$PacketResponder: message


3. Windows CBS logs
2016-09-28 04:30:31, Info CBS Failed to get next element [HRESULT=...]

Output Schema
timestamp | level | message | log_type

This normalization allows downstream ML models to operate independently of log format.

Anomaly Detection (anomaly_model.py)
Model Used

Isolation Forest (Unsupervised Learning)

Why Isolation Forest?
1. Logs are largely unlabeled
2. Anomalies are rare
3. Efficient for high-dimensional text features
4. Well-suited for operational data
5. Feature Representation
6. NLP-based vectorization of log messages
7. Supports both sparse (TF-IDF) and dense (embedding-based) representations

Output:-

1 → Normal behavior

-1 → Anomalous behavior

Models are persisted to disk to avoid retraining on every run.

🧠 Root Cause & Severity Inference (root_cause.py)
Key Insight

Log severity labels (INFO/WARN/ERROR) are often unreliable, especially in real systems like HDFS and Windows CBS.

Approach

Implemented domain-aware rule-based reasoning on top of ML output:

Combines:

Log message semantics

Log type (HDFS / Windows CBS / Generic)

ML anomaly flag

Produces:

Human-readable root cause

Confidence score

Example
Log Message	Root Cause
Failed to get next element [HRESULT=...]	Windows Update Failure
Warning: Unrecognized attribute	Windows Update Warning
Served block blk_xxx	Normal HDFS Operation

This hybrid approach improves explainability and trust.

Time-Window Analysis (time_window_analyzer.py)

Detects temporal spikes in error frequency by grouping logs into fixed time windows.

Why this matters:

System failures often emerge over time, not in isolation

Helps identify cascading or burst failures

Streaming Simulation (log_streamer.py)

Simulates real-time log ingestion by streaming logs line-by-line.

This demonstrates how the system can be extended to:

Online inference

Monitoring pipelines

Real-time alerting systems

Web Interface (app.py)

Built using Streamlit to rapidly prototype a production-style dashboard.

Capabilities

Upload .log / .txt files

View parsed logs

Visualize anomalies

Inspect root cause distribution

Analyze time-window error spikes

Simulate live log streaming
