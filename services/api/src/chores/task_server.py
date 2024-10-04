import uuid

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context

from chores.db import Database
from chores.deps import Container
from chores.grpc_generated.chores_pb2 import (
    Cadence,
    CreateChorePayload,
    CreateChoreResponse,
    CreateDistributionPayload,
    CreateDistributionResponse,
    DeleteChorePayload,
    DeleteChoreResponse,
    DeleteDistributionPayload,
    DeleteDistributionResponse,
    GetChorePayload,
    GetChoreResponse,
    GetDistributionPayload,
    GetDistributionResponse,
    UpdateChorePayload,
    UpdateChoreResponse,
    UpdateDistributionPayload,
    UpdateDistributionResponse,
)
from chores.grpc_generated.chores_pb2_grpc import TaskServicer
from chores.models.chore import Chore, ChoreDistribution
from chores.utils import enum_mapper


class TaskServer(TaskServicer):
    @inject
    def CreateChore(
        self, request: CreateChorePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> CreateChoreResponse:
        enum_map = enum_mapper(Cadence)
        chore = Chore(
            name=request.name,
            description=request.description,
            cadence=enum_map[request.cadence],
            start_date=request.start_date,
            end_date=request.end_date,
        )

        with database.session() as postgres:
            postgres.add(chore)
            postgres.commit()

            return CreateChoreResponse(id=str(chore.id))

    @inject
    def GetChore(
        self, request: GetChorePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetChoreResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.id).one_or_none()

        if not chore:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Chore {request.id} not found!")
            return GetChoreResponse()

        return GetChoreResponse(
            id=str(chore.id),
            name=chore.name,
            description=chore.description,
            cadence=chore.cadence,
            start_date=str(chore.start_date),
            end_date=str(chore.end_date),
        )

    @inject
    def UpdateChore(
        self, request: UpdateChorePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateChoreResponse:
        enum_map = enum_mapper(Cadence)
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.id).one_or_none()

            if not chore:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Chore {request.id} not found!")
                return UpdateChoreResponse()

            chore.name = request.name
            chore.description = request.description
            chore.cadence = enum_map[request.cadence]
            chore.start_date = request.start_date
            chore.end_date = request.end_date

            db.add(chore)
            db.commit()

            return UpdateChoreResponse(id=str(chore.id))

    @inject
    def DeleteChore(
        self, request: DeleteChorePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteChoreResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.id).one_or_none()

            if not chore:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Chore {request.id} not found!")
                return DeleteChoreResponse()

            db.delete(chore)
            db.commit()

            return DeleteChoreResponse(id=str(chore.id))

    @inject
    def CreateDistribution(
        self, request: CreateDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> CreateDistributionResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.chore_id).one_or_none()

            if not chore:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Chore {request.id} not found!")
                return CreateDistributionResponse()

            distributions = [
                ChoreDistribution(
                    chore_id=uuid.UUID(request.chore_id),
                    user_id=uuid.UUID(user_id),
                )
                for user_id in request.user_ids
            ]
            db.add_all(distributions)

        return CreateDistributionResponse()

    @inject
    def GetDistribution(
        self, request: GetDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetDistributionResponse:
        pass

    @inject
    def UpdateDistribution(
        self, request: UpdateDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateDistributionResponse:
        pass

    @inject
    def DeleteDistribution(
        self, request: DeleteDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteDistributionResponse:
        pass
