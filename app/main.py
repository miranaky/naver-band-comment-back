from app.api import router as api_router
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

    return app


def serve():
    import uvicorn
    import multiprocessing
    multiprocessing.freeze_support()
    uvicorn.run("app.main:get_app",host="0.0.0.0", port=8098, log_level="info",reload=False)


if __name__ == "__main__":
    serve()
