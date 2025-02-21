import pytest
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


class Test_CheckUpdatePayload:
    def test_it_validates_update_user_payload(self, client: TestClient):
        payload = {
            "email": fake.email(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "picture": fake.url(),
            "nickname": fake.user_name(),
            "sub": fake.uuid4(),
        }

        response = client.post("/user/updateValidate", json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "email": payload["email"],
            "firstName": payload["firstName"],
            "lastName": payload["lastName"],
            "picture": payload["picture"],
            "nickname": payload["nickname"],
            "sub": payload["sub"],
        }

    @pytest.mark.parametrize("field", ["email", "firstName", "lastName", "sub"])
    def test_it_raises_on_missing_fields(self, client: TestClient, field: str):
        payload = {
            "email": fake.email(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "picture": fake.url(),
            "nickname": fake.user_name(),
            "sub": fake.uuid4(),
        }
        payload.pop(field)

        response = client.post("/user/updateValidate", json=payload)
        assert response.status_code == 422
        assert response.json()[field] == ["Field required"]

    def test_it_raises_on_empty_fields(self, client: TestClient):
        payload = {
            "email": "",
            "firstName": "",
            "lastName": "",
            "picture": "",
            "nickname": "",
            "sub": "",
        }

        response = client.post("/user/updateValidate", json=payload)
        assert response.status_code == 422
        assert response.json() == {
            "email": ["String should have at least 1 character"],
            "firstName": ["String should have at least 1 character"],
            "lastName": ["String should have at least 1 character"],
            "sub": ["String should have at least 1 character"],
        }
