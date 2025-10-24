import tkinter as tk
from tkinter import simpledialog
from ui.gtd_viewer import show_gtd_viewer

def prompt_task():
    root = tk.Tk()
    root.withdraw()

    # show GTD context window
    gtd_window = show_gtd_viewer(root)

    # Now prompt for task entry
    capture = simpledialog.askstring("📥 Capture", "What’s on your mind?")
    if not capture:
        gtd_window.destroy()
        return None


    duration = simpledialog.askinteger("⏱ Time Block", "How many minutes will you focus?")
    if not duration:
        gtd_window.destroy()
        return {
            "capture": capture,
            "gtd_type": "Someday/Maybe",
            "next_action": "",
            "outcome": "",
            "duration": duration
        }

    gtd_window.destroy()


    return {
        # capture: the user's initial thought or task
        # gtd_type: 'Next Action' or 'Project' or 'Someday/Maybe'
        # next_action: the next physical action to take
        # outcome: the desired outcome for the task
        # duration: the planned focus time in minutes
        "capture": capture,
        "gtd_type": "",
        "next_action": "",
        "outcome": "",
        "duration": duration
    }
