"""
PathFinder-AI / llm_engine.py
Lightweight RAG engine (DistilBERT + FAISS) that replaces the old Keras model.
Public API:
    chatbot_response(user_text) -> str
"""

import json
import os
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
import faiss

# ------------------------------------------------------------------
# 1-time NLTK resources
# ------------------------------------------------------------------
nltk.download("punkt", quiet=True)
lemmatizer = WordNetLemmatizer()

# ------------------------------------------------------------------
# Load knowledge base
# ------------------------------------------------------------------
INTENTS_PATH = os.path.join(os.path.dirname(__file__), "intents_v2.jsonl")
intents = []
sentences = []

with open(INTENTS_PATH, encoding="utf-8") as f:
    for line in f:
        row = json.loads(line.strip())
        intents.append(row)
        for pat in row["patterns"]:
            sentences.append(pat)

# ------------------------------------------------------------------
# Sentence encoder + FAISS index
# ------------------------------------------------------------------
ENCODER = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = ENCODER.encode(sentences, show_progress_bar=False, normalize_embeddings=True)

index = faiss.IndexFlatIP(embeddings.shape[1])  # cosine via inner product
index.add(np.array(embeddings, dtype="float32"))

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def _most_similar(text: str, threshold: float = 0.45):
    vec = ENCODER.encode([text], normalize_embeddings=True).astype("float32")
    scores, idxs = index.search(vec, k=1)
    if scores[0][0] < threshold:
        return None
    return idxs[0][0]

def chatbot_response(user_text: str) -> str:
    idx = _most_similar(user_text)
    if idx is None:
        return ("I’m still learning—could you rephrase or ask about careers, salaries, or study paths?")
    intent = next(i for i in intents if user_text in i["patterns"])
    return np.random.choice(intent["responses"])