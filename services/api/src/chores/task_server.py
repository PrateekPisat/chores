import time
import uuid
from concurrent import futures
from itertools import cycle, zip_longest

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from pydantic import ValidationError
from setuplog import log, setup_logging
from sqlalchemy import delete
from sqlalchemy.orm import selectinload

from chores import schema
from chores.db import Database
from chores.deps import Container
from chores.errors import NotFound
from chores.grpc_generated.chores_pb2 import (
    Cadence,
    CreateChoreErrorsResponse,
    CreateChorePayload,
    CreateChoreResponse,
    CreateDistributionErrorResponse,
    CreateDistributionPayload,
    CreateDistributionResponse,
    DeleteChorePayload,
    DeleteChoreResponse,
    DeleteDistributionPayload,
    DeleteDistributionResponse,
    DeleteTaskPayload,
    DeleteTaskResponse,
    GetChorePayload,
    GetChoreResponse,
    GetDistributionPayload,
    GetDistributionResponse,
    GetTaskPayload,
    GetTaskResponse,
    UpdateChoreErrorsResponse,
    UpdateChorePayload,
    UpdateChoreResponse,
    UpdateDistributionPayload,
    UpdateDistributionResponse,
    UpdateTaskPayload,
    UpdateTaskResponse,
)
from chores.grpc_generated.chores_pb2 import (
    Chore as ChorePayload,
)
from chores.grpc_generated.chores_pb2 import (
    User as UserPayload,
)
from chores.grpc_generated.chores_pb2_grpc import add_TaskServicer_to_server, TaskServicer
from chores.interceptors import ExceptionToStatusInterceptor
from chores.models.chore import Chore, ChoreDistribution, Task
from chores.users_server import _ONE_DAY_IN_SECONDS
from chores.utils import distribution_needs_update, enum_mapper, get_intervals, parse_errors


