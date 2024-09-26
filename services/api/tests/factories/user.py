import uuid

from chores import models
from faker import Faker

fake = Faker()


class User:
    @staticmethod
    def user(
        id: uuid.UUID | None = None,
        email: str | None = None,
        password: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> models.User:
        return models.User(
            id=id or fake.uuid4(),
            email=email or fake.email(),
            password=password or fake.md5(),
            first_name=first_name or fake.first_name(),
            last_name=last_name or fake.last_name(),
        )
