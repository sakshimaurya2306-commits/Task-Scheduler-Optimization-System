from ortools.sat.python import cp_model


def solve_schedule(tasks, resources, horizon=48, objective="hybrid"):
    model = cp_model.CpModel()

    task_by_id = {task["id"]: task for task in tasks}
    resource_by_id = {resource["id"]: resource for resource in resources}

    start_vars = {}
    end_vars = {}
    assigned_vars = {}
    optional_intervals = {}
    lateness_vars = {}
    cost_terms = []

    for task in tasks:
        task_id = task["id"]
        duration = int(task["duration"])

        start_vars[task_id] = model.NewIntVar(0, horizon, f"start_{task_id}")
        end_vars[task_id] = model.NewIntVar(0, horizon, f"end_{task_id}")
        model.Add(end_vars[task_id] == start_vars[task_id] + duration)

        lateness = model.NewIntVar(0, horizon, f"lateness_{task_id}")
        model.Add(lateness >= end_vars[task_id] - int(task["deadline"]))
        model.Add(lateness >= 0)
        lateness_vars[task_id] = lateness

        compatible_resources = []

        for resource in resources:
            resource_id = resource["id"]

            if task["skill"] not in resource["skills"]:
                continue

            assigned = model.NewBoolVar(f"assign_{task_id}_{resource_id}")
            assigned_vars[(task_id, resource_id)] = assigned
            compatible_resources.append(assigned)

            interval = model.NewOptionalIntervalVar(
                start_vars[task_id],
                duration,
                end_vars[task_id],
                assigned,
                f"interval_{task_id}_{resource_id}"
            )

            optional_intervals[(task_id, resource_id)] = interval

            cost_terms.append(assigned * duration * int(resource["cost"]))

            # Working-hour rule:
            # task must start and end inside one valid shift window.
            valid_windows = []

            for day_start in range(0, horizon + 1, 24):
                shift_start = day_start + int(resource["start"])
                shift_end = day_start + int(resource["end"])

                if shift_start + duration <= horizon:
                    in_window = model.NewBoolVar(
                        f"window_{task_id}_{resource_id}_{day_start}"
                    )

                    model.Add(start_vars[task_id] >= shift_start).OnlyEnforceIf(in_window)
                    model.Add(end_vars[task_id] <= shift_end).OnlyEnforceIf(in_window)

                    valid_windows.append(in_window)

            if valid_windows:
                model.Add(sum(valid_windows) >= assigned).OnlyEnforceIf(assigned)

        if compatible_resources:
            model.Add(sum(compatible_resources) == 1)
        else:
            # If no compatible resource exists, this task cannot be scheduled.
            model.Add(start_vars[task_id] == 0)
            model.Add(end_vars[task_id] == 0)

    # Dependency constraints
    for task in tasks:
        task_id = task["id"]
        dependency = task.get("dependency", "")

        if dependency and dependency in task_by_id:
            model.Add(start_vars[task_id] >= end_vars[dependency])

    # No overlap for each resource
    for resource in resources:
        resource_id = resource["id"]
        intervals = [
            optional_intervals[(task["id"], resource_id)]
            for task in tasks
            if (task["id"], resource_id) in optional_intervals
        ]

        if intervals:
            model.AddNoOverlap(intervals)

    # Capacity constraints
    for resource in resources:
        resource_id = resource["id"]
        capacity_terms = []

        for task in tasks:
            task_id = task["id"]

            if (task_id, resource_id) in assigned_vars:
                capacity_terms.append(
                    assigned_vars[(task_id, resource_id)] * int(task["duration"])
                )

        if capacity_terms:
            model.Add(sum(capacity_terms) <= int(resource["capacity"]))

    # Objective
    weighted_lateness = []
    for task in tasks:
        task_id = task["id"]
        weighted_lateness.append(lateness_vars[task_id] * int(task["priority"]))

    if objective == "lateness":
        model.Minimize(sum(weighted_lateness) * 100 + sum(cost_terms))
    elif objective == "cost":
        model.Minimize(sum(cost_terms) + sum(weighted_lateness) * 20)
    else:
        model.Minimize(sum(weighted_lateness) * 70 + sum(cost_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 8
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {
            "status": "NO_SOLUTION",
            "plan": []
        }

    plan = []

    for task in tasks:
        task_id = task["id"]

        for resource in resources:
            resource_id = resource["id"]

            if (task_id, resource_id) in assigned_vars:
                if solver.Value(assigned_vars[(task_id, resource_id)]) == 1:
                    plan.append({
                        "id": task_id,
                        "name": task["name"],
                        "duration": int(task["duration"]),
                        "deadline": int(task["deadline"]),
                        "priority": int(task["priority"]),
                        "skill": task["skill"],
                        "dependency": task.get("dependency", ""),
                        "resourceId": resource_id,
                        "resourceName": resource["name"],
                        "start": solver.Value(start_vars[task_id]),
                        "end": solver.Value(end_vars[task_id]),
                        "cost": int(resource["cost"])
                    })

    return {
        "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
        "plan": plan
    }