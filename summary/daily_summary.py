import os
import sys
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
FOCUS_LOG = os.path.join(BASE_DIR, "focus_log.csv")

def generate_daily_summary():
    try:
        df = pd.read_csv(FOCUS_LOG, names=[
            "Capture", "Task", "Outcome", 
            "Duration(min)", "Actual(min)", 
            "Start Date", "Start Time", 
            "End Date", "End Time", 
            "Status"
        ], skiprows=1, engine="python", on_bad_lines='skip')
    except FileNotFoundError:
        print("No logs yet.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    df_today = df[df['Start Date'] == today]

    if df_today.empty:
        print("No focus data for today.")
        return

    completed = df_today[df_today["Status"] == "completed"]
    aborted = df_today[df_today["Status"] == "aborted"]

    total_tasks = len(df_today)
    total_minutes = df_today['Actual(min)'].sum()

    print("\n🧠 DAILY FOCUS SUMMARY")
    print(f"📅 Date: {today}")
    print(f"✅ Tasks Attempted: {total_tasks}")
    print(f"⏱ Total Logged Focus: {total_minutes} mins")
    print(f"🎯 Completed: {len(completed)} | ❌ Aborted: {len(aborted)}")

    # Optional: Print tasks
    print("\n🗂 Task Breakdown:")
    for i, row in df_today.iterrows():
        print(f" - {row['Task']} ({row['Actual(min)']} min) - {row['Status']}")

if __name__ == "__main__":
    generate_daily_summary()
