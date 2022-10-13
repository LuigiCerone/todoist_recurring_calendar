from hashlib import new
from todoist_api_python.api_async import TodoistAPIAsync
from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

import asyncio
import os
import pandas as pd


async def get_all_tasks():
    try:
        tasks = await api.get_tasks()
        return [task.to_dict() for task in tasks]
    except Exception as error:
        print(error)


async def get_all_projects():
    try:
        return await api.get_projects()
    except Exception as error:
        print(error)
    

async def get_all_sections_for_project(project_id: int):
    try:
        return await api.get_sections(project_id=project_id)
    except Exception as error:
        print(error)


async def create_task(content: str, day: str, section_id: int):
    try:
        task = await api.add_task(
            content=content,
            due_string=f'every {day}',
            section_id=section_id,
            due_lang='en'
        )
        return task
    except Exception as error:
        print(error)


async def create_multiple_tasks(new_task: dict):
    for day in new_task['days']:
        t = await create_task(content=new_task['content'], day=day, section_id=new_task['section_id'])


async def delete_task(task_to_delete: int):
    try:
        return await api.delete_task(task_id=task_to_delete)
    except Exception as error:
        print(error)


async def main():
    action = await inquirer.select(
        message='How do you want to edit your todoist?',
        choices=[
            Choice('create', 'Create new recurrent task'),
            Choice('delete', 'Delete a bunch of recurrent stuff')
        ]
    ).execute_async()

    if action == 'create':
        new_task = dict()
        new_task['content'] = await inquirer.text(message="What is the new task you want to work on?").execute_async()
        new_task['days'] = await inquirer.checkbox(
            message="Pick your recurrent days:",
            cycle=True,
            choices=[
                'Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday'
            ],
            validate=lambda result: len(result) >= 1,
            invalid_message="should be at least 1 selection",
            instruction="(select at least 1)"
        ).execute_async()

        new_task['project_id'] = await inquirer.select(
            message='Select the project to which you want to assign these tasks:',
            default=None,
            choices=[Choice(p.id, p.name) for p in await get_all_projects() ]
        ).execute_async()

        new_task['section_id'] = await inquirer.select(
            message='Select the section in project to which you want to assign these tasks:',
            default=None,
            choices=[Choice(s.id, s.name) for s in await get_all_sections_for_project(new_task['project_id']) ]
        ).execute_async()

        await create_multiple_tasks(new_task=new_task)

    elif action == 'delete':
        tasks = await get_all_tasks()
        df = pd.DataFrame(tasks)
        grouped_df = df.groupby(['content'])['id'].apply(list).reset_index(name='ids')

        index_to_delete = await inquirer.checkbox(
            message="Select recurrent tasks to delete:",
            cycle=True,
            choices=[ Choice(index, row['content']) for index, row in grouped_df.iterrows() ],
            validate=lambda result: len(result) >= 1,
            invalid_message="should be at least 1 selection",
            instruction="(select at least 1)"
        ).execute_async()

        print(index_to_delete)
        proceed = await inquirer.confirm(message="Are you sure you want to delete these tasks?", default=False).execute_async()
        if proceed:
            for i_to_delete in index_to_delete:
                result = [await delete_task(id) for id in grouped_df.iloc[i_to_delete]['ids']]
                if all(result):
                    print("Tasks successfully deleted!")

    else:
        raise Exception('Unknown option specified!')


if __name__ == '__main__':
    load_dotenv()
    api = TodoistAPIAsync(os.getenv('TOKEN'))

    asyncio.get_event_loop().run_until_complete(main())
