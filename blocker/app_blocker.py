import psutil
import time
import json
import os
from state import task_state

def load_blocked_apps():
    config_path = os.path.join(os.path.dirname(__file__), '../config/blocked_apps.json')
    config_path = os.path.abspath(config_path)
    with open(config_path, 'r') as f:
        return [app.lower() for app in json.load(f)]

def block_apps():
    blocked = load_blocked_apps()
    while True:
        if task_state.current_task_active:
            time.sleep(2)  # don't block during active task
            continue

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() in blocked:
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(1)
