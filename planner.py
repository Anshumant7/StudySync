from datetime import datetime, timedelta
from helpers import PRIORITY_WEIGHT, days_between

def urgency_score(task, today_text):
    days_left = days_between(today_text, task["due_date"])
    score = days_left - (2 * PRIORITY_WEIGHT[task["priority"]])
    if days_left < 0:
        score -= 1000
    return score

def sort_tasks_by_urgency(task_list, today_text):
    pending_tasks = []
    for task in task_list:
        if task["status"] == "pending":
            pending_tasks.append(task)

    pending_tasks.sort(key=lambda task: urgency_score(task, today_text))
    return pending_tasks

def total_hours_needed(task_list):
    total = 0
    for task in task_list:
        if task["status"] == "pending":
            total += task["est_hours"]
    return total

def make_weekly_plan(task_list, hours_per_day, today_text, number_of_days=7):
    ordered_tasks = sort_tasks_by_urgency(task_list, today_text)

    hours_left = {}
    for task in ordered_tasks:
        hours_left[task["id"]] = task["est_hours"]

    start_day = datetime.strptime(today_text, "%Y-%m-%d")
    plan = []

    for day_number in range(number_of_days):
        current_day = start_day + timedelta(days=day_number)
        free_hours_today = hours_per_day

        for task in ordered_tasks:
            if free_hours_today <= 0:
                break
            hours_remaining = hours_left[task["id"]]
            if hours_remaining <= 0:
                continue
            hours_to_spend = min(free_hours_today, hours_remaining)
            plan.append((current_day.strftime("%Y-%m-%d"), task["title"], hours_to_spend))
            hours_left[task["id"]] -= hours_to_spend
            free_hours_today -= hours_to_spend

    return plan