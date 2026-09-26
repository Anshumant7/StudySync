import os
import storage
import users
import tasks
import planner
import report
from helpers import is_valid_date, is_valid_priority, is_valid_hours, days_between

storage.USERS_FILE = "data/test_users.json"
storage.TASKS_FILE = "data/test_tasks.json"

tests_passed = 0
tests_failed = 0


def check(condition, description):
    global tests_passed, tests_failed
    if condition:
        print(f"PASS - {description}")
        tests_passed += 1
    else:
        print(f"FAIL - {description}")
        tests_failed += 1


def clean_up():
    for file_path in (storage.USERS_FILE, storage.TASKS_FILE):
        if os.path.exists(file_path):
            os.remove(file_path)


clean_up()

# helpers.py
check(is_valid_date("2026-12-25") is True, "a real date counts as valid")
check(is_valid_date("25-12-2026") is False, "a wrongly formatted date is invalid")
check(is_valid_priority("HIGH") is True, "priority check ignores capital letters")
check(is_valid_priority("urgent") is False, "an unknown priority is invalid")
check(is_valid_hours("2.5") is True, "a positive number of hours is valid")
check(is_valid_hours("-1") is False, "a negative number of hours is invalid")
check(days_between("2026-09-24", "2026-09-27") == 3, "days_between counts the days correctly")

# users.py
check(users.sign_up("test_alice", "mypassword") is True, "signing up a new user works")
check(users.sign_up("test_alice", "mypassword") is False, "signing up the same username twice fails")
check(users.log_in("test_alice", "mypassword") is True, "logging in with the right password works")
check(users.log_in("test_alice", "wrongpassword") is False, "logging in with the wrong password fails")

# tasks.py
new_task = tasks.add_task("test_alice", "Read Chapter 1", "Physics", "high", "2026-12-01", 2)
check(new_task["title"] == "Read Chapter 1", "a new task is created with the right title")
check(len(tasks.load_my_tasks("test_alice")) == 1, "the new task shows up for that student")

edited_ok = tasks.edit_task("test_alice", new_task["id"], "title", "Read Chapter 1 & 2")
check(edited_ok is True, "editing a task works")
saved_tasks = storage.load_json(storage.TASKS_FILE)
found_task = tasks.find_task_by_id(saved_tasks, new_task["id"])
check(found_task["title"] == "Read Chapter 1 & 2", "the edited title was actually saved")
check(tasks.find_task_by_id(saved_tasks, 9999) is None, "looking up an id that doesn't exist returns None")

check(tasks.mark_as_done("test_alice", new_task["id"]) is True, "marking a task as done works")

second_task = tasks.add_task("test_alice", "Solve Worksheet", "Maths", "medium", "2026-09-20", 3)
check(tasks.delete_task("test_alice", second_task["id"]) is True, "deleting a task works")
check(tasks.delete_task("test_alice", 9999) is False, "deleting a task that does not exist fails safely")

users.sign_up("test_bob", "otherpassword")
check(tasks.edit_task("test_bob", new_task["id"], "title", "Hacked!") is False,
      "a student cannot edit another student's task")

# planner.py
sample_tasks = [
    {"id": 1, "owner": "x", "title": "Overdue task", "subject": "S", "priority": "low",
     "due_date": "2026-09-20", "est_hours": 1, "status": "pending"},
    {"id": 2, "owner": "x", "title": "Urgent task", "subject": "S", "priority": "high",
     "due_date": "2026-09-30", "est_hours": 2, "status": "pending"},
    {"id": 3, "owner": "x", "title": "Already done task", "subject": "S", "priority": "high",
     "due_date": "2026-09-01", "est_hours": 5, "status": "done"},
]
ordered = planner.sort_tasks_by_urgency(sample_tasks, "2026-09-24")
check(ordered[0]["title"] == "Overdue task", "an overdue task is scheduled first")
check(planner.total_hours_needed(sample_tasks) == 3, "total_hours_needed only adds up pending tasks")

weekly_plan = planner.make_weekly_plan(sample_tasks, 1, "2026-09-24", number_of_days=5)
total_planned_hours = sum(hours for _, _, hours in weekly_plan)
check(total_planned_hours == 3, "the weekly plan schedules all of the pending hours")
check(all(hours <= 1.0001 for _, _, hours in weekly_plan), "no single day goes over the daily hour limit")

# report.py
stats = report.build_report(sample_tasks)
check(stats["total"] == 3, "report counts all tasks")
check(stats["done"] == 1, "report counts completed tasks correctly")
check(stats["pending"] == 2, "report counts pending tasks correctly")
check(stats["pending_hours"] == 3, "report shows the correct remaining hours")

clean_up()

print(f"\n{tests_passed} passed, {tests_failed} failed")
