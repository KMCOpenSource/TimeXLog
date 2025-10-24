import tkinter as tk
import pandas as pd
import os
import sys
from tkinter import simpledialog, messagebox
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
GTD_LOG = os.path.join(BASE_DIR, "gtd_tasks.csv")

def load_gtd_tasks():
    if not os.path.exists(GTD_LOG):
        return ["Nothing here"], ["Welcome"], ["add a task"]

    df = pd.read_csv(GTD_LOG).fillna("")

    someday = df[df['GTD Type'] == "Someday/Maybe"]['Capture'].tolist()
    next_actions = df[df['GTD Type'] == "Next Action"]['Next Action'].tolist()
    projects = df[df['GTD Type'] == "Project"]['Capture'].tolist()

    return someday, next_actions, projects

def promote_task(task_text):
    action = simpledialog.askstring("⛏️ Next Action", f"What’s the next action for:\n\n🧠 {task_text}")
    if not action:
        return

    outcome = simpledialog.askstring("🎯 Outcome", f"What does 'done' look like for:\n\n🧠 {task_text}")
    if not outcome:
        return

    duration = simpledialog.askinteger("⏱️ Duration", f"How long will it take (in minutes)?")
    if not duration:
        return

    now = datetime.now()
    with open(GTD_LOG, "a", encoding="utf-8", newline='') as f:
        if os.stat(GTD_LOG).st_size == 0:
            f.write("Date,Time,Capture,GTD Type,Next Action,Outcome,Planned Duration(min)\n")
        f.write(f"{now.date()},{now.strftime('%H:%M:%S')},{task_text},Next Action,{action},{outcome},{duration}\n")

    messagebox.showinfo("✅ Promoted", f"Task promoted to Next Action:\n\n{action}")

def show_gtd_viewer(root=None):
    local_root = False
    if root is None:
        root = tk.Tk()
        local_root = True
    root.withdraw()

    window = tk.Toplevel(root)
    window.title("🧠 GTD Viewer")
    window.geometry("700x400")

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    someday, actions, projects = load_gtd_tasks()

    # === Someday Section with Promote Buttons ===
    someday_box = tk.Frame(frame)
    tk.Label(someday_box, text="🧠 Someday/Maybe", font=('Helvetica', 10, 'bold')).pack(anchor="w")

    for task in someday:
        row = tk.Frame(someday_box)
        tk.Label(row, text=f"- {task}", anchor='w', wraplength=300, justify="left").pack(side='left', padx=(0,10))
        tk.Button(row, text="Promote", command=lambda t=task: promote_task(t)).pack(side='right')
        row.pack(anchor='w', fill='x', pady=2)

    someday_box.pack(side='left', expand=True, fill='both', padx=5)

    # === Next Actions Section ===
    next_box = tk.Frame(frame)
    tk.Label(next_box, text="🛠 Next Actions", font=('Helvetica', 10, 'bold')).pack(anchor="w")
    text = tk.Text(next_box, height=12, wrap='word')
    text.pack(fill="both")
    text.insert("1.0", "\n".join(f"- {item}" for item in actions))
    text.config(state='disabled')
    next_box.pack(side='left', expand=True, fill='both', padx=5)

    # === Projects Section ===
    project_box = tk.Frame(frame)
    tk.Label(project_box, text="🎯 Projects", font=('Helvetica', 10, 'bold')).pack(anchor="w")
    text = tk.Text(project_box, height=12, wrap='word')
    text.pack(fill="both")
    text.insert("1.0", "\n".join(f"- {item}" for item in projects))
    text.config(state='disabled')
    project_box.pack(side='left', expand=True, fill='both', padx=5)

    if local_root:
        window.mainloop()

    return window
