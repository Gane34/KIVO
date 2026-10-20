"""FastAPI Application factory for PhysioTwin REST API.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from physiotwin.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="PhysioTwin REST API",
        version="0.1.0",
        description=(
            "Digital Twin Challenge 2026: Mechanistic glucose regulation API. "
            "All datasets and patient records are synthetic for research prototyping."
        ),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()
