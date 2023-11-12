from fastapi import FastAPI
from pinochet.api.v1.api import api_router
from pinochet.settings import ApiEnvironment, settings
from starlette.middleware.cors import CORSMiddleware


def configure_graphql(app: FastAPI) -> FastAPI:
    from pinochet.api.v1.endpoints.graphql import schema
    from strawberry.fastapi import GraphQLRouter

    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    return app


def configure_sentry(app: FastAPI) -> FastAPI:
    ...


def configure_extensions(app: FastAPI) -> FastAPI:
    configure_sentry(app)


def include_routers(app: FastAPI) -> FastAPI:
    app.include_router(api_router, prefix=settings.api_v1_str)


def configure_middleware(app: FastAPI) -> FastAPI:
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


def create_app(
    title: str = settings.project_name,
    openapi_url: str = f"{settings.api_v1_str}/openapi.json",
    debug: bool = settings.API_ENV in (ApiEnvironment.DEV, ApiEnvironment.TEST),
) -> FastAPI:
    app = FastAPI(
        title=title,
        openapi_url=openapi_url,
        debug=debug,
        version=settings.API_VERSION,
    )

    include_routers(app)
    configure_graphql(app)
    configure_middleware(app)
    configure_extensions(app)

    return app


app = create_app()
