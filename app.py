import streamlit as st
import json
import os
from datetime import date

# Page Settings
st.set_page_config(
    page_title="Personal Productivity Agent",
    page_icon="📋",
    layout="centered"
)

# Sidebar
st.sidebar.title("📊 Dashboard")

st.sidebar.info("""
Personal Productivity Agent

✅ Track Tasks
✅ Manage Work
✅ Generate Daily Summary
""")

# Title
st.title("📋 Personal Productivity Agent")
st.caption("AI-Powered Daily Task Management System")
st.write("Today's Date:", date.today())

# Create JSON file if not exists
if not os.path.exists("tasks.json"):
    with open("tasks.json", "w") as f:
        json.dump([], f)

# Load tasks
with open("tasks.json", "r") as f:
    tasks = json.load(f)

# Add Task Section
st.subheader("➕ Add New Task")

new_task = st.text_input("Enter Task")

category = st.selectbox(
    "Select Category",
    ["Work", "Study", "Personal", "Health"]
)

if st.button("Add Task"):

    if new_task.strip() != "":

        tasks.append({
            "task": new_task,
            "category": category,
            "done": False
        })

        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

        st.success("Task Added Successfully!")
        st.rerun()

# Show Tasks
st.subheader("📝 Your Tasks")

for i, task in enumerate(tasks):

    done = st.checkbox(
    f"{task['task']} ({task.get('category','General')})",
    value=task["done"],
    key=f"task_{i}"
)
    tasks[i]["done"] = done

# Save Updated Tasks
with open("tasks.json", "w") as f:
    json.dump(tasks, f)

# Statistics
completed = len([t for t in tasks if t["done"]])
pending = len([t for t in tasks if not t["done"]])

st.subheader("📈 Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total", len(tasks))

with col2:
    st.metric("Completed", completed)

with col3:
    st.metric("Pending", pending)

# EOD Summary
st.subheader("🤖 Daily Report")

if st.button("Generate EOD Summary"):

    report = f"""
📋 Daily Productivity Report

Total Tasks: {len(tasks)}
Completed Tasks: {completed}
Pending Tasks: {pending}

Keep going! Focus on completing your pending tasks tomorrow.
"""

    st.success(report)

# Footer
st.markdown("---")
st.caption("Developed using Python & Streamlit")
st.markdown("---")

# Reset Tasks
st.subheader("🗑️ Reset Tasks")

if st.button("Clear All Tasks"):

    tasks = []

    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

    st.success("All tasks cleared successfully!")

    st.rerun()

# Footer
st.markdown("---")

st.subheader("🎯 Project Objective")

st.info("""
This application helps users manage daily tasks,
track productivity, monitor completed work,
and generate end-of-day productivity reports.
""")