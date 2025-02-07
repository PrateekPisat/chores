from chores_client import views

user_routes = [
    {
        "path": "/user/{user_id}",
        "method": "GET",
        "endpoint": views.user.get_user,
        "tags": ["User"],
    },
    {
        "path": "/user/{user_id}",
        "method": "PUT",
        "endpoint": views.user.update_user,
        "tags": ["User"],
    },
    {
        "path": "/user/{user_id}",
        "method": "DELETE",
        "endpoint": views.user.delete_user,
        "tags": ["User"],
    },
    {
        "path": "/user/search",
        "method": "POST",
        "endpoint": views.user.search_user,
        "tags": ["User"],
    },
    {
        "path": "/user/sync",
        "method": "POST",
        "endpoint": views.user.sync_user,
        "tags": ["User"],
    },
]

house_routes = [
    {
        "path": "/house",
        "method": "POST",
        "endpoint": views.house.create_house,
        "tags": ["House"],
    },
    {
        "path": "/houseValidate",
        "method": "POST",
        "endpoint": views.house.check_house_payload,
        "tags": ["House"],
    },
    {
        "path": "/house/{house_id}",
        "method": "GET",
        "endpoint": views.house.get_house,
        "tags": ["House"],
    },
    {
        "path": "/house/updateValidate",
        "method": "POST",
        "endpoint": views.house.check_update_payload,
        "tags": ["User"],
    },
    {
        "path": "/house/{house_id}",
        "method": "PUT",
        "endpoint": views.house.update_house,
        "tags": ["House"],
    },
    {
        "path": "/house/{house_id}",
        "method": "DELETE",
        "endpoint": views.house.delete_house,
        "tags": ["House"],
    },
    {
        "path": "/house/member",
        "method": "POST",
        "endpoint": views.house.add_member,
        "tags": ["House"],
    },
    {
        "path": "/house/{house_id}/member/{user_id}",
        "method": "DELETE",
        "endpoint": views.house.remove_member,
        "tags": ["House"],
    },
    {
        "path": "/house/{house_id}/member",
        "method": "get",
        "endpoint": views.house.get_members,
        "tags": ["House"],
    },
]

task_routes = [
    {
        "path": "/chore",
        "method": "POST",
        "endpoint": views.task.create_chore,
        "tags": ["Chore"],
    },
    {
        "path": "/choreValidate",
        "method": "POST",
        "endpoint": views.task.check_chore_payload,
        "tags": ["Chore"],
    },
    {
        "path": "/chore/{chore_id}",
        "method": "GET",
        "endpoint": views.task.get_chore,
        "tags": ["Chore"],
    },
    {
        "path": "/chore/{chore_id}",
        "method": "PUT",
        "endpoint": views.task.update_chore,
        "tags": ["Chore"],
    },
    {
        "path": "/chore/{chore_id}",
        "method": "DELETE",
        "endpoint": views.task.delete_chore,
        "tags": ["Chore"],
    },
    {
        "path": "/chore/{chore_id}/distribution",
        "method": "POST",
        "endpoint": views.task.create_distribute,
        "tags": ["Chore", "Distribution"],
    },
    {
        "path": "/chore/distributionValidate",
        "method": "POST",
        "endpoint": views.task.check_distribution_payload,
        "tags": ["Chore", "Distribution"],
    },
    {
        "path": "/chore/{chore_id}/distribution",
        "method": "GET",
        "endpoint": views.task.get_distribution,
        "tags": ["Chore", "Distribution"],
    },
    {
        "path": "/chore/{chore_id}/distribution",
        "method": "PUT",
        "endpoint": views.task.update_distribution,
        "tags": ["Chore", "Distribution"],
    },
    {
        "path": "/chore/{chore_id}/distribution",
        "method": "DELETE",
        "endpoint": views.task.delete_distribution,
        "tags": ["Chore", "Distribution"],
    },
    {
        "path": "/task/{task_id}",
        "method": "GET",
        "endpoint": views.task.get_task,
        "tags": ["Chore", "Task"],
    },
    {
        "path": "/task/{task_id}",
        "method": "PUT",
        "endpoint": views.task.update_task,
        "tags": ["Chore", "Task"],
    },
    {
        "path": "/task/{task_id}",
        "method": "DELETE",
        "endpoint": views.task.delete_task,
        "tags": ["Chore", "Task"],
    },
]

all_routes = user_routes + house_routes + task_routes
