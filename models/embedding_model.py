from typing import List

from sentence_transformers import SentenceTransformer

_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_text_embedding(text_input: str) -> List[float]:
    """Return a 384-dim embedding for the given text as a Python list."""
    embedding = _embedding_model.encode(text_input, normalize_embeddings=True)
    # Ensure JSON-serializable for Streamlit caching, etc.
    return embedding.tolist()


