from app.application.interfaces.shared_route_repository import SharedRouteRepository
from app.application.schemas.route_schemas import (
    CreateSharedRouteRequest,
    SharedRouteDetailResponse,
)
from app.core.exceptions import ResourceNotFoundError


class AdminRouteService:
    def __init__(self, repository: SharedRouteRepository):
        self._repository = repository

    def list_routes(self) -> list[SharedRouteDetailResponse]:
        return self._repository.list_route_details()

    def update_route(self, route_id: str, payload: CreateSharedRouteRequest) -> SharedRouteDetailResponse:
        route = self._repository.update_route(route_id, payload)
        if route is None:
            raise ResourceNotFoundError(f"Shared route '{route_id}' was not found.")
        return route

    def delete_route(self, route_id: str) -> None:
        deleted = self._repository.delete_route(route_id)
        if not deleted:
            raise ResourceNotFoundError(f"Shared route '{route_id}' was not found.")