class TaskServer(TaskServicer):
    def ValidateCreateChorePayload(self, request: CreateChorePayload, context: _Context) -> CreateChoreErrorsResponse:
        try:
            schema.CreateChorePayload(
                name=request.name,
                description=request.description,
                cadence=request.cadence,
                start_date=request.start_date,
                end_date=request.end_date,
            )
        except ValidationError as e:
            return CreateChoreErrorsResponse(**parse_errors(e))

        return CreateChoreErrorsResponse()

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
            raise NotFound(f"Chore {request.id} not found!")

        return GetChoreResponse(
            id=str(chore.id),
            name=chore.name,
            description=chore.description,
            cadence=chore.cadence,
            start_date=chore.start_date.isoformat(),
            end_date=chore.end_date.isoformat(),
        )

    def ValidateUpdateChorePayload(self, request: UpdateChorePayload, context: _Context) -> UpdateChoreErrorsResponse:
        try:
            schema.UpdateChorePayload(
                id=request.id,
                name=request.name,
                description=request.description,
                cadence=request.cadence,
                start_date=request.start_date,
                end_date=request.end_date,
            )
        except ValidationError as e:
            return UpdateChoreErrorsResponse(**parse_errors(e))

        return UpdateChoreErrorsResponse()

    @inject
    def UpdateChore(
        self, request: UpdateChorePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateChoreResponse:
        enum_map = enum_mapper(Cadence)
        with database.session() as db:
            chore = (
                db.query(Chore).options(selectinload(Chore.distributions)).filter(Chore.id == request.id).one_or_none()
            )

            if not chore:
                raise NotFound(f"Chore {request.id} not found!")

            needs_update = distribution_needs_update(chore, request, enum_map)

            chore.name = request.name
            chore.description = request.description
            chore.cadence = enum_map[request.cadence]
            chore.start_date = request.start_date
            chore.end_date = request.end_date
            db.add(chore)
            db.commit()

            if needs_update and chore.distributions:
                update_distribution_request = UpdateDistributionPayload(
                    chore_id=str(chore.id), user_ids=[str(distribution.user_id) for distribution in chore.distributions]
                )
                self.UpdateDistribution(update_distribution_request, context)

            return UpdateChoreResponse(id=str(chore.id))

    @inject
    def DeleteChore(
        self, request: DeleteChorePayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteChoreResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.id).one_or_none()

            if not chore:
                raise NotFound(f"Chore {request.id} not found!")

            db.delete(chore)
            db.commit()

            return DeleteChoreResponse(id=str(chore.id))

    def ValidateCreateDistributionPayload(
        self, request: CreateDistributionPayload, context: _Context
    ) -> CreateDistributionErrorResponse:
        try:
            CreateDistributionPayload(chore_id=request.chore_id, user_ids=request.user_ids)
        except ValidationError as e:
            return CreateDistributionErrorResponse(**parse_errors(e))

        return CreateDistributionErrorResponse()

    @inject
    def CreateDistribution(
        self, request: CreateDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> CreateDistributionResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.chore_id).one_or_none()

            if not chore:
                raise NotFound(f"Chore {request.chore_id} not found!")

            distributions = [
                ChoreDistribution(chore_id=uuid.UUID(request.chore_id), user_id=uuid.UUID(user_id))
                for user_id in request.user_ids
            ]
            db.add_all(distributions)

            for due_date, distribution in zip_longest(
                get_intervals(chore.start_date, chore.end_date, chore.cadence), cycle(distributions), fillvalue=None
            ):
                if not due_date:
                    break
                task = Task(chore_distribution=distribution, due_date=due_date)
                db.add(task)

            db.commit()

            return CreateDistributionResponse(id=str(chore.id))

    @inject
    def GetDistribution(
        self, request: GetDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetDistributionResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.id).one_or_none()

            if not chore:
                raise NotFound(f"Chore {request.id} not found!")

            distributions = db.query(ChoreDistribution).filter(ChoreDistribution.chore_id == chore.id).all()
            return GetDistributionResponse(
                chore=ChorePayload(
                    id=str(chore.id),
                    name=chore.name,
                    description=chore.description,
                    cadence=chore.cadence,
                    start_date=chore.start_date.isoformat(),
                    end_date=chore.end_date.isoformat(),
                ),
                users=[
                    UserPayload(
                        id=str(distribution.user.id),
                        email=distribution.user.email,
                        first_name=distribution.user.first_name,
                        last_name=distribution.user.last_name,
                    )
                    for distribution in distributions
                ],
            )

    def ValidateUpdateDistributionPayload(
        self, request: UpdateDistributionPayload, context: _Context
    ) -> CreateDistributionErrorResponse:
        try:
            schema.UpdateDistributionPayload(chore_id=request.chore_id, user_ids=request.user_ids)
        except ValidationError as e:
            return CreateDistributionErrorResponse(**parse_errors(e))

        return CreateDistributionErrorResponse()

    @inject
    def UpdateDistribution(
        self, request: UpdateDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateDistributionResponse:
        with database.session() as db:
            chore = db.query(Chore).filter(Chore.id == request.chore_id).one_or_none()

            if not chore:
                raise NotFound(f"Chore {request.chore_id} not found!")

            db.execute(delete(ChoreDistribution).where(ChoreDistribution.chore_id == chore.id))

            distributions = [
                ChoreDistribution(chore_id=uuid.UUID(request.chore_id), user_id=uuid.UUID(user_id))
                for user_id in request.user_ids
            ]
            db.add_all(distributions)

            for due_date, distribution in zip_longest(
                get_intervals(chore.start_date, chore.end_date, chore.cadence), cycle(distributions), fillvalue=None
            ):
                if not due_date:
                    break
                task = Task(chore_distribution=distribution, due_date=due_date)
                db.add(task)

            db.commit()

            return UpdateDistributionResponse(id=str(chore.id))

    @inject
    def DeleteDistribution(
        self, request: DeleteDistributionPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteDistributionResponse:
        with database.session() as db:
            distributions = db.query(ChoreDistribution).filter(ChoreDistribution.chore_id == request.id).all()

            if not distributions:
                raise NotFound(f"Chore {request.id} not found!")

            for distribution in distributions:
                db.delete(distribution)
            db.commit()

            return DeleteDistributionResponse(id=request.id)

    def GetTask(
        self, request: GetTaskPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetTaskResponse:
        with database.session() as db:
            task = (
                db.query(Task)
                .options(
                    selectinload(Task.chore_distribution).selectinload(ChoreDistribution.user),
                    selectinload(Task.chore_distribution).selectinload(ChoreDistribution.chore),
                )
                .filter(Task.id == request.id)
                .one_or_none()
            )

            if not task:
                raise NotFound(f"Task {request.id} not found!")

            return GetTaskResponse(
                id=str(task.id),
                due_date=task.due_date.isoformat(),
                completed_at=task.completed_at.isoformat(),
                chore=ChorePayload(
                    id=str(task.chore_distribution.chore.id),
                    name=task.chore_distribution.chore.name,
                    description=task.chore_distribution.chore.description,
                    cadence=task.chore_distribution.chore.cadence,
                    start_date=task.chore_distribution.chore.start_date.isoformat(),
                    end_date=task.chore_distribution.chore.end_date.isoformat(),
                ),
                user=UserPayload(
                    id=str(task.chore_distribution.user.id),
                    email=task.chore_distribution.user.email,
                    first_name=task.chore_distribution.user.first_name,
                    last_name=task.chore_distribution.user.last_name,
                ),
            )

    def UpdateTask(
        self, request: UpdateTaskPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateTaskResponse:
        with database.session() as db:
            task = db.query(Task).filter(Task.id == request.id).one_or_none()

            if not task:
                raise NotFound(f"Task {request.id} not found!")

            task.due_date = request.due_date
            task.completed_at = request.completed_at

            db.add(task)
            db.commit()

            return UpdateTaskResponse(id=str(task.id))

    def DeleteTask(
        self, request: DeleteTaskPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteTaskResponse:
        with database.session() as db:
            task = db.query(Task).filter(Task.id == request.id).one_or_none()

            if not task:
                raise NotFound(f"Task {request.id} not found!")

            db.delete(task)
            db.commit()

            return DeleteTaskResponse(id=str(task.id))


def serve():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    config = container.config()
    setup_logging(
        log_level=config.logging.level,
        namespace="chores.task_server",
        style=" %(name)s :: %(levelname)-8s :: %(message)s",
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[ExceptionToStatusInterceptor()])
    add_TaskServicer_to_server(TaskServer(), server)
    server.add_insecure_port(f"[::]:{config.task_service_port}")
    server.start()
    log.info("Task server started on port %s", config.task_service_port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
