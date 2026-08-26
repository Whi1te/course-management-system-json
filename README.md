# Course Management System

A command-line course management system built with Python. This initial version uses JSON for data persistence.

## Features

- Add, find, update, and delete students
- Add, find, update, and delete courses
- Enroll students in courses
- Drop courses
- Update grades
- View course rosters
- View a student's current courses
- Calculate semester or overall GPA
- Save and load data using JSON

## Project Structure

- `models.py` - Defines Student, Course, and Enrollment classes
- `student_service.py` - Student management logic
- `course_service.py` - Course management logic
- `enrollment_service.py` - Enrollment, grading, roster, and GPA logic
- `save_load.py` - JSON loading and saving logic
- `main.py` - Command-line interface and application entry point
- majors.json - Stores the list of available student majors

## How to Run

Make sure Python 3.10+ is installed.

From the project directory, run:

```bash
python main.py
```

Follow the menu prompts in the terminal.

## Data Persistence

Application data is currently stored in JSON format.

Student and Course objects are serialized into JSON, while Enrollment records store student IDs and course IDs. When data is loaded, these relationships are reconstructed into Python objects.

## Future Improvements
- Migrate persistence from JSON to SQLite
- Add automated tests
- Improve CLI output formatting
- Add additional reporting features