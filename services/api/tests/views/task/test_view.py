import random

import pendulum
import pytest
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


class Test_CheckChorePayload:
    def test_it_validates_payload(self, client: TestClient):
        payload = {
            "name": fake.word(),
            "description": fake.sentence(),
            "cadence": random.choice(["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]),
            "startDate": pendulum.now().date().isoformat(),
            "endDate": pendulum.now().date().isoformat(),
        }

        response = client.post("/chore/choreValidate", json=payload)
        assert response.status_code == 200
        assert response.json() == payload

    @pytest.mark.parametrize("field", ["name", "description", "cadence", "startDate", "endDate"])
    def test_it_raises_on_missing_fields(self, client: TestClient, field: str):
        payload = {
            "name": fake.word(),
            "description": fake.sentence(),
            "cadence": random.choice(["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]),
            "startDate": pendulum.now().date().isoformat(),
            "endDate": pendulum.now().date().isoformat(),
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
        }

        response = client.post("/chore/choreValidate", json=payload)
        assert response.status_code == 422
        assert response.json() == {
            "name": ["String should have at least 1 character"],
            "description": ["String should have at least 1 character"],
            "cadence": ["Input should be 'DAILY', 'WEEKLY', 'MONTHLY' or 'YEARLY'"],
            "startDate": ["String should have at least 1 character"],
            "endDate": ["String should have at least 1 character"],
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
