class Task:
    def __init__(self, task_id, name, priority, deadline, execution_time, profit):
        self.task_id = int(task_id)
        self.name = name
        self.priority = int(priority)
        self.deadline = int(deadline)
        self.execution_time = int(execution_time)
        self.profit = int(profit)

    def __repr__(self):
        return (
            f"Task(id={self.task_id}, name='{self.name}', "
            f"priority={self.priority}, deadline={self.deadline}, "
            f"execution_time={self.execution_time}, profit={self.profit})"
        )