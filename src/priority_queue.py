import heapq


class TaskPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, task):
        heapq.heappush(
            self.heap,
            (
                task.deadline,
                -task.priority,
                -task.profit,
                task.task_id,
                task
            )
        )

    def pop(self):
        if self.is_empty():
            return None

        return heapq.heappop(self.heap)[4]

    def is_empty(self):
        return len(self.heap) == 0

    def display_queue(self):
        return [item[4] for item in self.heap]