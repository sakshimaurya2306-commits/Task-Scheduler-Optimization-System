from src.priority_queue import TaskPriorityQueue


def schedule_tasks(tasks):
    task_queue = TaskPriorityQueue()

    for task in tasks:
        task_queue.push(task)

    current_time = 0
    completed_tasks = []
    missed_tasks = []

    while not task_queue.is_empty():
        task = task_queue.pop()

        start_time = current_time
        end_time = current_time + task.execution_time

        if end_time <= task.deadline:
            completed_tasks.append({
                "task": task,
                "start_time": start_time,
                "end_time": end_time
            })
            current_time = end_time
        else:
            missed_tasks.append(task)

    return completed_tasks, missed_tasks