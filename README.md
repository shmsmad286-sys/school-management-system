# School Management System

A simple desktop app to manage students, teachers and grades, built with pure Python and Object-Oriented Programming (Tkinter GUI). No database and no external libraries.

## Features
- Add and delete students
- Add teachers with their subjects
- Record grades per student and subject
- Automatic grade average for each student

## Screenshots
![Students](docs/students.png)
![Teachers](docs/teachers.png)
![Grades](docs/grades.png)

## OOP Design
| Class | Role | Concept |
|---|---|---|
| `Person` | Base class: name, age | Base class |
| `Student(Person)` | ID and private grades | Inheritance, encapsulation |
| `Teacher(Person)` | Subject taught | Inheritance |
| `School` | Holds all students and teachers | Aggregation |
| `App` | Tkinter window and tabs | GUI |

## Run
```bash
python school_management.py
```
Requires Python 3 (Tkinter is included with the standard installer).

## Note
Data is stored in memory while the app is running.

## Team
[Team 5]
