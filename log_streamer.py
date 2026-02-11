import time

def stream_logs(log_file, delay=1):
    with open(log_file) as f:
        for line in f:
            yield line
            time.sleep(delay)
