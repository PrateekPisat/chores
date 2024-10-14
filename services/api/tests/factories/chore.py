import random

import pendulum
from chores import models
from chores.grpc_generated.chores_pb2 import Cadence
from faker import Faker
from tests.factories.user import User

fake = Faker()


class Chore:
    @staticmethod
    def chore(
        name: str | None = None,
        description: str | None = None,
        cadence: str | None = None,
        start_date: pendulum.Date | None = None,
        end_date: pendulum.Date | None = None,
    ):
        return models.Chore(
            name=name or fake.catch_phrase(),
            description=description or fake.sentence(),
            cadence=cadence or random.choice(Cadence.keys()),
            start_date=start_date or pendulum.now().date(),
            end_date=end_date or pendulum.now().date(),
        )

    @staticmethod
    def distribution(
        chore: models.Chore | None = None,
        user: models.User | None = None,
    ):
        if not chore:
            chore = Chore.chore()

        if not user:
            user = User.user()

        return models.ChoreDistribution(chore=chore, user=user)
