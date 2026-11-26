# Backend

FastAPI app. Runs in Docker with the database (see the top-level `docker-compose.yml`).

## Endpoints so far
- `GET /health`: confirms the API is running and can reach PostgreSQL. Returns `{"status": "ok", "database": "ok"}`, or 503 if the database is unreachable.
- `GET /docs`: automatic interactive API page.

## Run it
From the project root:
```
docker compose up -d --build
```
Then open http://localhost:8000/health in a browser.
