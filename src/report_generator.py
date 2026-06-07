def generate_report(completed_tasks, missed_tasks, metrics, file_path):
    with open(file_path, "w") as file:
        file.write("TASK SCHEDULER OPTIMIZATION REPORT\n")
        file.write("=" * 40)
        file.write("\n\n")

        file.write("OPTIMIZED SCHEDULE\n")
        file.write("-" * 40)
        file.write("\n")

        for item in completed_tasks:
            task = item["task"]
            file.write(
                f"{task.name} | Start: {item['start_time']} | "
                f"End: {item['end_time']} | Profit: {task.profit}\n"
            )

        file.write("\nMISSED TASKS\n")
        file.write("-" * 40)
        file.write("\n")

        if len(missed_tasks) == 0:
            file.write("No missed tasks\n")
        else:
            for task in missed_tasks:
                file.write(f"{task.name} | Deadline: {task.deadline}\n")

        file.write("\nPERFORMANCE REPORT\n")
        file.write("-" * 40)
        file.write("\n")

        file.write(f"Total Tasks: {metrics['total_tasks']}\n")
        file.write(f"Completed Tasks: {metrics['completed_tasks']}\n")
        file.write(f"Missed Tasks: {metrics['missed_tasks']}\n")
        file.write(f"Total Profit: {metrics['total_profit']}\n")
        file.write(f"Total Execution Time: {metrics['total_execution_time']}\n")
        file.write(f"Success Percentage: {metrics['success_percentage']:.2f}%\n")