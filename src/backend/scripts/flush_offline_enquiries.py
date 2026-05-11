from __future__ import annotations

import json
from pathlib import Path
from src.backend.core.database import SessionLocal
from src.backend.repositories.leads import LeadsRepository

QUEUE = Path("data/offline_enquiries.jsonl")


def flush_queue():
    if not QUEUE.exists():
        print("No offline enquiries to flush")
        return
    session = SessionLocal()
    repo = LeadsRepository(session)
    success_count = 0
    lines = QUEUE.read_text(encoding="utf-8").splitlines()
    remaining = []
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            repo.create_enquiry(enquiry_data=payload)
            success_count += 1
        except Exception as e:
            print("Failed to flush a queued enquiry, keeping for retry", e)
            remaining.append(line)
    if remaining:
        QUEUE.write_text("\n".join(remaining), encoding="utf-8")
    else:
        QUEUE.unlink()
    session.close()
    print(f"Flushed {success_count} enquiries")


if __name__ == "__main__":
    flush_queue()
