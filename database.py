import sqlite3
from datetime import date

def create_database():

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        description TEXT,
        category TEXT,
        priority TEXT,
        due_date TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eod_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summary TEXT,
        created_date TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_task(task_name, description, category, priority, due_date):

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks
    (task_name, description, category, priority, due_date)
    VALUES (?, ?, ?, ?, ?)
    """, (task_name, description, category, priority, due_date))

    conn.commit()
    conn.close()


def get_tasks():

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def complete_task(task_id):

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET completed = 1
    WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


def get_overdue_tasks():

    today = str(date.today())

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM tasks
    WHERE completed = 0
    AND due_date < ?
    """, (today,))

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def delete_all_tasks():

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")

    conn.commit()
    conn.close()


def get_task_statistics():

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
    pending = cursor.fetchone()[0]

    conn.close()

    return total, completed, pending


def save_eod_summary(summary, created_date):

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO eod_summaries
    (summary, created_date)
    VALUES (?, ?)
    """, (summary, created_date))

    conn.commit()
    conn.close()


def get_eod_summaries():

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM eod_summaries
    ORDER BY id DESC
    """)

    summaries = cursor.fetchall()

    conn.close()

    return summaries