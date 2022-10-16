from typing import List

import asyncio
import pandas as pd

from utils.cli_interface import get_delete_tasks_info, get_new_task_info, get_user_action
from utils.todosit_api import create_multiple_tasks, delete_task, get_all_tasks


async def create_new_tasks():
    new_task = await get_new_task_info()
    await create_multiple_tasks(new_task=new_task)


async def get_recurrent_tasks_df() -> pd.DataFrame:
    tasks = await get_all_tasks()
    df = pd.DataFrame(tasks)
    return df.groupby(['content'])['id'].apply(list).reset_index(name='ids')


async def delete_recurrent_tasks(df: pd.DataFrame, indexes_to_delete: List[int]):
    for i_to_delete in indexes_to_delete:
        return [].extends([await delete_task(id) for id in df.iloc[i_to_delete]['ids']])
        

async def delete_multiple_tasks():
    df = await get_recurrent_tasks_df()

    indexes_to_delete = await get_delete_tasks_info(df)
    if indexes_to_delete:
        result = await delete_multiple_tasks(df, indexes_to_delete)
        if all(result):
            print("Tasks successfully deleted!")


async def main():
    action = await get_user_action()

    if action == 'create':
        await create_new_tasks()
    elif action == 'delete':
        await delete_multiple_tasks()
    else:
        raise Exception('Unknown option specified!')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
