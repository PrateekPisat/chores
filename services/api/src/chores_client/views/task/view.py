from chores.grpc_generated.chores_pb2 import (
    Cadence,
    CreateChoreResponse,
    CreateDistributionPayload,
    CreateDistributionResponse,
    DeleteChorePayload,
    DeleteChoreResponse,
    DeleteDistributionPayload,
    DeleteDistributionResponse,
    DeleteTaskPayload,
    DeleteTaskResponse,
    GetChorePayload,
    GetChoreResponse,
    GetDistributionPayload,
    GetDistributionResponse,
    GetTaskPayload,
    GetTaskResponse,
    ListChorePayload,
    ListChoreResponse,
    ListTaskPayload,
    ListTaskResponse,
    UpdateChorePayload,
    UpdateChoreResponse,
    UpdateDistributionPayload,
    UpdateDistributionResponse,
    UpdateTaskPayload,
    UpdateTaskResponse,
)

from chores_client.dependencies import TaskClientDep, TokenDep
from chores_client.views.task.schema import (
    Chore,
    ChoreDetails,
    ChoreDistribution,
    ChoreId,
    Task,
    TaskId,
    UpdateTask,
    UserIds,
)
from chores_client.views.user.schema import User

ENUM_MAP = enum_map = {
    Cadence.DAILY: "DAILY",
    Cadence.WEEKLY: "WEEKLY",
    Cadence.MONTHLY: "MONTHLY",
    Cadence.YEARLY: "YEARLY",
}


def create_chore(payload: ChoreDetails, task_client: TaskClientDep, token: TokenDep) -> ChoreId:
    response: CreateChoreResponse = task_client.CreateChore(
        payload.grpc_model_dump(), metadata=[("authorization", f"Bearer {token}")]
    )
    return ChoreId(id=response.id)


def check_chore_payload(payload: ChoreDetails) -> ChoreDetails:
    return ChoreDetails(**payload.model_dump())


def get_chore(chore_id: str, task_client: TaskClientDep, token: TokenDep) -> Chore:
    response: GetChoreResponse = task_client.GetChore(
        GetChorePayload(id=chore_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return Chore(
        id=response.id,
        name=response.name,
        description=response.description,
        cadence=ENUM_MAP[response.cadence],
        start_date=response.start_date,
        end_date=response.end_date,
    )


def list_chores(user_id: str, task_client: TaskClientDep, token: TokenDep):
    response: ListChoreResponse = task_client.ListChores(
        ListChorePayload(user_id=user_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return [
        Chore(
            id=chore.id,
            name=chore.name,
            description=chore.description,
            cadence=ENUM_MAP[chore.cadence],
            start_date=chore.start_date,
            end_date=chore.end_date,
            houseId=chore.house_id,
        )
        for chore in response.chores
    ]


def update_chore(
    chore_id: str, payload: ChoreDetails, task_client: TaskClientDep, token: TokenDep
) -> ChoreId:
    response: UpdateChoreResponse = task_client.UpdateChore(
        UpdateChorePayload(**payload.model_dump(), id=chore_id),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return ChoreId(id=response.id)


def delete_chore(chore_id: str, task_client: TaskClientDep, token: TokenDep) -> ChoreId:
    response: DeleteChoreResponse = task_client.DeleteChore(
        DeleteChorePayload(id=chore_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return ChoreId(id=response.id)


def create_distribute(
    chore_id: str, payload: UserIds, task_client: TaskClientDep, token: TokenDep
) -> ChoreId:
    response: CreateDistributionResponse = task_client.CreateDistribution(
        CreateDistributionPayload(chore_id=chore_id, user_ids=payload.user_ids),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return ChoreId(id=response.id)


def check_distribution_payload(payload: UserIds) -> UserIds:
    return UserIds(**payload.model_dump())


def get_distribution(
    chore_id: str, task_client: TaskClientDep, token: TokenDep
) -> ChoreDistribution:
    response: GetDistributionResponse = task_client.GetDistribution(
        GetDistributionPayload(id=chore_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return ChoreDistribution(
        chore=Chore(
            id=response.chore.id,
            name=response.chore.name,
            description=response.chore.description,
            cadence=ENUM_MAP[response.chore.cadence],
            start_date=response.chore.start_date,
            end_date=response.chore.end_date,
        ),
        users=[
            User(
                user_id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            for user in response.users
        ],
    )


def update_distribution(
    chore_id: str, payload: UserIds, task_client: TaskClientDep, token: TokenDep
) -> ChoreId:
    response: UpdateDistributionResponse = task_client.UpdateDistribution(
        UpdateDistributionPayload(user_ids=payload.user_ids, chore_id=chore_id),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return ChoreId(id=response.id)


def delete_distribution(chore_id: str, task_client: TaskClientDep, token: TokenDep) -> ChoreId:
    response: DeleteDistributionResponse = task_client.DeleteDistribution(
        DeleteDistributionPayload(id=chore_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return ChoreId(id=response.id)


def list_tasks(user_id: str, task_client: TaskClientDep, token: TokenDep):
    response: ListTaskResponse = task_client.ListTasks(
        ListTaskPayload(user_id=user_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return [
        Task(
            id=task.id,
            dueDate=task.due_date if task.due_date else None,
            completedAt=task.completed_at if task.completed_at else None,
            chore=Chore(
                id=task.chore.id,
                name=task.chore.name,
                description=task.chore.description,
                cadence=ENUM_MAP[task.chore.cadence],
                start_date=task.chore.start_date,
                end_date=task.chore.end_date,
                houseId=task.chore.house_id,
            ),
            user=User(
                user_id=task.user.id,
                email=task.user.email,
                first_name=task.user.first_name,
                last_name=task.user.last_name,
                sub=task.user.sub,
                picture=task.user.picture,
                nickname=task.user.nickname,
            ),
        )
        for task in response.tasks
    ]


def get_task(task_id: str, task_client: TaskClientDep, token: TokenDep) -> Task:
    response: GetTaskResponse = task_client.GetTask(
        GetTaskPayload(id=task_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return Task(
        id=response.id,
        dueDate=response.due_date if response.due_date else None,
        completedAt=response.completed_at if response.completed_at else None,
        chore=Chore(
            id=response.chore.id,
            name=response.chore.name,
            description=response.chore.description,
            cadence=ENUM_MAP[response.chore.cadence],
            start_date=response.chore.start_date,
            end_date=response.chore.end_date,
        ),
        user=User(
            user_id=response.user.id,
            email=response.user.email,
            first_name=response.user.first_name,
            last_name=response.user.last_name,
        ),
    )


def update_task(
    task_id: str, payload: UpdateTask, task_client: TaskClientDep, token: TokenDep
) -> TaskId:
    response: UpdateTaskResponse = task_client.UpdateTask(
        UpdateTaskPayload(id=task_id, due_date=payload.due_date, completed_at=payload.completed_at),
        metadata=[("authorization", f"Bearer {token}")],
    )

    return TaskId(id=response.id)


def delete_task(task_id: str, task_client: TaskClientDep, token: TokenDep) -> TaskId:
    response: DeleteTaskResponse = task_client.DeleteTask(
        DeleteTaskPayload(id=task_id), metadata=[("authorization", f"Bearer {token}")]
    )

    return TaskId(id=response.id)
