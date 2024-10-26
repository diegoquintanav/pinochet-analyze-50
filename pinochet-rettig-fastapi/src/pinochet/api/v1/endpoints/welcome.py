from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=Any, status_code=201)
def get_welcome() -> Any:
    """
    Get a welcome message
    """

    return {
        "message": "Welcome to the Pinochet API v1. See the api docs at /docs.",
    }
