from fastapi import APIRouter
from pinochet.api.v1.endpoints import events, locations, root, victims

api_router = APIRouter()

api_router.include_router(
    root.router,
    tags=["welcome"],
)

api_router.include_router(
    victims.router,
    prefix="/victims",
    tags=["victims", "rettig"],
)

api_router.include_router(
    events.router,
    prefix="/events",
    tags=["events", "rettig"],
)

api_router.include_router(
    locations.router,
    prefix="/locations",
    tags=["locations", "rettig"],
)
