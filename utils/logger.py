import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
FOCUS_LOG = os.path.join(BASE_DIR, "focus_log.csv")


def log_task_start(capture, next_action, outcome, planned_duration):
    now = datetime.now()
    # Returns a dictionary with the following keys:
    # 'capture', 'next_action', 'outcome', 'planned_duration', 'start_time'
    return {
        "capture": capture,
        "next_action": next_action,
        "outcome": outcome,
        "planned_duration": planned_duration,
        "start_time": now,
    }


def log_task_end(log_data):
    # Expects log_data to contain at least: 'task', 'planned_duration', 'start_time'
    end_time = datetime.now()
    start_time = log_data["start_time"]

    actual_duration = round((end_time - start_time).total_seconds() / 60)

    start_date = start_time.strftime("%Y-%m-%d")
    start_clock = start_time.strftime("%H:%M:%S")
    end_date = end_time.strftime("%Y-%m-%d")
    end_clock = end_time.strftime("%H:%M:%S")

    try:
        with open(FOCUS_LOG, "a", encoding="utf-8", newline='') as f:
            if f.tell() == 0:
                f.write("Task,Planned(min),Actual(min),Start Date,Start Time,End Date,End Time\n")
            f.write(f"{log_data['task']},{log_data['planned_duration']},{actual_duration},"
                    f"{start_date},{start_clock},{end_date},{end_clock}\n")
    except PermissionError:
        print("[✗] Cannot write to log. File is open or locked.")
    except Exception as e:
        print(f"[✗] Logging failed: {e}")
def log_task_abort(log_data):
    # Expects log_data to contain at least: 'capture', 'next_action', 'outcome', 'planned_duration', 'start_time'
    end_time = datetime.now()
    start_time = log_data["start_time"]
    actual_duration = round((end_time - start_time).total_seconds() / 60)

    start_date = start_time.strftime("%Y-%m-%d")
    start_clock = start_time.strftime("%H:%M:%S")
    end_date = end_time.strftime("%Y-%m-%d")
    end_clock = end_time.strftime("%H:%M:%S")

    with open(FOCUS_LOG, "a", encoding="utf-8", newline='') as f:
        if f.tell() == 0:
            f.write("Capture,Next Action,Outcome,Planned(min),Actual(min),Start Date,Start Time,End Date,End Time,Status\n")
        f.write(f"{log_data['capture']},{log_data['next_action']},{log_data['outcome']},"
                f"{log_data['planned_duration']},{actual_duration},{start_date},{start_clock},{end_date},{end_clock},Aborted\n")
