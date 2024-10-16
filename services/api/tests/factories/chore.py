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

    @staticmethod
    def task(
        chore_distribution: models.ChoreDistribution | None = None,
        due_date: pendulum.Date | None = None,
        completed_at: pendulum.DateTime | None = None,
    ):
        if not chore_distribution:
            chore_distribution = Chore.distribution()

        return models.Task(
            chore_distribution=chore_distribution,
            due_date=due_date or pendulum.now().date(),
            completed_at=completed_at or pendulum.now(),
        )
