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
