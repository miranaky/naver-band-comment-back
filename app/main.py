from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api import router as api_router
from app.core import task


def get_app() -> FastAPI:
    app = FastAPI(title="Naver Band API", version="0.1")
    app.include_router(api_router, prefix="")
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", task.create_start_app_handler(app))

    return app


app = get_app()


@app.get("/health")
def health_check():
    return {"status": "ok"}
