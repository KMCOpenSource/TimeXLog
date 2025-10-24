import tkinter as tk
from tkinter import messagebox
from state import task_state
from utils.logger import log_task_abort,log_task_end

def show_timer(task, minutes):
    win = tk.Tk()
    win.title("⏳ Gyan's Timer")
    win.geometry("300x120")
    win.attributes("-topmost", True)
    win.resizable(False, False)
    win.attributes('-toolwindow', True)

    label = tk.Label(win, font=("Helvetica", 12), text=f"Task: {task}")
    label.pack(pady=10)

    countdown = tk.Label(win, font=("Helvetica", 16))
    countdown.pack()

    time_left = {"seconds": minutes * 60}
    countdown_id = {"after_id": None}
    result = {"status": None}

    def update():
        # print("[DEBUG] update() called, seconds left:", time_left["seconds"])
        if time_left["seconds"] <= 0:
            countdown.config(text="Time Left: 00:00")
            result["status"] = "completed"
            # print("[DEBUG] Timer completed, closing window.")
            win.quit()
            win.destroy() 
        else:
            mins, secs = divmod(time_left["seconds"], 60)
            countdown.config(text=f"Time Left: {mins:02d}:{secs:02d}")
            time_left["seconds"] -= 1
            countdown_id["after_id"] = win.after(1000, update)

    def close():
        print("[DEBUG] close() called")
        if countdown_id["after_id"]:
            win.after_cancel(countdown_id["after_id"])
        if task_state.log_data:
            log_task_abort(task_state.log_data)
            result["status"] = "aborted"
        task_state.current_task_active = False
        win.quit()
        win.destroy() 
        print("[DEBUG] Window destroyed in close()")

    win.protocol("WM_DELETE_WINDOW", close)
    # print("[DEBUG] Before update() call")
    update()
    # print("[DEBUG] After update() call, before mainloop")
    win.mainloop()
    # print("[DEBUG] mainloop exited, result status:", result["status"])
    return result["status"]
