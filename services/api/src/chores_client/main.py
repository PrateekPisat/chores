from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chores_client.responses import error_handlers
from chores_client.routes import all_routes


def create_app(routes: list):
    app = FastAPI(debug=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
