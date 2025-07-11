import uuid

import grpc
import pendulum
import pytest
from chores.config import Config
from chores.grpc_generated.chores_pb2 import (
    Cadence,
    CreateChorePayload,
    CreateDistributionPayload,
    DeleteDistributionPayload,
    GetChorePayload,
    GetDistributionPayload,
    GetDistributionResponse,
    GetTaskPayload,
    ListChorePayload,
    ListTaskPayload,
    UpdateChorePayload,
    UpdateDistributionPayload,
    UpdateTaskPayload,
)
from chores.grpc_generated.chores_pb2_grpc import TaskStub
from chores.models.chore import Chore, ChoreDistribution, Task
from chores.utils import enum_mapper, get_token_payload
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory


class Test_Chores:
    def test_it_creates_a_chore(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        now = pendulum.now()

        token = get_token_payload(user, config.cryptography.secret_key)
        request = CreateChorePayload(
            name="Chore 1",
            description="Chore 1 description",
            cadence=Cadence.DAILY,
            start_date=now.date().isoformat(),
            end_date=now.add(days=7).date().isoformat(),
            house_id=str(house.id),  # Ensure we have a house for the chore
        )

        response = task_service.CreateChore(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.id

        chore = db.query(Chore).filter(Chore.id == response.id).one_or_none()
        assert chore
        assert chore.name == request.name
        assert chore.description == request.description
        assert chore.cadence == "DAILY"
        assert chore.start_date

    def test_it_lists_chores(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        chore = mf.chore.chore(house=house)
        mf.chore.chore()  # Create another chore to ensure we have multiple
        token = get_token_payload(user, config.cryptography.secret_key)
        request = ListChorePayload(house_id=str(house.id))

        response = task_service.ListChores(request, metadata=(("authorization", f"Bearer {token}"),))

        assert len(response.chores) == 1
        for c in response.chores:
            assert c.id == str(chore.id)
            assert c.name == chore.name
            assert c.description == chore.description
            assert c.cadence == Cadence.Value(chore.cadence)
            assert c.start_date == chore.start_date.isoformat()
            assert c.end_date == chore.end_date.isoformat()
            assert c.house_id == str(house.id)

    def test_it_lists_user_chores(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        house1 = mf.house.house()
        house2 = mf.house.house()
        chore1 = mf.chore.chore(house=house1)
        chore2 = mf.chore.chore(house=house2)
        mf.chore.chore()  # Create another chore to ensure we have multiple
        mf.house.house_member(house_id=house1.id, user_id=user.id)
        mf.house.house_member(house_id=house2.id, user_id=user.id)
        token = get_token_payload(user, config.cryptography.secret_key)
        request = ListChorePayload(user_id=str(user.id))

        response = task_service.ListChores(request, metadata=(("authorization", f"Bearer {token}"),))

        assert len(response.chores) == 2
        assert {str(c.id) for c in response.chores} == {str(chore1.id), str(chore2.id)}

    def test_it_gets_a_chore(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        chore = mf.chore.chore()
        token = get_token_payload(user, config.cryptography.secret_key)
        request = GetChorePayload(id=str(chore.id))

        response = task_service.GetChore(request, metadata=(("authorization", f"Bearer {token}"),))

        enum_map = enum_mapper(Cadence)
        assert response.id == str(chore.id)
        assert response.name == chore.name
        assert response.description == chore.description
        assert enum_map[response.cadence] == chore.cadence
        assert response.start_date == str(chore.start_date)
        assert response.end_date == str(chore.end_date)

    def test_it_raises_on_missing_chore(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = GetChorePayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.GetChore(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"

    def test_it_updates_a_chore(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        chore = mf.chore.chore(house=house)
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateChorePayload(
            id=str(chore.id),
            name="Chore 2",
            description="Chore 2 description",
            cadence=Cadence.WEEKLY,
            start_date=pendulum.now().date().isoformat(),
            end_date=pendulum.now().add(days=7).date().isoformat(),
            house_id=str(house.id),  # Ensure we have a house for the chore
        )

        response = task_service.UpdateChore(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(chore.id)

        db.expunge_all()
        chore = db.query(Chore).filter(Chore.id == chore.id).one_or_none()
        assert chore.name == request.name
        assert chore.description == request.description
        assert chore.cadence == "WEEKLY"
        assert chore.start_date.isoformat() == request.start_date
        assert chore.end_date.isoformat() == request.end_date

    def test_it_updates_a_chore_with_distribution(
        self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory
    ):
        now = pendulum.now()
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        chore = mf.chore.chore(house=house, cadence="DAILY", start_date=now.date(), end_date=now.add(days=7).date())
        user = mf.user.user()
        mf.chore.distribution(chore=chore, user=user)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateChorePayload(
            id=str(chore.id),
            name="Chore 2",
            description="Chore 2 description",
            cadence=Cadence.WEEKLY,
            start_date=pendulum.now().date().isoformat(),
            end_date=pendulum.now().add(weeks=2).date().isoformat(),
            house_id=str(house.id),  # Ensure we have a house for the chore
        )
        response = task_service.UpdateChore(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(chore.id)

        db.expunge_all()
        chore = db.query(Chore).filter(Chore.id == chore.id).one_or_none()
        assert chore.name == request.name
        assert chore.description == request.description
        assert chore.cadence == "WEEKLY"
        assert chore.start_date.isoformat() == request.start_date
        assert chore.end_date.isoformat() == request.end_date

        tasks = (
            db.query(Task)
            .join(ChoreDistribution)
            .filter(ChoreDistribution.chore_id == chore.id)
            .order_by(Task.due_date)
            .all()
        )
        assert len(tasks) == 2

        for i, task in enumerate(tasks, start=1):
            assert task.due_date == now.add(weeks=i).date()

    def test_it_raises_on_missing_chore_for_update(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateChorePayload(
            id=str(uuid.uuid4()),
            name="Chore 2",
            description="Chore 2 description",
            cadence=Cadence.WEEKLY,
            start_date=pendulum.now().date().isoformat(),
            house_id=str(house.id),  # Ensure we have a house for the chore
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.UpdateChore(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"

    def test_it_deletes_a_chore(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        chore = mf.chore.chore()
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateChorePayload(id=str(chore.id))

        response = task_service.DeleteChore(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.id == str(chore.id)

        chore = db.query(Chore).filter(Chore.id == chore.id).one_or_none()
        assert chore is None

    def test_it_raises_on_missing_chore_for_delete(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateChorePayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.DeleteChore(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"


class Test_ChoreDistribution:
    def test_it_distributes_a_chore(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        now = pendulum.now()
        user = mf.user.user(email="test@example.com")
        chore = mf.chore.chore(start_date=now.date(), end_date=now.add(days=7).date(), cadence="DAILY")
        user1 = mf.user.user()
        user2 = mf.user.user()

        token = get_token_payload(user, config.cryptography.secret_key)
        request = CreateDistributionPayload(chore_id=str(chore.id), user_ids=[str(user1.id), str(user2.id)])
        response = task_service.CreateDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(chore.id)

        chore_distribution = db.query(ChoreDistribution).filter(ChoreDistribution.chore_id == chore.id).all()
        assert len(chore_distribution) == 2
        assert chore_distribution[0].user_id == user1.id
        assert chore_distribution[1].user_id == user2.id

        tasks = (
            db.query(Task)
            .join(ChoreDistribution)
            .filter(ChoreDistribution.chore_id == chore.id)
            .order_by(Task.due_date)
            .all()
        )
        assert len(tasks) == 7

        for i, task in enumerate(tasks, start=1):
            assert task.chore_distribution_id in [c.id for c in chore_distribution]
            assert task.due_date == now.add(days=i).date()

    def test_it_raises_on_missing_chore_for_distribution(
        self, task_service: TaskStub, config: Config, mf: ModelFactory
    ):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = CreateDistributionPayload(chore_id=str(uuid.uuid4()), user_ids=[str(uuid.uuid4())])

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.CreateDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.chore_id} not found!"

    def test_it_gets_a_distribution(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        chore = mf.chore.chore(cadence="DAILY")
        user = mf.user.user()
        mf.chore.distribution(chore=chore, user=user)
        token = get_token_payload(user, config.cryptography.secret_key)
        request = GetDistributionPayload(id=str(chore.id))

        response: GetDistributionResponse = task_service.GetDistribution(
            request, metadata=(("authorization", f"Bearer {token}"),)
        )

        assert response
        assert response.chore.id == str(chore.id)
        assert response.chore.name == chore.name
        assert response.chore.description == chore.description
        assert response.chore.cadence == 0  # DAILY
        assert response.chore.start_date == chore.start_date.isoformat()
        assert response.chore.end_date == chore.end_date.isoformat()

        assert len(response.users) == 1
        assert response.users[0].id == str(user.id)
        assert response.users[0].email == user.email
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name

    def test_it_raises_on_missing_distribution(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = GetDistributionPayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.GetDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"

    def test_it_updates_distribution(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        now = pendulum.now()
        chore = mf.chore.chore(cadence="DAILY", start_date=now.date(), end_date=now.add(days=7).date())
        user1 = mf.user.user()
        user2 = mf.user.user()
        mf.chore.distribution(chore=chore, user=user1)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateDistributionPayload(chore_id=str(chore.id), user_ids=[str(user1.id), str(user2.id)])
        response = task_service.UpdateDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(chore.id)

        chore_distribution = db.query(ChoreDistribution).filter(ChoreDistribution.chore_id == chore.id).all()
        assert len(chore_distribution) == 2
        assert chore_distribution[0].user_id == user1.id
        assert chore_distribution[1].user_id == user2.id

        tasks = (
            db.query(Task)
            .join(ChoreDistribution)
            .filter(ChoreDistribution.chore_id == chore.id)
            .order_by(Task.due_date)
            .all()
        )
        assert len(tasks) == 7

        for i, task in enumerate(tasks, start=1):
            assert task.chore_distribution_id in [c.id for c in chore_distribution]
            assert task.due_date == now.add(days=i).date()

    def test_it_raises_on_missing_chore_for_update(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateDistributionPayload(chore_id=str(uuid.uuid4()), user_ids=[str(uuid.uuid4())])

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.UpdateDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.chore_id} not found!"

    def test_it_deletes_distribution(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        chore = mf.chore.chore(cadence="DAILY")
        user = mf.user.user()
        mf.chore.distribution(chore=chore, user=user)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = DeleteDistributionPayload(id=str(chore.id))
        response = task_service.DeleteDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(chore.id)

        chore_distribution = db.query(ChoreDistribution).filter(ChoreDistribution.chore_id == chore.id).all()
        assert len(chore_distribution) == 0

    def test_it_raises_on_missing_chore_for_delete(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = DeleteDistributionPayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.DeleteDistribution(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Chore {request.id} not found!"


class Test_Task:
    def test_it_lists_tasks(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        now = pendulum.now()
        chore = mf.chore.chore(cadence="DAILY", start_date=now.date(), end_date=now.add(days=1).date())
        user = mf.user.user()
        distribution = mf.chore.distribution(chore=chore, user=user)
        task = mf.chore.task(chore_distribution=distribution)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = ListTaskPayload(user_id=str(user.id))
        response = task_service.ListTasks(request, metadata=(("authorization", f"Bearer {token}"),))

        assert len(response.tasks) == 1
        for t in response.tasks:
            assert t.id == str(task.id)
            assert t.due_date == task.due_date.isoformat()
            assert not t.completed_at
            assert t.user.id == str(user.id)
            assert t.user.email == user.email
            assert t.user.first_name == user.first_name
            assert t.user.last_name == user.last_name
            assert t.chore.id == str(chore.id)
            assert t.chore.name == chore.name
            assert t.chore.description == chore.description
            assert t.chore.cadence == 0
            assert t.chore.start_date == chore.start_date.isoformat()
            assert t.chore.end_date == chore.end_date.isoformat()

    def test_it_gets_a_task(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        now = pendulum.now()
        chore = mf.chore.chore(cadence="DAILY", start_date=now.date(), end_date=now.add(days=1).date())
        user = mf.user.user()
        distribution = mf.chore.distribution(chore=chore, user=user)
        task = mf.chore.task(chore_distribution=distribution, completed_at=now)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = GetTaskPayload(id=str(task.id))
        response = task_service.GetTask(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response
        assert response.id == str(task.id)
        assert response.due_date == task.due_date.isoformat()
        assert response.completed_at == task.completed_at.isoformat()
        assert response.user.id == str(user.id)
        assert response.user.email == user.email
        assert response.user.first_name == user.first_name
        assert response.user.last_name == user.last_name
        assert response.chore.id == str(chore.id)
        assert response.chore.name == chore.name
        assert response.chore.description == chore.description
        assert response.chore.cadence == 0
        assert response.chore.start_date == chore.start_date.isoformat()
        assert response.chore.end_date == chore.end_date.isoformat()

    def test_it_raises_on_missing_task(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = GetTaskPayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.GetTask(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Task {request.id} not found!"

    def test_it_updates_a_task(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        now = pendulum.now("America/New_York")
        chore = mf.chore.chore(cadence="DAILY", start_date=now.date(), end_date=now.add(days=1).date())
        user = mf.user.user()
        distribution = mf.chore.distribution(chore=chore, user=user)
        task = mf.chore.task(chore_distribution=distribution)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateTaskPayload(
            id=str(task.id),
            due_date=now.add(days=2).date().isoformat(),
            completed_at=now.add(days=1).isoformat(),
        )
        response = task_service.UpdateTask(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(task.id)

        db.expunge_all()
        tasks = db.query(Task).filter(Task.id == task.id).all()
        assert len(tasks) == 1
        assert tasks[0].due_date.isoformat() == request.due_date
        assert (
            pendulum.instance(tasks[0].completed_at).in_timezone("America/New_York").isoformat() == request.completed_at
        )

    def test_it_raises_on_missing_task_for_update(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateTaskPayload(
            id=str(uuid.uuid4()),
            due_date=pendulum.now().add(days=2).date().isoformat(),
            completed_at=pendulum.now().add(days=1).isoformat(),
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.UpdateTask(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Task {request.id} not found!"

    def test_it_deletes_a_task(self, task_service: TaskStub, db: Session, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        now = pendulum.now()
        chore = mf.chore.chore(cadence="DAILY", start_date=now.date(), end_date=now.add(days=1).date())
        user = mf.user.user()
        distribution = mf.chore.distribution(chore=chore, user=user)
        task = mf.chore.task(chore_distribution=distribution)

        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateTaskPayload(id=str(task.id))
        response = task_service.DeleteTask(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.id == str(task.id)

        tasks = db.query(Task).filter(Task.id == task.id).all()
        assert len(tasks) == 0

    def test_it_raises_on_missing_task_for_delete(self, task_service: TaskStub, config: Config, mf: ModelFactory):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = UpdateTaskPayload(id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            task_service.DeleteTask(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"Task {request.id} not found!"
