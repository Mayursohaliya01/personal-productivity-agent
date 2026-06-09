import streamlit as st
from groq import Groq
from datetime import date

from database import (
    create_database,
    add_task,
    get_tasks,
    complete_task,
    get_overdue_tasks,
    delete_all_tasks,
    get_task_statistics,
    save_eod_summary,
    get_eod_summaries
)

create_database()

st.set_page_config(
    page_title="Personal Productivity Agent",
    page_icon="📋",
    layout="wide"
)
st.sidebar.title("📊 Dashboard")

st.sidebar.info("""
Personal Productivity Agent

✅ Task Management
✅ AI EOD Summary
✅ Tomorrow Planner
✅ Weekly Review
""")

st.title("📋 Personal Productivity Agent")
st.caption("AI-Powered Daily Task Management System")

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

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

    with st.spinner("Generating AI Summary..."):

        prompt = f"""
        Create a professional End Of Day productivity summary.

        Total Tasks: {len(tasks)}
        Completed Tasks: {completed_count}
        Pending Tasks: {pending_count}

        Mention:
        - Today's productivity
        - Completed work
        - Pending work
        - Suggestions for tomorrow

        Keep the summary under 120 words.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        summary = response.choices[0].message.content

        save_eod_summary(
            summary,
            str(date.today())
        )

        st.success(summary)

# Tomorrow Plan

# Tomorrow Plan

st.divider()

st.subheader("📅 AI Tomorrow Planner")

if st.button("Generate Tomorrow Plan"):

    pending_tasks = []

    for task in tasks:

        if task[6] == 0:
            pending_tasks.append(task[1])

    if len(pending_tasks) == 0:

        st.success("All tasks completed. No plan needed for tomorrow 🎉")

    else:

        task_text = ", ".join(pending_tasks)

        prompt = f"""
        Create a productivity plan for tomorrow.

        Pending Tasks:
        {task_text}

        Give:
        1. Task priorities
        2. Suggested order of work
        3. Short motivational advice

        Keep it under 150 words.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        tomorrow_plan = response.choices[0].message.content

        st.success(tomorrow_plan)

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
st.divider()

st.subheader("📚 Previous EOD Summaries")

summaries = get_eod_summaries()

if len(summaries) == 0:

    st.info("No summaries generated yet.")

else:

    for summary in summaries:

        st.write(f"📅 {summary[2]}")
        st.write(summary[1])

        st.divider()

# Clear Tasks

st.divider()

if st.button("🗑️ Clear All Tasks"):

    delete_all_tasks()
    st.rerun()

# Footer

st.divider()

st.info("Personal Productivity Agent | Capstone Project")