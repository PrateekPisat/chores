from contextvars import ContextVar

from sqlalchemy.orm import Session

from chores.errors import NotFound, PermissionDenied, Unauthenticated
from chores.models.chore import Chore
from chores.models.house import House, HouseMember
from chores.models.user import User

current_user_sub: ContextVar[str | None] = ContextVar("current_user_sub", default=None)
current_user_email: ContextVar[str | None] = ContextVar("current_user_email", default=None)
current_caller: ContextVar[User | None] = ContextVar("current_caller", default=None)


def escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")


def require_caller(db: Session) -> User:
    """Return the authenticated user bound to ``db``.

    The auth interceptor loads the row once and stores it on ``current_caller``.
    This attaches that instance to the handler session. A direct lookup remains
    for callers that only set the token subject, such as the test interceptor.
    """
    cached = current_caller.get()
    if cached is not None:
        return db.merge(cached, load=False)

    sub = current_user_sub.get()
    if not sub:
        raise Unauthenticated("Missing token subject")

    user = db.query(User).filter(User.sub == sub).one_or_none()
    if user is None:
        raise Unauthenticated("User is not registered")
    return user


def require_self(caller: User, user_id: str, message: str = "Cannot access another user") -> None:
    if str(caller.id) != user_id:
        raise PermissionDenied(message)


def require_house_member(db: Session, caller: User, house_id: str) -> House:
    house = db.query(House).filter(House.id == house_id).one_or_none()
    if house is None:
        raise NotFound("House not found!")

    membership = (
        db.query(HouseMember).filter(HouseMember.house_id == house.id, HouseMember.user_id == caller.id).one_or_none()
    )
    if membership is None:
        raise PermissionDenied("Not a member of this house")
    return house


def require_chore_member(db: Session, caller: User, chore_id: str) -> Chore:
    chore = db.query(Chore).filter(Chore.id == chore_id).one_or_none()
    if chore is None:
        raise NotFound(f"Chore {chore_id} not found!")

    require_house_member(db, caller, str(chore.house_id))
    return chore
