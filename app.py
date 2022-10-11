from todoist_api_python.api_async import TodoistAPIAsync
from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


import asyncio
import os
import pandas as pd


async def get_tasks_async():
    try:
        tasks = await api.get_tasks()
        return [task.to_dict() for task in tasks]
    except Exception as error:
        print(error)


async def create_task(content: str):
    try:
        task = await api.add_task(
            content=content,
        )
        return task
    except Exception as error:
        print(error)


async def delete_task(task_to_delete: int):
    try:
        is_success = await api.delete_task(task_id=task_to_delete)
        print(is_success)
    except Exception as error:
        print(error)


async def main():

    action = inquirer.select(
        message='How do you want to edit your todoist?',
        choices=[
            Choice('create', 'Create new recurrent task'), 
            Choice('delete', 'Delete a bunch of recurrent stuff')
            ]
    ).execute()

    if action == 'create':
        pass
    elif action == 'delete':
        pass
    else:
        raise Exception('Unknown option specified!')


async def get_all_tasks():
    tasks_dict = await get_tasks_async()
    df = pd.DataFrame.from_dict(tasks_dict)
    print(df.head())


if __name__ == '__main__':
    load_dotenv()
    api = TodoistAPIAsync(os.getenv('TOKEN'))

    asyncio.run(main())
