import random
from unittest.mock import Mock

import pendulum
import pytest
from chores.grpc_generated.chores_pb2 import (
    Cadence,
    GetChoreResponse,
    GetDistributionResponse,
    GetTaskResponse,
)
from chores.grpc_generated.chores_pb2 import Chore as ChoreMessage
from chores.grpc_generated.chores_pb2 import User as UserMessage
from chores_client.views.task.view import get_chore, get_distribution, get_task
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def _chore_payload() -> ChoreMessage:
    return ChoreMessage(
        id="chore-1",
        name="Dishes",
        description="Wash the dishes",
        cadence=Cadence.DAILY,
        start_date="2026-01-01",
        end_date="2026-01-08",
        house_id="house-1",
    )


def _user_payload() -> UserMessage:
    return UserMessage(
        id="user-1",
        email="ada@example.com",
        first_name="Ada",
        last_name="Lovelace",
        sub="auth0|ada",
        picture="",
        nickname="",
    )


class Test_CheckChorePayload:
    def test_it_validates_payload(self, client: TestClient):
        payload = {
            "name": fake.word(),
            "description": fake.sentence(),
            "cadence": random.choice(["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]),
            "startDate": pendulum.now().date().isoformat(),
            "endDate": pendulum.now().date().isoformat(),
            "houseId": fake.uuid4(),
        }

        response = client.post("/chore/choreValidate", json=payload)
        assert response.status_code == 200
        assert response.json() == payload

    @pytest.mark.parametrize(
        "field", ["name", "description", "cadence", "startDate", "endDate", "houseId"]
    )
    def test_it_raises_on_missing_fields(self, client: TestClient, field: str):
        payload = {
            "name": fake.word(),
            "description": fake.sentence(),
            "cadence": random.choice(["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]),
            "startDate": pendulum.now().date().isoformat(),
            "endDate": pendulum.now().date().isoformat(),
            "houseId": fake.uuid4(),
        }
        payload.pop(field)

        response = client.post("/chore/choreValidate", json=payload)
        assert response.status_code == 422
        assert response.json()[field] == ["Field required"]

    def test_it_validates_dates(self, client: TestClient):
        payload = {
            "name": fake.word(),
            "description": fake.sentence(),
            "cadence": random.choice(["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]),
            "startDate": "2021-01-02",
            "endDate": "2020-01-01",
            "houseId": fake.uuid4(),
        }

        response = client.post("/chore/choreValidate", json=payload)
        assert response.status_code == 422
        assert response.json() == {"endDate": ["Value error, End date must be after start date"]}

    def test_it_raises_on_empty_fields(self, client: TestClient):
        payload = {
            "name": "",
            "description": "",
            "cadence": "",
            "startDate": "",
            "endDate": "",
            "houseId": "",
        }

        response = client.post("/chore/choreValidate", json=payload)
        assert response.status_code == 422
        assert response.json() == {
            "name": ["String should have at least 1 character"],
            "description": ["String should have at least 1 character"],
            "cadence": ["Input should be 'DAILY', 'WEEKLY', 'MONTHLY' or 'YEARLY'"],
            "startDate": ["String should have at least 1 character"],
            "endDate": ["String should have at least 1 character"],
            "houseId": ["String should have at least 1 character"],
        }


class Test_CheckDistributionPayload:
    def test_it_validates_payload(self, client: TestClient):
        payload = {"userIds": [fake.uuid4() for _ in range(random.randint(1, 10))]}

        response = client.post("/chore/distributionValidate", json=payload)
        assert response.status_code == 200
        assert response.json() == payload

    def test_it_raises_on_empty_fields(self, client: TestClient):
        payload = {"userIds": []}

        response = client.post("/chore/distributionValidate", json=payload)
        assert response.status_code == 422
        assert response.json() == {
            "userIds": ["List should have at least 1 item after validation, not 0"]
        }


class Test_TaskResponses:
    def test_get_chore_includes_house_id(self):
        client = Mock()
        client.GetChore.return_value = GetChoreResponse(
            id="chore-1",
            name="Dishes",
            description="Wash the dishes",
            cadence=Cadence.DAILY,
            start_date="2026-01-01",
            end_date="2026-01-08",
            house_id="house-1",
        )

        chore = get_chore("chore-1", client, "token")

        assert chore.house_id == "house-1"
        assert chore.cadence == "DAILY"

    def test_get_distribution_includes_house_and_user_sub(self):
        client = Mock()
        client.GetDistribution.return_value = GetDistributionResponse(
            chore=_chore_payload(), users=[_user_payload()]
        )

        distribution = get_distribution("chore-1", client, "token")

        assert distribution.chore.house_id == "house-1"
        assert distribution.users[0].sub == "auth0|ada"
        assert distribution.users[0].picture is None
        assert distribution.users[0].nickname is None

    def test_get_task_includes_house_and_user_sub(self):
        client = Mock()
        client.GetTask.return_value = GetTaskResponse(
            id="task-1",
            due_date="2026-01-02",
            completed_at="",
            chore=_chore_payload(),
            user=_user_payload(),
        )

        task = get_task("task-1", client, "token")

        assert task.chore.house_id == "house-1"
        assert task.user.sub == "auth0|ada"
        assert task.user.picture is None
        assert task.completed_at is None
