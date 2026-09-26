import getpass
from helpers import is_valid_date, is_valid_priority, is_valid_hours
from users import sign_up, log_in
from tasks import load_my_tasks, add_task, edit_task, mark_as_done, delete_task
from planner import sort_tasks_by_urgency, make_weekly_plan
from report import print_report

def show_task(task):
    print(f"[{task['id']}] {task['title']} | {task['subject']} | {task['priority']} "
          f"| due {task['due_date']} | {task['est_hours']}h | {task['status']}")

def ask_for_new_task(username):
    title = input("Task title: ").strip()
    subject = input("Subject: ").strip()
    if subject == "":
        subject = "General"

    priority = input("Priority (low/medium/high): ").strip()
    while not is_valid_priority(priority):
        print("Please type low, medium or high.")
        priority = input("Priority (low/medium/high): ").strip()

    due_date = input("Due date (YYYY-MM-DD): ").strip()
    while not is_valid_date(due_date):
        print("Please use the format YYYY-MM-DD, for example 2026-12-25.")
        due_date = input("Due date (YYYY-MM-DD): ").strip()

    est_hours = input("How many hours do you think it will take? ").strip()
    while not is_valid_hours(est_hours):
        print("Please type a positive number, for example 2.5")
        est_hours = input("How many hours do you think it will take? ").strip()

    task = add_task(username, title, subject, priority, due_date, est_hours)
    print("Task added!")
    show_task(task)

def student_menu(username):
    today = input("What is today's date? (YYYY-MM-DD): ").strip()
    while not is_valid_date(today):
        today = input("Please use YYYY-MM-DD format. Today's date: ").strip()

    while True:
        print("\n1) Add task   2) View tasks   3) Edit task   4) Mark done")
        print("5) Delete task   6) Smart order   7) Weekly plan   8) Report   9) Logout")
        choice = input("> ").strip()

        try:
            if choice == "1":
                ask_for_new_task(username)

            elif choice == "2":
                my_tasks = load_my_tasks(username)
                if len(my_tasks) == 0:
                    print("You have no tasks yet.")
                for task in my_tasks:
                    show_task(task)

            elif choice == "3":
                task_id = int(input("Task id to edit: "))
                field = input("Which field? (title/subject/priority/due_date/est_hours): ").strip()
                new_value = input("New value: ").strip()
                if edit_task(username, task_id, field, new_value):
                    print("Task updated.")
                else:
                    print("Could not find that task.")

            elif choice == "4":
                task_id = int(input("Task id to mark done: "))
                if mark_as_done(username, task_id):
                    print("Nicely done!")
                else:
                    print("Could not find that task.")

            elif choice == "5":
                task_id = int(input("Task id to delete: "))
                if delete_task(username, task_id):
                    print("Task deleted.")
                else:
                    print("Could not find that task.")

            elif choice == "6":
                my_tasks = load_my_tasks(username)
                ordered_tasks = sort_tasks_by_urgency(my_tasks, today)
                position = 1
                for task in ordered_tasks:
                    print(position, end=" ")
                    show_task(task)
                    position += 1

            elif choice == "7":
                hours_per_day = float(input("How many hours can you study per day? "))
                my_tasks = load_my_tasks(username)
                plan = make_weekly_plan(my_tasks, hours_per_day, today)
                for day, title, hours in plan:
                    print(f"{day}  {hours:.1f}h  {title}")

            elif choice == "8":
                my_tasks = load_my_tasks(username)
                print_report(my_tasks)

            elif choice == "9":
                print("Logged out. See you next time!")
                return

            else:
                print("Please choose a number from the menu.")

        except ValueError:
            print("That doesn't look like a valid number, try again.")

def main():
    print("Welcome to StudySync!")
    while True:
        choice = input("\n1) Sign up   2) Log in   3) Quit\n> ").strip()

        if choice == "1":
            username = input("Choose a username: ").strip()
            password = getpass.getpass("Choose a password: ")
            if sign_up(username, password):
                print("Account created! You can log in now.")
            else:
                print("That username is already taken.")

        elif choice == "2":
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            if log_in(username, password):
                print(f"Welcome back, {username}!")
                student_menu(username)
            else:
                print("Wrong username or password.")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Please choose 1, 2 or 3.")


if __name__ == "__main__":
    main()