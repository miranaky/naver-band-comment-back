from api import router as api_router
from core import task
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware


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
    app.add_event_handler("startup", task.create_start_handler(app))

    return app


def serve():
    import uvicorn

    uvicorn.run(
        "main:get_app", port=8098, log_level="info", reload=True, reload_dirs=["./"]
    )


if __name__ == "__main__":
    serve()
