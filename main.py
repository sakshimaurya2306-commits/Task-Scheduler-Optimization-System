from src.input_loader import load_tasks
from src.validator import validate_tasks
from src.scheduler import schedule_tasks
from src.metrics import calculate_metrics
from src.report_generator import generate_report


tasks = load_tasks("data/tasks.csv")
valid_tasks = validate_tasks(tasks)

completed_tasks, missed_tasks = schedule_tasks(valid_tasks)
metrics = calculate_metrics(completed_tasks, missed_tasks)

print("Optimized Schedule:")
for item in completed_tasks:
    task = item["task"]
    print(f"{task.name} | Start: {item['start_time']} | End: {item['end_time']}")

print("\nMissed Tasks:")
if len(missed_tasks) == 0:
    print("No missed tasks")
else:
    for task in missed_tasks:
        print(task.name)

print("\nPerformance Report:")
print(f"Total Tasks: {metrics['total_tasks']}")
print(f"Completed Tasks: {metrics['completed_tasks']}")
print(f"Missed Tasks: {metrics['missed_tasks']}")
print(f"Total Profit: {metrics['total_profit']}")
print(f"Total Execution Time: {metrics['total_execution_time']}")
print(f"Success Percentage: {metrics['success_percentage']:.2f}%")

generate_report(
    completed_tasks,
    missed_tasks,
    metrics,
    "outputs/schedule_report.txt"
)

print("\nReport saved to outputs/schedule_report.txt")