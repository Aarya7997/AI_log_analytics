import pandas as pd

def detect_time_anomalies(df, window="5min", threshold=5):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    error_counts = (
        df[df["level"] == "ERROR"]
        .resample(window)
        .count()["message"]
    )

    anomalous_windows = error_counts[error_counts > threshold]
    return anomalous_windows
