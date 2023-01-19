
import json
from api.schemas.common import DefaultSuccessResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status

from pydantic import ValidationError

from lib.api.v1.admin.notification import IAdminNotification
from lib.model.user import User
from lib.model.notification import Notification

from src.frontend.service.auth_api import AuthApiService, get_auth_api_service
from src.frontend.service.event_storage import EventStorageService, get_event_storage_service
from src.frontend.notifications import get_admin_notifications_service

router = APIRouter()


@router.get(path="/notifications", response_model=DefaultSuccessResponse)
async def get_admin_notifications(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
    admin_notifications_service: IAdminNotification = get_admin_notifications_service(),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    response_body = json.dumps(admin_notifications_service.get_admin_notifications())

    await event_storage_service.send(
        topic_name="admin_log",
        model=Notification,
    )

    return DefaultSuccessResponse(response_body)

@router.post(path="/immediate", response_model=DefaultSuccessResponse)
async def post_immediate(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
    admin_notifications_service: IAdminNotification = get_admin_notifications_service(),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    note_id = request.json()['id']
    note = admin_notifications_service.get_notification(note_id)

    admin_notifications_service.send_immediate([note])
    await event_storage_service.send(
        topic_name="admin_log",
        model=Notification,
    )
    return DefaultSuccessResponse()

@router.post(path="/background", response_model=DefaultSuccessResponse)
async def schedule_background(
    request: Request,
    event_storage_service: EventStorageService = Depends(get_event_storage_service),
    auth_api_service: AuthApiService = Depends(get_auth_api_service),
    admin_notifications_service: IAdminNotification = get_admin_notifications_service(),
) -> DefaultSuccessResponse:
    try:
        user = await auth_api_service.get_user_info(headers=dict(request.headers))
    except (TypeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    note_id = request.json()['id']
    note = admin_notifications_service.get_notification(note_id)

    admin_notifications_service.schedule_background([note])
    await event_storage_service.send(
        topic_name="admin_log",
        model=Notification,
    )
    return DefaultSuccessResponse()
