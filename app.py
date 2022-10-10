from todoist_api_python.api_async import TodoistAPIAsync
from dotenv import load_dotenv

import asyncio
import os
import pandas as pd


async def get_tasks_async():
    try:
        tasks = await api.get_tasks()
        return [task.to_dict() for task in tasks]
    except Exception as error:
        print(error)


async def main():
    tasks_dict = await get_tasks_async()
    df = pd.DataFrame.from_dict(tasks_dict)
    print(df.head())


if __name__ == '__main__':
    load_dotenv()
    api = TodoistAPIAsync(os.getenv('TOKEN'))

    asyncio.run(main())
