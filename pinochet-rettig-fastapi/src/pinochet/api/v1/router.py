from fastapi import APIRouter, Depends
from pinochet.api.deps import get_current_active_user
from pinochet.api.v1.endpoints import auth, events, locations, users, victims, welcome

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)

api_router.include_router(
    welcome.router,
    tags=["welcome"],
)

api_router.include_router(
    victims.router,
    prefix="/victims",
    tags=["victims"],
    dependencies=[Depends(get_current_active_user)],
)

api_router.include_router(
    events.router,
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(get_current_active_user)],
)

api_router.include_router(
    locations.router,
    prefix="/locations",
    tags=["locations"],
    dependencies=[Depends(get_current_active_user)],
)
