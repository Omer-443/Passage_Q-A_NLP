import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def find_best_chunk(question, chunks, embeddings):
    q_embedding = embedding_model.encode([question])[0]
    scores = np.dot(embeddings, q_embedding)
    top_idx = np.argmax(scores)
    return chunks[top_idx]