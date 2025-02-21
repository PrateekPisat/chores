import pytest
from fastapi.testclient import TestClient


class Test_CheckHousePayload:
    @pytest.mark.parametrize("endpoint", ["updateValidate", "houseValidate"])
    def test_it_validates_payload(self, client: TestClient, endpoint: str):
        payload = {"name": "Test House"}

        response = client.post(f"/house/{endpoint}", json=payload)
        assert response.status_code == 200
        assert response.json() == {"name": payload["name"]}

    @pytest.mark.parametrize("endpoint", ["updateValidate", "houseValidate"])
    def test_it_raises_on_missing_fields(self, client: TestClient, endpoint: str):
        payload = {}

        response = client.post(f"/house/{endpoint}", json=payload)
        assert response.status_code == 422
        assert response.json() == {"name": ["Field required"]}

    @pytest.mark.parametrize("endpoint", ["updateValidate", "houseValidate"])
    def test_it_raises_on_empty_fields(self, client: TestClient, endpoint: str):
        payload = {"name": ""}

        response = client.post(f"/house/{endpoint}", json=payload)
        assert response.status_code == 422
        assert response.json() == {"name": ["String should have at least 1 character"]}
