# Problem Statement

This program allows you to keep track of deadlines across subjects with a priority based hierarchy which allows you to get work done on time, the priority is decided on the basis of urgency, due date and user input priority level.

## Scope

StudySync is a command-line application. It stores data locally in two JSON files rather than a database, which was sufficient for the scale of the problem and the tools covered so far in the course. It supports account creation, task management, and two planning views: an urgency-based ordering of tasks, and a weekly plan built from the study hours available.

It does not include a graphical interface, reminders, or syncing across devices. These are reasonable directions for future work, but were outside the scope of what this version needed to do.

## Target Users

Students who want a simple, private way to track coursework.

## Core Features

- Account creation and login, with hashed passwords
- Task creation, editing, completion and deletion
- Urgency-based task ordering, using due date and priority
- A 7-day study plan generated from available hours per day
- A summary report of completed and remaining work