import os
import joblib
from sklearn.ensemble import IsolationForest
from embedding_model import get_embeddings

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest_bert.pkl")

def detect_anomalies(messages):
    os.makedirs(MODEL_DIR, exist_ok=True)

    embeddings = get_embeddings(messages)

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = IsolationForest(contamination=0.15, random_state=42)
        model.fit(embeddings)
        joblib.dump(model, MODEL_PATH)

    return model.predict(embeddings), embeddings
