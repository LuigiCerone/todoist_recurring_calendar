from typing import List

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pandas import DataFrame

from utils.todosit_api import get_all_projects, get_all_sections_for_project


async def get_user_action() -> str:
    """Method used to request to the user an action

    Returns:
        str: Requested user action
    """
    return await inquirer.select(
        message="How do you want to edit your todoist?",
        choices=[
            Choice("create", "Create new recurring task"),
            Choice("delete", "Delete a bunch of recurring stuff"),
        ],
    ).execute_async()


async def get_new_task_info() -> dict:
    """Method used to collect all the new task information from the user

    Returns:
        dict: Dictionary containing all the new task information required to create it
    """
    new_task = dict()
    new_task["content"] = await inquirer.text(
        message="What is the new task you want to work on?"
    ).execute_async()
    new_task["days"] = await inquirer.checkbox(
        message="Pick your recurring days:",
        cycle=True,
        choices=[
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ],
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute_async()

    new_task["project_id"] = await inquirer.select(
        message="Select the project to which you want to assign these tasks:",
        default=None,
        choices=[Choice(p.id, p.name) for p in await get_all_projects()],
    ).execute_async()

    sections = await get_all_sections_for_project(new_task["project_id"])
    if sections:
        new_task["section_id"] = await inquirer.select(
            message="Select the section in project to which you want to assign these tasks:",
            default=None,
            choices=[Choice(s.id, s.name) for s in sections],
        ).execute_async()

    return new_task


async def get_delete_tasks_info(df: DataFrame) -> List[int]:
    """Method used to collect all the information about the task we want to delete

    Args:
        df (DataFrame): Dataframe with recurring tasks information along with a unique row identifier

    Returns:
        List[int]: List of all the Dataframe indexes that needs to be deleted. One index may contain multple task ids
    """
    indexes_to_delete = await inquirer.checkbox(
        message="Select recurring tasks to delete:",
        cycle=True,
        choices=[Choice(index, row["content"]) for index, row in df.iterrows()],
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute_async()

    proceed = await inquirer.confirm(
        message="Are you sure you want to delete these tasks?", default=False
    ).execute_async()
    return indexes_to_delete if proceed else None
