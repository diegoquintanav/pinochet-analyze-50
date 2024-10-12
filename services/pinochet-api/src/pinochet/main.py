from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pinochet.api.v1.router import api_router
from pinochet.settings import ApiEnvironment, get_settings

# Get the settings from the environment
settings = get_settings()


def configure_graphql(app: FastAPI) -> FastAPI:
    from strawberry.fastapi import GraphQLRouter

    from pinochet.api.v1.graphql import get_context, schema

    graphql_app = GraphQLRouter(schema, context_getter=get_context)
    app.include_router(graphql_app, prefix="/graphql")
    return app


def configure_healthcheck(app: FastAPI) -> FastAPI:
    from fastapi_healthz import (
        HealthCheckRegistry,
        HealthCheckDatabase,
        health_check_route,
    )

    # Add Health Checks
    _healthChecks = HealthCheckRegistry()
    _healthChecks.add(HealthCheckDatabase(uri=settings.db_uri))
    app.add_api_route("/health", endpoint=health_check_route(registry=_healthChecks))
    return app


def configure_sentry(app: FastAPI) -> FastAPI:
    # TODO: implement sentry
    return app


def configure_extensions(app: FastAPI) -> FastAPI:
    app = configure_sentry(app)
    app = configure_healthcheck(app)
    return app


def include_routers(app: FastAPI) -> FastAPI:
    app.include_router(api_router, prefix="/api/v1")


def configure_middleware(
    app: FastAPI,
) -> FastAPI:
    # https://fastapi.tiangolo.com/tutorial/cors/?h=cors#cors-cross-origin-resource-sharing
    if settings.BACKEND_CORS_ORIGINS:
        origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def create_app() -> FastAPI:
    """A wrapper around FastAPI to create the application.

    Returns
    -------
    FastAPI
        A FastAPI application instance.
    """

    title: str = f"Pinochet - Rettig ({settings.API_ENV})"
    openapi_url: str = "/api/v1/openapi.json"
    debug: bool = settings.API_ENV in (ApiEnvironment.DEV, ApiEnvironment.TEST)

    app = FastAPI(
        title=title,
        openapi_url=openapi_url,
        debug=debug,
        version="v1",
    )

    include_routers(app)
    configure_graphql(app)
    configure_middleware(app)
    configure_extensions(app)

    return app


app = create_app()
