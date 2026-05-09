# mktplace
Lloyds Market Place

FrontEnd: http://localhost:8501
Backend: http://localhost:8000
Backend API docs: http://localhost:8000/docs
ChromaDB host port: http://localhost:8001
Portainer: https://localhost:9443

Quickstart (Docker-first):

1) Create Docker env file

```bash
cp .env.docker.example .env.docker
# then edit .env.docker to add your OPENAI_API_KEY (optional for now)
```

2) Launch the full stack

```bash
docker compose up -d --build
```

3) Open the apps

- Streamlit UI: http://localhost:8501
- FastAPI backend: http://localhost:8000 (docs at /docs)
- ChromaDB server (optional for now): http://localhost:8001
- Portainer (Docker management): https://localhost:9443

4) Live editing in VS Code

- Source code, data, and assets are mounted into the containers via volumes.
- Edit code locally in VS Code; backend (uvicorn --reload) and frontend (Streamlit) auto-reload.
- Inventory CSV is read from `data/dataset.csv` by default; car images from `assets/` (placeholder included).

5) Logs and control

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose restart backend
docker compose down
docker compose down -v   # deletes database/vector/Portainer volumes; use with care
```

Local (non-Docker) development:

- `.env.example` shows a local configuration. Copy to `.env` and adjust as needed if you choose to run services outside Docker.
- Docker Compose remains the default and recommended local runtime.

Docker Commands:
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose restart backend
docker compose down
docker compose down -v (only use to delete database/vector/Portainer volumes.)

https://prod.liveshare.vsengsaas.visualstudio.com/join?5E2712283F408F9A627D29F2E26A64100A98