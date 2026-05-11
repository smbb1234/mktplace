from __future__ import annotations

from typing import List, Dict, Any

from .chroma_config import get_chroma_client


def index_vehicle(vehicle_id: str, metadata: Dict[str, Any], embedding: List[float]) -> bool:
    client = get_chroma_client()
    if client is None:
        # No-op fallback for local-disabled Chroma
        return False
    try:
        collection = client.get_or_create_collection("vehicles")
        collection.add(ids=[vehicle_id], metadatas=[metadata], embeddings=[embedding])
        return True
    except Exception:
        return False


def query_similar(query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    client = get_chroma_client()
    if client is None:
        return []
    try:
        collection = client.get_or_create_collection("vehicles")
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        # Normalize to list of {id, score, metadata}
        out: List[Dict[str, Any]] = []
        for i, _ in enumerate(results.get("ids", [[]])[0]):
            out.append({
                "id": results["ids"][0][i],
                "score": results.get("distances", [[]])[0][i],
                "metadata": results.get("metadatas", [[]])[0][i],
            })
        return out
    except Exception:
        return []
