import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
GTD_LOG = os.path.join(BASE_DIR, "gtd_tasks.csv")


def log_gtd_task(data):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    with open(GTD_LOG, "a", encoding="utf-8", newline='') as f:
        if f.tell() == 0:
            f.write("Date,Time,Capture,GTD Type,Next Action,Outcome,Planned Duration(min)\n")
        f.write(f"{date},{time},{data['capture']},{data['gtd_type']},{data['next_action']},{data['outcome']},{data['duration']}\n")
