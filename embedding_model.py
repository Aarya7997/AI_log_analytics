from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(messages):
    return model.encode(messages, show_progress_bar=False)
