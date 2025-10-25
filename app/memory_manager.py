import faiss
import numpy as np
import sqlite3
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH") or os.path.join("data", "memories.sqlite3")
FAISS_DB_PATH = os.getenv("FAISS_DB_PATH") or os.path.join("data", "memories.faiss")
EMBEDDING_DIM = 384


def initialize_memory() -> None:
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(SQLITE_DB_PATH):
        conn = sqlite3.connect(SQLITE_DB_PATH)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE memories (
                id INTEGER PRIMARY KEY,
                caption TEXT,
                modality TEXT,
                timestamp TEXT,
                filepath TEXT
            )
        """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                summary TEXT,
                timestamp TEXT,
                tags TEXT
            )
        """
        )
        conn.commit()
        conn.close()

    if not os.path.exists(FAISS_DB_PATH):
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        faiss.write_index(index, FAISS_DB_PATH)


def add_memory(caption: str, modality: str, filepath: str, embedding: list) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(SQLITE_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO memories (caption, modality, timestamp, filepath)
        VALUES (?, ?, ?, ?)
        """,
        (caption, modality, timestamp, filepath),
    )
    conn.commit()
    conn.close()

    index = faiss.read_index(FAISS_DB_PATH)
    vec = np.array([embedding], dtype="float32")
    index.add(vec)
    faiss.write_index(index, FAISS_DB_PATH)


def search_memory(query_embedding: list, k: int = 5):
    index = faiss.read_index(FAISS_DB_PATH)
    vector = np.array([query_embedding], dtype="float32")
    distances, indices = index.search(vector, k)

    conn = sqlite3.connect(SQLITE_DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM memories")
    rows = c.fetchall()
    conn.close()

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(rows):
            results.append(rows[idx])
    return results


def save_reflection(summary: str, tags: str = "") -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(SQLITE_DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO reflections (summary, timestamp, tags)
        VALUES (?, ?, ?)
        """,
        (summary, timestamp, tags),
    )
    conn.commit()
    conn.close()
