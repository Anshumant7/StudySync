import os
import storage
import users
import tasks
import planner
import report
from helpers import is_valid_date, is_valid_priority, is_valid_hours, days_between

storage.USERS_FILE = "data/test_users.json"
storage.TASKS_FILE = "data/test_tasks.json"

if os.path.exists(storage.USERS_FILE):
    os.remove(storage.USERS_FILE)
if os.path.exists(storage.TASKS_FILE):
    os.remove(storage.TASKS_FILE)

assert is_valid_date("2026-12-25") == True
assert is_valid_date("25-12-2026") == False
assert is_valid_priority("HIGH") == True
assert is_valid_priority("urgent") == False
assert is_valid_hours("2.5") == True
assert is_valid_hours("-1") == False
assert days_between("2026-09-24", "2026-09-27") == 3

assert users.sign_up("alice", "mypassword") == True
assert users.sign_up("alice", "mypassword") == False
assert users.log_in("alice", "mypassword") == True
assert users.log_in("alice", "wrongpass") == False

task = tasks.add_task("alice", "Read Chapter 1", "Physics", "high", "2026-12-01", 2)
assert task["title"] == "Read Chapter 1"
assert len(tasks.load_my_tasks("alice")) == 1

tasks.edit_task("alice", task["id"], "title", "Read Chapter 1 & 2")
updated_task = tasks.load_my_tasks("alice")[0]
assert updated_task["title"] == "Read Chapter 1 & 2"

assert tasks.mark_as_done("alice", task["id"]) == True

task2 = tasks.add_task("alice", "Solve Worksheet", "Maths", "medium", "2026-09-20", 3)
assert tasks.delete_task("alice", task2["id"]) == True
assert tasks.delete_task("alice", 9999) == False

sample_tasks = [
    {"id": 1, "owner": "x", "title": "Overdue task", "subject": "S", "priority": "low",
     "due_date": "2026-09-20", "est_hours": 1, "status": "pending"},
    {"id": 2, "owner": "x", "title": "Urgent task", "subject": "S", "priority": "high",
     "due_date": "2026-09-30", "est_hours": 2, "status": "pending"},
    {"id": 3, "owner": "x", "title": "Done task", "subject": "S", "priority": "high",
     "due_date": "2026-09-01", "est_hours": 5, "status": "done"},
]

ordered_tasks = planner.sort_tasks_by_urgency(sample_tasks, "2026-09-24")
assert ordered_tasks[0]["title"] == "Overdue task"
assert planner.total_hours_needed(sample_tasks) == 3

weekly_plan = planner.make_weekly_plan(sample_tasks, 1, "2026-09-24", number_of_days=5)
total_planned_hours = sum(hours for day, title, hours in weekly_plan)
assert total_planned_hours == 3

stats = report.build_report(sample_tasks)
assert stats["total"] == 3
assert stats["done"] == 1
assert stats["pending"] == 2
assert stats["pending_hours"] == 3

os.remove(storage.USERS_FILE)
os.remove(storage.TASKS_FILE)

print("all tests passed")
