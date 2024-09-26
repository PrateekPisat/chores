from sqlalchemy_model_factory.declarative import declarative
from tests.factories.user import User


@declarative()
class ModelFactory:
    user = User
