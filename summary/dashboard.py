import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
FOCUS_LOG = os.path.join(BASE_DIR, "focus_log.csv")

def show_focus_dashboard():
    df = pd.read_csv(FOCUS_LOG)

    # Convert start date to datetime
    df['Start Date'] = pd.to_datetime(df['Start Date'])

    # Aggregate total minutes per day
    df_summary = df.groupby('Start Date')['Actual(min)'].sum().reset_index()

    # Filter for last 7 days
    last_7_days = datetime.now() - timedelta(days=7)
    df_summary = df_summary[df_summary['Start Date'] >= last_7_days]

    plt.figure(figsize=(10, 4))
    plt.plot(df_summary['Start Date'], df_summary['Actual(min)'], marker='o', color='green')
    plt.title('🧠 Focus Minutes per Day (Last 7 Days)')
    plt.xlabel('Date')
    plt.ylabel('Total Focus Minutes')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    show_focus_dashboard()
