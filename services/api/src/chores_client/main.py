from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chores_client.config import load_config
from chores_client.responses import error_handlers
from chores_client.routes import all_routes


def get_allowed_origins() -> list[str]:
    config = load_config()

    # Production origins
    origins = ["https://chores.prateekpisat.com", "https://www.chores.prateekpisat.com"]

    # Add development origins
    if config.environment and config.environment.lower() in ["development", "local"]:
        origins.extend(
            [
                "http://localhost:9000",
                "http://localhost:8000",
                "http://127.0.0.1:9000",
                "http://127.0.0.1:8000",
            ]
        )

    return origins


def create_app(routes: list):
    app = FastAPI(debug=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_allowed_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )

    for route in routes:
        app.add_api_route(
            path=route["path"],
            endpoint=route["endpoint"],
            methods=[route["method"]],
            tags=route["tags"],
        )

    for exc, handler in error_handlers:
        register_handler = app.exception_handler(exc)
        register_handler(handler)

    return app


app = create_app(routes=all_routes)
