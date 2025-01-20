from sqlalchemy_model_factory.declarative import declarative
from tests.factories.chore import Chore
from tests.factories.house import House
from tests.factories.user import User


@declarative()
class ModelFactory:
    user = User
    house = House
    chore = Chore
