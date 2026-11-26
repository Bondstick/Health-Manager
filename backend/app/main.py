from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text

from . import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()  # creates tables on startup if they are missing
    yield


app = FastAPI(title="Personal Health Manager API", version="0.2.0", lifespan=lifespan)


@app.get("/health")
def health():
    """Checks the API is running and can reach the database."""
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception as exc:  # report the failure instead of crashing
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "unreachable", "detail": str(exc)},
        )
