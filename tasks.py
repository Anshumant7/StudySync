import storage

def load_my_tasks(username):
    every_task = storage.load_json(storage.TASKS_FILE)
    my_tasks = []
    for task in every_task:
        if task["owner"] == username:
            my_tasks.append(task)
    return my_tasks

def next_task_id(every_task):
    biggest_id_so_far = 0
    for task in every_task:
        if task["id"] > biggest_id_so_far:
            biggest_id_so_far = task["id"]
    return biggest_id_so_far + 1

def add_task(username, title, subject, priority, due_date, est_hours):
    every_task = storage.load_json(storage.TASKS_FILE)

    new_task = {
        "id": next_task_id(every_task),
        "owner": username,
        "title": title,
        "subject": subject,
        "priority": priority.lower(),
        "due_date": due_date,
        "est_hours": float(est_hours),
        "status": "pending",
    }

    every_task.append(new_task)
    storage.save_json(storage.TASKS_FILE, every_task)
    return new_task

def find_task_by_id(task_list, task_id):
    for task in task_list:
        if task["id"] == task_id:
            return task
    return None

def edit_task(username, task_id, field, new_value):
    every_task = storage.load_json(storage.TASKS_FILE)
    task = find_task_by_id(every_task, task_id)

    if task is None or task["owner"] != username:
        return False

    if field == "est_hours":
        new_value = float(new_value)

    task[field] = new_value
    storage.save_json(storage.TASKS_FILE, every_task)
    return True

def mark_as_done(username, task_id):
    return edit_task(username, task_id, "status", "done")

def delete_task(username, task_id):
    every_task = storage.load_json(storage.TASKS_FILE)
    task = find_task_by_id(every_task, task_id)

    if task is None or task["owner"] != username:
        return False

    every_task.remove(task)
    storage.save_json(storage.TASKS_FILE, every_task)
    return True