import uuid

from chores import models
from faker import Faker

fake = Faker()


class User:
    @staticmethod
    def user(
        id: uuid.UUID | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        sub: str | None = None,
        picture: str | None = None,
        nickname: str | None = None,
    ) -> models.User:
        return models.User(
            id=id or fake.uuid4(),
            email=email or fake.email(),
            first_name=first_name or fake.first_name(),
            last_name=last_name or fake.last_name(),
            sub=sub or fake.md5(),
            picture=picture or fake.image_url(),
            nickname=nickname or fake.user_name(),
        )
