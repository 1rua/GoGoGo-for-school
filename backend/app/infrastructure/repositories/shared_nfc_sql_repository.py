from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.application.interfaces.shared_nfc_repository import SharedNfcRepository
from app.application.schemas.nfc_schemas import CreateSharedNfcRequest, SharedNfcResponse
from app.core.id_generator import generate_public_id
from app.infrastructure.db.models.nfc import SharedNfcModel


class SharedNfcSqlRepository(SharedNfcRepository):
    def __init__(self, db: Session):
        self._db = db

    def list_entries(self) -> list[SharedNfcResponse]:
        rows = self._db.query(SharedNfcModel).order_by(SharedNfcModel.created_at.desc()).all()
        return [self._to_response(row) for row in rows]

    def create_entry(self, payload: CreateSharedNfcRequest) -> SharedNfcResponse:
        now = int(datetime.now(timezone.utc).timestamp() * 1000)
        entry = SharedNfcModel(
            id=generate_public_id("nfc"),
            name=payload.name,
            url=payload.url,
            package_name=payload.packageName,
            source=payload.source,
            created_at=now,
        )
        self._db.add(entry)
        self._db.commit()
        self._db.refresh(entry)
        return self._to_response(entry)

    def update_entry(self, entry_id: str, payload: CreateSharedNfcRequest) -> SharedNfcResponse | None:
        entry = self._db.query(SharedNfcModel).filter(SharedNfcModel.id == entry_id).first()
        if entry is None:
            return None
        entry.name = payload.name
        entry.url = payload.url
        entry.package_name = payload.packageName
        entry.source = payload.source
        self._db.commit()
        self._db.refresh(entry)
        return self._to_response(entry)

    def delete_entry(self, entry_id: str) -> bool:
        entry = self._db.query(SharedNfcModel).filter(SharedNfcModel.id == entry_id).first()
        if entry is None:
            return False
        self._db.delete(entry)
        self._db.commit()
        return True

    def _to_response(self, row: SharedNfcModel) -> SharedNfcResponse:
        return SharedNfcResponse(
            id=row.id,
            name=row.name,
            url=row.url,
            packageName=row.package_name,
            source=row.source,
            createdAt=row.created_at,
        )
