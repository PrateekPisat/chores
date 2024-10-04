import uuid

import grpc
import pendulum
import pytest
from chores.grpc_generated.chores_pb2 import Cadence, CreateChorePayload, GetChorePayload, UpdateChorePayload
from chores.grpc_generated.chores_pb2_grpc import TaskStub
from chores.models.chore import Chore
from chores.utils import enum_mapper
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory


class Test_Chores:
    def test_it_creates_a_chore(self, task_service: TaskStub, db: Session):
        now = pendulum.now()

        request = CreateChorePayload(
            name="Chore 1",
            description="Chore 1 description",
            cadence=Cadence.DAILY,
            start_date=now.date().isoformat(),
            end_date=now.add(days=7).date().isoformat(),
        )

        response = task_service.CreateChore(request)
        assert response.id

        chore = db.query(Chore).filter(Chore.id == response.id).one_or_none()
        assert chore
        assert chore.name == request.name
        assert chore.description == request.description
        assert chore.cadence == "DAILY"
        assert chore.start_date

    def test_it_gets_a_chore(self, task_service: TaskStub, db: Session, mf: ModelFactory):
        chore = mf.chore.chore()
        request = GetChorePayload(id=str(chore.id))

        response = task_service.GetChore(request)

        enum_map = enum_mapper(Cadence)
        assert response.id == str(chore.id)
        assert response.name == chore.name
        assert response.description == chore.description
        assert enum_map[response.cadence] == chore.cadence
        assert response.start_date == str(chore.start_date)
        assert response.end_date == str(chore.end_date)

    def test_it_raises_on_missing_chore(self, task_service: TaskStub):
        request = GetChorePayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.GetChore(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"

    def test_it_updates_a_chore(self, task_service: TaskStub, db: Session, mf: ModelFactory):
        chore = mf.chore.chore()
        request = UpdateChorePayload(
            id=str(chore.id),
            name="Chore 2",
            description="Chore 2 description",
            cadence=Cadence.WEEKLY,
            start_date=pendulum.now().date().isoformat(),
            end_date=pendulum.now().add(days=7).date().isoformat(),
        )

        response = task_service.UpdateChore(request)

        assert response.id == str(chore.id)

        db.expunge_all()
        chore = db.query(Chore).filter(Chore.id == chore.id).one_or_none()
        assert chore.name == request.name
        assert chore.description == request.description
        assert chore.cadence == "WEEKLY"
        assert chore.start_date.isoformat() == request.start_date
        assert chore.end_date.isoformat() == request.end_date

    def test_it_raises_on_missing_chore_for_update(self, task_service: TaskStub):
        request = UpdateChorePayload(
            id=str(uuid.uuid4()),
            name="Chore 2",
            description="Chore 2 description",
            cadence=Cadence.WEEKLY,
            start_date=pendulum.now().date().isoformat(),
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.UpdateChore(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"

    def test_it_deletes_a_chore(self, task_service: TaskStub, db: Session, mf: ModelFactory):
        chore = mf.chore.chore()
        request = UpdateChorePayload(id=str(chore.id))

        response = task_service.DeleteChore(request)
        assert response.id == str(chore.id)

        chore = db.query(Chore).filter(Chore.id == chore.id).one_or_none()
        assert chore is None

    def test_it_raises_on_missing_chore_for_delete(self, task_service: TaskStub):
        request = UpdateChorePayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.DeleteChore(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"


class Test_ChoreDistribution: ...


class Test_Task: ...
