# Personal Productivity Agent

## Overview

Personal Productivity Agent is a task management application developed using Python and Streamlit. The application helps users organize daily activities, track task completion, monitor productivity, and generate end-of-day productivity reports.

## Features

* Add new tasks
* Categorize tasks (Work, Study, Personal, Health)
* Mark tasks as completed
* Track completed and pending tasks
* View productivity statistics
* Generate End-of-Day (EOD) productivity reports
* Simple and user-friendly dashboard

## Technology Stack

* Python
* Streamlit
* JSON Storage

## Project Architecture

User Interface (Streamlit)

↓

Python Application Logic

↓

JSON Data Storage (tasks.json)

## Installation

1. Clone or download the project.
2. Open the project folder in VS Code.
3. Install Streamlit:

```bash
pip install streamlit
```

4. Run the application:

```bash
python -m streamlit run app.py
```

## Project Structure

```text
Personal_Productivity_Agent/
│
├── app.py
├── tasks.json
├── README.md
└── requirements.txt
```

## How to Use

1. Enter a task name.
2. Select a category.
3. Click the Add Task button.
4. Mark completed tasks using checkboxes.
5. View productivity statistics.
6. Generate the End-of-Day Summary Report.

## Output

The application provides:

* Total Tasks Count
* Completed Tasks Count
* Pending Tasks Count
* Daily Productivity Report

## Future Enhancements

* User Authentication
* SQLite Database Integration
* AI-Based Task Suggestions
* Email Notifications
* Mobile Application Support
* Cloud Deployment

## Conclusion

The Personal Productivity Agent helps users efficiently manage their daily activities and improve productivity through task tracking and reporting features. The project demonstrates the use of Python, Streamlit, and data management concepts in a practical productivity application.

## Developer

Name: Mayur Sohaliya

Project: Personal Productivity Agent

Technology: Python, Streamlit, JSON
