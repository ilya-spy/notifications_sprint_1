from api.v1.endpoints import admin, client
from fastapi import APIRouter

admin_v1_router = APIRouter()
admin_v1_router.include_router(admin.router, prefix="/admin", tags=["admin"])

client_v1_router = APIRouter()
admin_v1_router.include_router(client.router, prefix="/client", tags=["client"])
