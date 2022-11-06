import asyncio
from typing import List

import pandas as pd

from utils.cli_interface import (
    get_delete_tasks_info,
    get_new_task_info,
    get_user_action,
)
from utils.todosit_api import create_multiple_tasks, delete_task, get_all_tasks


async def create_new_tasks():
    """Method used to manage the creation of a new recurring task"""
    new_task = await get_new_task_info()
    await create_multiple_tasks(new_task=new_task)
    print("Tasks successfully created!")


async def get_recurring_tasks_df() -> pd.DataFrame:
    """Method used to retrieve all tasks information. Then, a dataframe is created with this information.
    Finally, the method looks for task ids associated to recurring istances of the same principal task

    Returns:
        pd.DataFrame: Dataframe with recurring tasks information along with a unique row identifier
    """
    tasks = await get_all_tasks()
    df = pd.DataFrame(tasks)
    return df.groupby(["content"])["id"].apply(list).reset_index(name="ids")


async def delete_recurring_tasks(df: pd.DataFrame, indexes_to_delete: List[int]):
    """Method used to coordinate the deletion of all the task instances associated to a principal task

    Args:
        df (pd.DataFrame): Dataframe with all tasks information and aggregated ids
        indexes_to_delete (List[int]): List of Dataframe indexes to delete

    Returns:
        List[bool]: list of boolean flags
    """
    for i_to_delete in indexes_to_delete:
        [await delete_task(id) for id in df.iloc[i_to_delete]["ids"]]


async def delete_multiple_tasks():
    """Method used to coordinate the deletion of a recurring task"""
    df = await get_recurring_tasks_df()

    indexes_to_delete = await get_delete_tasks_info(df)
    if indexes_to_delete:
        await delete_recurring_tasks(df, indexes_to_delete)
        print("Tasks successfully deleted!")


async def main():
    action = await get_user_action()

    if action == "create":
        await create_new_tasks()
    elif action == "delete":
        await delete_multiple_tasks()
    else:
        raise Exception("Unknown option specified!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
