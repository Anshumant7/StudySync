# StudySync

A command-line study planner I built to keep track of my own assignments across different subjects. It is written in plain Python, with two JSON files handling storage instead of a database.

## Motivation

This program allows you to keep track of deadlines across subjects with a priority based hierarchy which allows you to get work done on time.

## Features

- Sign up and log in using passwords stored as SHA-256 hashes rather than plain text
- Add, edit, mark done and delete tasks
- A "smart order" view that ranks pending tasks by urgency, based on due date and priority
- A weekly planner that spreads tasks across the next 7 days according to how many hours are available per day
- A short report showing completion percentage and hours remaining per subject

## Requirements

Python 3.9 or later. No external libraries are used.

## Running the Program

```
git clone https://github.com/Anshumant7/StudySync
cd StudySync
python main.py
```

## Running the Tests

```
python tests.py
```

tests.py does not use a testing framework. It just runs a series of assert statements and prints "all tests passed" at the end. If something is broken, Python stops on whichever assert failed and shows the line number.

## File Overview

- main.py, the menu-driven entry point
- users.py, sign-up and login
- tasks.py, adding, editing, deleting and completing tasks
- planner.py, urgency scoring and the weekly plan
- report.py, the progress summary
- storage.py, reads and writes the JSON data files
- helpers.py, input validation for dates, hours and priority
- tests.py, the test script

## Limitations

Passwords are hashed but not salted, and all data is stored locally in plain JSON.