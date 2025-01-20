from chores.grpc_generated.chores_pb2_grpc import UsersStub
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


class TestRegisterUser:
    def test_it_registers_a_user(self, client: TestClient, user_service: UsersStub):
        response = client.post(
            "/user",
            json={
                "email": fake.email(),
                "password": "password",
                "confirm_password": "password",
                "first_name": "first_name",
                "last_name": "last_name",
            },
        )
        assert response.status_code == 200
        assert "user_id" in response.json()
        assert "token" in response.json()
