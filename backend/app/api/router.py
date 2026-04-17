from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.health import router as health_router
from app.api.routes.shared_nfc import router as shared_nfc_router
from app.api.routes.shared_routes import router as shared_routes_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(admin_router, tags=["admin"])
api_router.include_router(shared_routes_router, prefix="/shared/routes", tags=["shared-routes"])
api_router.include_router(shared_nfc_router, prefix="/shared/nfc", tags=["shared-nfc"])
