from typing import Dict, Any

from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableLambda

from app.memory_manager import search_memory
from models.embedding_model import get_text_embedding


def embed_query(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state["query"]
    state["embedded_query"] = get_text_embedding(query)
    return state


def search_relevant(state: Dict[str, Any]) -> Dict[str, Any]:
    embedding = state["embedded_query"]
    state["search_results"] = search_memory(embedding, k=5)
    return state


def format_results(state: Dict[str, Any]) -> Dict[str, Any]:
    results = state["search_results"]
    messages = []
    for r in results:
        _, caption, modality, timestamp, filepath = r
        messages.append(
            {
                "caption": caption,
                "modality": modality,
                "timestamp": timestamp,
                "filepath": filepath,
            }
        )
    state["formatted"] = messages
    return state


def build_langgraph_memory_flow():
    g = StateGraph()
    g.add_node("embed_query", RunnableLambda(embed_query))
    g.add_node("search_relevant", RunnableLambda(search_relevant))
    g.add_node("format_results", RunnableLambda(format_results))

    g.set_entry_point("embed_query")
    g.add_edge("embed_query", "search_relevant")
    g.add_edge("search_relevant", "format_results")
    g.add_edge("format_results", END)

    return g.compile()

