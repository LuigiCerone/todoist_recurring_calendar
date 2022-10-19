import os

from dotenv import load_dotenv
from todoist_api_python.api_async import TodoistAPIAsync

load_dotenv()
api = TodoistAPIAsync(os.getenv("TOKEN"))


async def get_all_tasks():
    """Method used to retrieve all tasks by using Todoist offical API

    Returns:
        List[dict]: List of dictionaries containing all the tasks information
    """
    try:
        tasks = await api.get_tasks()
        return [task.to_dict() for task in tasks]
    except Exception as error:
        print(error)


async def get_all_projects():
    """Method used to retrieve all projects by using Todoist official API

    Returns:
        List[dict]: List of dictionaries containing all the projects information
    """
    try:
        return await api.get_projects()
    except Exception as error:
        print(error)


async def get_all_sections_for_project(project_id: int):
    """Method used to retrieve all sections by using Todoist official API

    Args:
        project_id (int): The project id used to find sections

    Returns:
        List[dict]: List of dictionaries containing all the sections information
    """
    try:
        return await api.get_sections(project_id=project_id)
    except Exception as error:
        print(error)


async def create_task(content: str, day: str, section_id: int):
    """Method used to create a new task by using Todoist official API

    Args:
        content (str): The new task's content
        day (str): The new task's recurring days
        section_id (int): The new task's section identifier

    Returns:
        dict: Dictionary containing all the new task information
    """
    try:
        task = await api.add_task(
            content=content,
            due_string=f"every {day}",
            section_id=section_id,
            due_lang="en",
        )
        return task
    except Exception as error:
        print(error)


async def create_multiple_tasks(new_task: dict):
    """Method used to create multiple tasks by using Todoist offical API

    Args:
        new_task (dict): Dictionary containing all the new task information required to create it
    """
    for day in new_task["days"]:
        await create_task(
            content=new_task["content"],
            day=day,
            section_id=new_task.get("section_id", None),
        )


async def delete_task(task_to_delete: int):
    """Method used to delete a task by using Todoist offical API

    Args:
        task_to_delete (int): The id of the task that needs to be deleted

    Returns:
        bool: Boolean flag with operation result
    """
    try:
        return await api.delete_task(task_id=task_to_delete)
    except Exception as error:
        print(error)
