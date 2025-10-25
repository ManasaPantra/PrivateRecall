# PrivateRecall — Multimodal AI Assistant

PrivateRecall is a privacy-first “second brain” that runs entirely on your device. It captures screenshots and voice notes, creates searchable embeddings, and lets you recall moments with natural language — no cloud required.

## Highlights
- On-device multimodal ingestion: image captioning (BLIP) and speech-to-text (Whisper)
- Local retrieval: FAISS vector search + SQLite metadata
- Simple UI: Streamlit app for upload, search, and weekly reflections
- Optional local LLM (Ollama) for summaries

## Quickstart
```bash
git clone https://github.com/GITHUB_USER/PrivateRecall.git
cd PrivateRecall
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
bash run_app.sh
```
Open http://localhost:8501

## Configuration (optional)
Create a `.env` for any connectors/tokens you use (kept local):
```
SQLITE_DB_PATH=data/memories.sqlite3
FAISS_DB_PATH=data/memories.faiss
# SLACK_BOT_TOKEN=...
```

## Project Structure
```
app/              # Streamlit UI and retrieval flow
models/           # BLIP captioning, Whisper, and embeddings
tests/            # Basic tests
run_app.sh        # Launches the UI
```

## Maintainer
Manasa

## License
Choose a license (e.g., MIT) and add a LICENSE file.
# PrivateRecall
