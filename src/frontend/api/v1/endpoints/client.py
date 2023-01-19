
import json
from api.schemas.common import DefaultSuccessResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status

from pydantic import ValidationError

from lib.api.v1.frontend.notification import IClientNotification
from lib.model.user import User
from lib.model.notification import Notification

from src.frontend.service.auth_api import AuthApiService, get_auth_api_service
from src.frontend.service.event_storage import EventStorageService, get_event_storage_service
from src.frontend.notifications import get_client_notifications_service

router = APIRouter()


@router.post(path="/immediate", response_model=DefaultSuccessResponse)
async def post_immediate(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
    notifications_service: IClientNotification = get_client_notifications_service(),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    note_id = request.json()['id']
    notifications_service.send_notification(note_id)

    await event_storage_service.send(
        topic_name="client_log",
        model=Notification,
    )
    return DefaultSuccessResponse()

@router.post(path="/immediate", response_model=DefaultSuccessResponse)
async def post_user_immediate(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
    notifications_service: IClientNotification = get_client_notifications_service(),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    note_id = request.json()['note_id']
    user_id = request.json()['user_id']
    notifications_service.user_notification(note_id, user_id)

    await event_storage_service.send(
        topic_name="client_log",
        model=Notification,
    )
    return DefaultSuccessResponse()

@router.post(path="/background", response_model=DefaultSuccessResponse)
async def schedule_background(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
    notifications_service: IClientNotification = get_client_notifications_service(),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    user_id = request.json()['user_id']
    event_id = request.json()['event_id']
    notifications_service.user_event(user_id, event_id)

    await event_storage_service.send(
        topic_name="client_log",
        model=Notification,
    )
    return DefaultSuccessResponse()
