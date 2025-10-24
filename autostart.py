import winreg as reg
import os
import sys


def add_to_startup(app_name="FocusEnforcer"):
    script_path = os.path.realpath("main.pyw")  # .pyw = no console window

    # Prefer pythonw.exe (no console) if it exists alongside the Python executable
    python_dir = os.path.dirname(sys.executable)
    pythonw_candidate = os.path.join(python_dir, "pythonw.exe")
    if os.path.exists(pythonw_candidate):
        python_path = pythonw_candidate
    else:
        python_path = sys.executable  # fallback

    full_cmd = f'"{python_path}" "{script_path}"'

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, full_cmd)
        reg.CloseKey(reg_key)
        print(f"[✓] Auto-start entry created for {app_name}")
    except Exception as e:
        print(f"[✗] Failed to add to startup: {e}")
