import time
import uuid
from concurrent import futures

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from chores.db import Database
from chores.deps import Container
from chores.errors import AlreadyExists, NotFound
from chores.grpc_generated.chores_pb2 import (
    AddMemberResponse,
    AddMembersPayload,
    CreatePayload,
    CreateResponse,
    DeletePayload,
    DeleteResponse,
    GetMembersResponse,
    GetPayload,
    GetResponse,
    RemoveMemberPayload,
    RemoveMemberResponse,
    UpdatePayload,
    UpdateResponse,
)
from chores.grpc_generated.chores_pb2_grpc import add_HouseServicer_to_server, HouseServicer
from chores.interceptors import ExceptionToStatusInterceptor
from chores.models.house import House, HouseMember
from chores.users_server import _ONE_DAY_IN_SECONDS


class HouseServer(HouseServicer):
    @inject
    def Create(
        self, request: CreatePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> CreateResponse:
        house = House(name=request.name)
        with database.session() as postgres:
            postgres.add(house)
            postgres.commit()

            return CreateResponse(house_id=str(house.id))

    @inject
    def Get(
        self, request: GetPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetResponse:
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()

        if not house:
            raise NotFound("House not found!")

        return GetResponse(house_id=str(house.id), name=house.name)

    @inject
    def Update(
        self, request: UpdatePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateResponse:
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()

            if not house:
                raise NotFound("House not found!")

            house.name = request.name
            db.add(house)
            db.commit()

            return UpdateResponse(house_id=str(house.id))

    @inject
    def Delete(
        self, request: DeletePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteResponse:
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()

            if not house:
                raise NotFound("House not found!")

            db.delete(house)
            db.commit()

            return DeleteResponse(house_id=str(house.id))

    @inject
    def AddMembers(
        self, request: AddMembersPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> AddMemberResponse:
        with database.session() as db:
            house = db.query(House).filter(House.id == request.house_id).one_or_none()
            if not house:
                raise NotFound("House not found!")

            users = db.query(HouseMember).filter(HouseMember.house_id == request.house_id).all()
            user_ids = {str(user.user_id) for user in users}
            for user_id in request.user_ids:
                if user_id in user_ids:
                    raise AlreadyExists(f"User {user_id} already exists in the house {request.house_id}!")

            members = [
                HouseMember(house_id=uuid.UUID(request.house_id), user_id=uuid.UUID(user_ids))
                for user_ids in request.user_ids
            ]
            db.add_all(members)
            try:
                db.flush()
            except IntegrityError:
                raise NotFound("User not found!")
            db.commit()

            return AddMemberResponse(house_id=request.house_id, user_ids=request.user_ids)

    @inject
    def RemoveMember(
        self, request: RemoveMemberPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> RemoveMemberResponse:
        with database.session() as db:
            query = delete(HouseMember).where(
                HouseMember.house_id == request.house_id, HouseMember.user_id == request.user_id
            )
            db.execute(query)
            db.commit()

            return RemoveMemberResponse(user_id=request.user_id, house_id=request.house_id)

    @inject
    def GetMembers(
        self, request: GetPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetMembersResponse:
        with database.session() as db:
            members = db.query(HouseMember).filter(HouseMember.house_id == request.house_id).all()

            return GetMembersResponse(house_id=str(request.house_id), users=[member.user.as_dict for member in members])


def serve():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[ExceptionToStatusInterceptor()])
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
