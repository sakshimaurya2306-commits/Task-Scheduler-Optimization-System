def calculate_metrics(completed_tasks, missed_tasks):
    total_completed = len(completed_tasks)
    total_missed = len(missed_tasks)
    total_tasks = total_completed + total_missed

    total_profit = 0
    total_execution_time = 0

    for item in completed_tasks:
        task = item["task"]
        total_profit += task.profit
        total_execution_time += task.execution_time

    if total_tasks == 0:
        success_percentage = 0
    else:
        success_percentage = (total_completed / total_tasks) * 100

    return {
        "total_tasks": total_tasks,
        "completed_tasks": total_completed,
        "missed_tasks": total_missed,
        "total_profit": total_profit,
        "total_execution_time": total_execution_time,
        "success_percentage": success_percentage
    }