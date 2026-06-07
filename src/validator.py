def validate_tasks(tasks):
    valid_tasks = []

    for task in tasks:
        if task.name.strip() == "":
            print(f"Invalid task skipped: Task ID {task.task_id} has empty name")
            continue

        if task.priority <= 0:
            print(f"Invalid task skipped: {task.name} has invalid priority")
            continue

        if task.deadline <= 0:
            print(f"Invalid task skipped: {task.name} has invalid deadline")
            continue

        if task.execution_time <= 0:
            print(f"Invalid task skipped: {task.name} has invalid execution time")
            continue

        if task.profit <= 0:
            print(f"Invalid task skipped: {task.name} has invalid profit")
            continue

        valid_tasks.append(task)

    return valid_tasks