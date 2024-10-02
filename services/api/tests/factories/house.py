import uuid

from chores import models
from faker import Faker
from tests.factories.user import User

fake = Faker("az_AZ")


class House:
    @staticmethod
    def house(id: uuid.UUID | None = None, name: str | None = None) -> dict:
        return models.House(id=id or fake.uuid4(), name=name or fake.house_number())

    @staticmethod
    def house_member(house_id: uuid.UUID | None = None, user_id: uuid.UUID | None = None) -> dict:
        if not house_id:
            house = House.house()
            house_id = house.id

        if not user_id:
            user = User.user()
            user_id = user.id

        return models.HouseMember(house_id=house_id, user_id=user_id)
