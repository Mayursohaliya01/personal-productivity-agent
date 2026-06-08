import streamlit as st
from database import (
    create_database,
    add_task,
    get_tasks,
    complete_task,
    get_overdue_tasks,
    delete_all_tasks,
    get_task_statistics
)

create_database()

st.set_page_config(
    page_title="Personal Productivity Agent",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Personal Productivity Agent")
st.caption("AI-Powered Daily Task Management System")

# Morning Check-In

st.subheader("🌅 Morning Check-In")

task_name = st.text_input("Task Name")

description = st.text_area("Task Description")

category = st.selectbox(
    "Category",
    ["Work", "Personal", "Health", "Learning"]
)

priority = st.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
)

due_date = st.date_input("Due Date")

if st.button("💾 Save Task"):

    if task_name.strip() != "":

        add_task(
            task_name,
            description,
            category,
            priority,
            str(due_date)
        )

        st.success("Task Saved Successfully")
        st.rerun()

# Overdue Tasks

st.divider()

st.subheader("⚠️ Overdue Tasks")

overdue_tasks = get_overdue_tasks()

if len(overdue_tasks) == 0:

    st.success("No Overdue Tasks 🎉")

else:

    for task in overdue_tasks:

        st.warning(
            f"{task[1]} | Priority: {task[4]} | Due: {task[5]}"
        )

# Task List

st.divider()

st.subheader("📋 Today's Tasks")

tasks = get_tasks()

completed_count = 0
pending_count = 0

for task in tasks:

    st.markdown(f"### 📌 {task[1]}")

    st.write(f"📝 Description: {task[2]}")
    st.write(f"📂 Category: {task[3]}")
    st.write(f"🔥 Priority: {task[4]}")
    st.write(f"📅 Due Date: {task[5]}")

    if task[6] == 0:

        pending_count += 1

        if st.button(
            f"✅ Mark Complete ({task[0]})",
            key=f"complete_{task[0]}"
        ):

            complete_task(task[0])
            st.rerun()

    else:

        completed_count += 1
        st.success("✅ Completed")

    st.divider()

# Statistics

st.subheader("📊 Productivity Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tasks", len(tasks))

with col2:
    st.metric("Completed Tasks", completed_count)

with col3:
    st.metric("Pending Tasks", pending_count)

# EOD Summary

st.divider()

st.subheader("🤖 Run My EOD")

if st.button("Generate EOD Summary"):

    summary = f"""
📋 Daily Productivity Report

Total Tasks: {len(tasks)}
Completed Tasks: {completed_count}
Pending Tasks: {pending_count}

Focus on pending tasks tomorrow and complete high priority items first.
"""

    st.success(summary)

# Tomorrow Plan

st.divider()

st.subheader("📅 Tomorrow Plan")

pending_found = False

for task in tasks:

    if task[6] == 0:

        pending_found = True
        st.write(f"➡️ {task[1]}")

if not pending_found:

    st.success("All tasks completed. Great job!")

# Weekly Review

st.divider()

st.subheader("📈 Weekly Review")

total, completed, pending = get_task_statistics()

completion_rate = 0

if total > 0:
    completion_rate = round((completed / total) * 100)

st.write(f"Total Tasks Created: {total}")
st.write(f"Completed Tasks: {completed}")
st.write(f"Pending Tasks: {pending}")
st.write(f"Completion Rate: {completion_rate}%")

if completion_rate >= 80:
    st.success("Excellent Productivity This Week 🚀")
elif completion_rate >= 50:
    st.info("Good Progress 👍")
else:
    st.warning("Try Completing More Tasks Next Week 💪")

# Clear Tasks

st.divider()

if st.button("🗑️ Clear All Tasks"):

    delete_all_tasks()
    st.rerun()

# Footer

st.divider()

st.info("Personal Productivity Agent | Capstone Project")