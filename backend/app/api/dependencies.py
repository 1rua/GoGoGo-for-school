from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.shared_nfc_service import SharedNfcService
from app.application.services.shared_route_service import SharedRouteService
from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.shared_nfc_sql_repository import SharedNfcSqlRepository
from app.infrastructure.repositories.shared_route_sql_repository import SharedRouteSqlRepository


def get_route_service(db: Session = Depends(get_db_session)) -> SharedRouteService:
    return SharedRouteService(SharedRouteSqlRepository(db))


def get_nfc_service(db: Session = Depends(get_db_session)) -> SharedNfcService:
    return SharedNfcService(SharedNfcSqlRepository(db))
