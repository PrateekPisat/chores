import time
from concurrent import futures

import grpc
from grpc._server import _Context
from sqlalchemy import delete

from chores.db import Database
from chores.deps import Container
from chores.grpc_generated.house_pb2 import (
    AddMembersPayload,
    AddMembersResponse,
    CreatePayload,
    CreateResponse,
    DeletePayload,
    DeleteResponse,
    GetPayload,
    GetResponse,
    RemoveMemberPayload,
    RemoveMemberResponse,
    UpdatePayload,
    UpdateResponse,
)
from chores.grpc_generated.house_pb2_grpc import add_HouseServicer_to_server, HouseServicer
from chores.models.house import House, HouseMember
from chores.users_server import _ONE_DAY_IN_SECONDS


class HouseServer(HouseServicer):
    def Create(self, request: CreatePayload, context: _Context, database: Database) -> CreateResponse:  # noqa: N802
        house = House(name=request.name)
        with database.session() as postgres:
            postgres.add(house)
            postgres.commit()

            return CreateResponse(house_id=str(house.id))

    def Get(self, request: GetPayload, context: _Context, database: Database) -> GetResponse:  # noqa: N802
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()

        if not house:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("House not found!")
            return GetResponse()

        return GetResponse(house_id=str(house.id), name=house.name)

    def Update(self, request: UpdatePayload, context: _Context, database: Database) -> UpdateResponse:  # noqa: N802
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()

            if not house:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("House not found!")
                return UpdateResponse()

            house.name = request.name
            db.add(house)
            db.commit()

            return UpdateResponse(house_id=str(house.id))

    def Delete(self, request: DeletePayload, context: _Context, database: Database) -> DeleteResponse:  # noqa: N802
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()

            if not house:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("House not found!")
                return DeleteResponse()

            db.delete(house)
            db.commit()

            return DeleteResponse()

    def AddMembers(self, request: AddMembersPayload, context: _Context, database: Database) -> AddMembersResponse:  # noqa: N802
        members = [HouseMember(house_id=request.house_id, user_id=user_ids) for user_ids in request.user_ids]
        with database.session() as db:
            db.add_all(members)
            db.commit()

            return AddMembersResponse(house_id=request.house)

    def RemoveMember(self, request: RemoveMemberPayload, context: _Context, database: Database) -> RemoveMemberResponse:  # noqa: N802
        with database.session() as db:
            query = delete(HouseMember).where(
                HouseMember.house_id == request.house_id, HouseMember.user_id == request.user_id
            )
            db.execute(query)
            db.commit()

            return RemoveMemberResponse(user_id=request.user_id, house_id=request.house_id)


def serve():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HouseServicer_to_server(HouseServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
