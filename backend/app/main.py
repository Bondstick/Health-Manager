import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from . import db
from .routes import router as patient_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()  # creates tables on startup if they are missing
    yield


app = FastAPI(title="Personal Health Manager API", version="0.4.0", lifespan=lifespan)
app.include_router(patient_router)

# Only local dev sites may call the API from a browser (used with `npm run dev`).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


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


# Serve the built React app from the same server, so one public link covers both.
# Added last, so the API routes above always take priority.
_frontend_dir = os.environ.get("FRONTEND_DIST")
if _frontend_dir and os.path.isfile(os.path.join(_frontend_dir, "index.html")):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
