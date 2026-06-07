import csv
from src.task import Task


def load_tasks(file_path):
    tasks = []

    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            task = Task(
                row["task_id"],
                row["name"],
                row["priority"],
                row["deadline"],
                row["execution_time"],
                row["profit"]
            )
            tasks.append(task)

    return tasks