import streamlit as st
from datetime import date

# Page config
st.set_page_config(page_title="📝To-Do List", layout="centered")

# ---- Add Background Image ----
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
background: rgba(255,255,255,0.8);
}

.stButton>button {
    background-color: #6c63ff;
    color: white;
    border-radius: 10px;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.title("📝To-Do List App")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Function to trigger rerun
def rerun():
    st.session_state.rerun = not st.session_state.get("rerun", False)

# Add a new task
with st.form("Add Task"):
    task_name = st.text_input("Task Name")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Due Date", value=date.today())
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if task_name.strip() != "":
            st.session_state.tasks.append({
                "name": task_name,
                "priority": priority,
                "due_date": due_date,
                "completed": False
            })
            st.success(f"Task '{task_name}' added!")
            rerun()
        else:
            st.error("Please enter a task name!")

# Filter tasks
filter_status = st.radio("Filter Tasks:", ["All", "Pending", "Completed"])

# Display tasks
st.subheader("Your Tasks")
if not st.session_state.tasks:
    st.info("No tasks added yet!")
else:
    for idx, task in enumerate(st.session_state.tasks):
        if (filter_status == "Pending" and task["completed"]) or \
           (filter_status == "Completed" and not task["completed"]):
            continue

        col1, col2, col3, col4 = st.columns([0.5, 0.2, 0.2, 0.2])
        task_display = f"{task['name']} (Priority: {task['priority']}, Due: {task['due_date']})"
        if task["completed"]:
            col1.markdown(f"~~{task_display}~~")
        else:
            col1.write(task_display)

        if col2.button("✅ Done", key=f"done_{idx}"):
            st.session_state.tasks[idx]["completed"] = True
            rerun()

        if col3.button("✏️ Edit", key=f"edit_{idx}"):
            new_name = st.text_input("Edit Task", value=task["name"], key=f"input_{idx}")
            if new_name.strip() != "":
                st.session_state.tasks[idx]["name"] = new_name
                rerun()

        if col4.button("🗑️ Delete", key=f"delete_{idx}"):
            st.session_state.tasks.pop(idx)
            rerun()

# Clear all tasks
if st.button("🧹 Clear All Tasks"):
    st.session_state.tasks = []
    rerun()
    st.success("All tasks cleared!")