import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import threading
from ui.task_prompt import prompt_task
from ui.timer_window import show_timer
from blocker.app_blocker import block_apps
from utils.logger import log_task_start, log_task_end, log_task_abort
from autostart import add_to_startup
from state import task_state
from summary.daily_summary import generate_daily_summary

def main():
    add_to_startup()
    blocker_thread = threading.Thread(target=block_apps, daemon=True)
    blocker_thread.start()

    while True:
        if task_state.current_task_active:
            continue

        data = prompt_task()
        if not data or not data.get("capture"):
            continue

        # Ensure we have a valid duration (minutes) before starting the timer.
        duration = data.get("duration")
        if not isinstance(duration, int) or duration <= 0:
            # nothing to time — skip
            print("[DEBUG] No valid duration provided, skipping.")
            continue

        task_state.current_task_active = True
        log_data = log_task_start(
            data['capture'],
            data['next_action'],
            data['outcome'],
            data['duration']
        )
        # k = key (field name), v = value (field value) from the data dictionary
        for k, v in data.items():
            log_data[k] = v
        # Ensure 'task' field is set for logging
        log_data['task'] = data.get('capture', data.get('next_action', ''))
        task_state.log_data = log_data

        print("[DEBUG] Before show_timer")
        status = show_timer(data['next_action'], duration)
        print(f"[DEBUG] After show_timer, status: {status}")

        # 🧹 Cleanup
        task_state.current_task_active = False
        task_state.log_data = None
        print(f"[DEBUG] After cleanup, current_task_active: {task_state.current_task_active}")

        # 🗂 Log result
        if status == "completed":
            log_task_end(log_data)
        elif status == "aborted":
            log_task_abort(log_data)
        else:
            print("⚠️ Timer returned unknown status. Skipping log.")
        
        print(f"[DEBUG] Timer exited with status: {status}")


        # 📈 Always generate summary
        print("[DEBUG] Generating summary…")
        generate_daily_summary()
        print("[DEBUG] Summary generated.")

if __name__ == "__main__":
    main()
