#!/usr/bin/env bash
set -euo pipefail

echo "Initializing database and creating tables..."
python - <<PY
from app.database import engine, Base
import app.models as models

Base.metadata.create_all(bind=engine)
print('Tables created: ', list(Base.metadata.tables.keys()))
PY

echo "init_db completed"
