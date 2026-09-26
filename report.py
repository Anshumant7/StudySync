from planner import total_hours_needed

def build_report(task_list):
    total_tasks = len(task_list)

    done_tasks = []
    pending_tasks = []
    for task in task_list:
        if task["status"] == "done":
            done_tasks.append(task)
        else:
            pending_tasks.append(task)

    hours_by_subject = {}
    for task in pending_tasks:
        subject = task["subject"]
        if subject not in hours_by_subject:
            hours_by_subject[subject] = 0
        hours_by_subject[subject] += task["est_hours"]

    if total_tasks > 0:
        completion_rate = round(100 * len(done_tasks) / total_tasks, 1)
    else:
        completion_rate = 0.0

    return {
        "total": total_tasks,
        "done": len(done_tasks),
        "pending": len(pending_tasks),
        "completion_rate": completion_rate,
        "pending_hours": total_hours_needed(task_list),
        "hours_by_subject": hours_by_subject,
    }

def print_report(task_list):
    stats = build_report(task_list)
    print("=== My StudySync Report ===")
    print(f"Total tasks : {stats['total']}")
    print(f"Completed   : {stats['done']} ({stats['completion_rate']}%)")
    print(f"Pending     : {stats['pending']} ({stats['pending_hours']} hours left)")
    print("Hours needed per subject:")
    for subject in stats["hours_by_subject"]:
        print(f"  - {subject}: {stats['hours_by_subject'][subject]} hours")