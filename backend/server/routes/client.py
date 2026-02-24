from fastapi import APIRouter

from server.business.auth.auth_verifier import AuthVerifier
from server.business.auth.schema import UserTokenInfo
from server.business.client.list import list_clients
from server.business.client.schema import PClient
from server.shared.databasemanager import DatabaseManager
from server.shared.pydantic import PList


def get_router(database: DatabaseManager, auth_verifier: AuthVerifier) -> APIRouter:
    router = APIRouter()

    @router.get("/client")
    async def list_clients_route(
        _: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PList[PClient]:
        with database.create_session() as session:
            clients = list_clients(session)
            return PList(data=clients)

    # ---------------------------
    # Task 1 addition
    # ---------------------------
    @router.get("/client/{client_id}")
    async def show_client_information(
        client_id: str,  # URL parameter
        _: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ):
        with database.create_session() as session:
            client = get_client(session, client_id)  # business function queries DB
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            return client


    return router
