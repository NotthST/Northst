commands = {
    "Process Check": {
        "cmd": 'ps -ef | grep -Ei "p_ctmag|p_ctmap|p_ctmaw"',
        "formatter": "ps"
    },
    "Service Status": {
        "cmd": (
            'for s in "qsoft for BSC" "MesaExtractor.ksh" "msqft for Mesa" "recuperationAR" '
            '"synchroCalypso" "synchroCNM" "synchroChestrator" "synchroOneClick" '
            '"synchroDocStoreMailSender" "synchroDocStoreReSender" "synchroSophis" '
            '"bsc-events-dispatcher.jar"; '
            'do ps -ef | grep -v grep | grep -i "$s" > /dev/null && echo "$s is RUNNING" || echo "$s is NOT RUNNING"; done'
        ),
        "formatter": "status"
    },
    "Directory Listing": {
        "cmd": 'ls -l /Soft/sesame /Soft/sesame_log /Soft/sesame_confirms /Soft/sesame_data /Home/sesame /Home/segueest /data',
        "formatter": "ls"
    }
}

# --- Formatters ---
def format_ps(output):
    rows = []
    for line in output.splitlines():
        if "grep" in line or not line.strip():
            continue
        parts = line.split(None, 7)
        if len(parts) == 8:
            rows.append(parts)
    headers = ["UID", "PID", "PPID", "C", "STIME", "TTY", "TIME", "CMD"]
    return tabulate(rows, headers, tablefmt="grid")

def format_status(output):
    rows = []
    for line in output.splitlines():
        if "is RUNNING" in line or "is NOT RUNNING" in line:
            service, status = line.rsplit(" is ", 1)
            rows.append([service.strip(), status.strip()])
    headers = ["Service", "Status"]
    return tabulate(rows, headers, tablefmt="grid")

def format_ls(output):
    rows = []
    for line in output.splitlines():
        if line.startswith("total") or not line or line.endswith(":"):
            continue
        parts = line.split(None, 8)
        if len(parts) >= 9:
            rows.append([
                parts[0], parts[2], parts[3], parts[4],
                f"{parts[5]} {parts[6]} {parts[7]}", parts[8]
            ])
    headers = ["Perms", "Owner", "Group", "Size", "Date", "Filename"]
    return tabulate(rows, headers, tablefmt="grid")

# --- SSH Execution ---
def run_remote_commands():
    try:
        print("[INFO] Connecting to SSH server...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        for label, config in commands.items():
            print(f"\n========== {label} ==========")
            stdin, stdout, stderr = ssh.exec_command(config["cmd"])
            raw_out = stdout.read().decode().strip()
            raw_err = stderr.read().decode().strip()

            print("\n--- RAW OUTPUT ---")
            print(raw_out or raw_err or "(no output)")

            print("\n--- FORMATTED OUTPUT ---")
            if config["formatter"] == "ps":
                print(format_ps(raw_out))
            elif config["formatter"] == "status":
                print(format_status(raw_out))
            elif config["formatter"] == "ls":
                print(format_ls(raw_out))
            else:
                print("(no formatting defined)")

        ssh.close()
        print("\n[INFO] SSH session closed.")

    except Exception as e:
        print(f"[ERROR] SSH connection or command failed: {e}")

# --- Entry Point ---
if __name__ == "__main__":
    run_remote_commands()
✅ Next Step: Share It via a Link
Would you like me to:

Create a GitHub Gist with this version?

Or export it to a .txt or .zip file you can download?

Let me know and I’ll generate the link immediately.








You said:
i mean for sharing just take off the commands and keep the structure 


ChatGPT said:
Got it! Here's the corporate-friendly template of your SSH script — stripped of any specific or sensitive commands. This version:

Keeps the structure and logic intact

Leaves placeholders where your actual commands and parsers go

Is clean and ready to be filled with project-specific checks later

✅ SSH Monitoring Template (No Commands)
python
Copy
Edit
"""
Generic SSH Monitoring Script Template
Author: [Your Name]
Purpose: Securely connect to a remote server via SSH, run predefined checks,
         and display outputs in both raw and formatted views.

Dependencies:
- paramiko: for SSH connection
- tabulate: for clean tabular formatting
Install with: pip install paramiko tabulate
"""

import paramiko
from tabulate import tabulate

# --- SSH Configuration ---
hostname = "your.remote.host"
port = 22
username = "your-username"
password = "your-password"  # Consider using getpass.getpass() for security

# --- Commands to Run (fill in your use cases) ---
commands = {
    "Check 1": {
        "cmd": 'your-command-here',
        "formatter": "your_formatter"
    },
    "Check 2": {
        "cmd": 'another-command-here',
        "formatter": "another_formatter"
    },
}

# --- Formatters (customize these for your output structure) ---
def your_formatter(output):
    """
    Example formatter function.
    Adapt this to parse and format your command output.
    """
    rows = []
    for line in output.splitlines():
        rows.append([line.strip()])
    return tabulate(rows, headers=["Output"], tablefmt="grid")

# Example fallback formatter if none defined
def raw_formatter(output):
    return tabulate([[line] for line in output.splitlines()], headers=["Output"], tablefmt="grid")

# --- SSH Execution ---
def run_remote_commands():
    try:
        print("[INFO] Connecting to SSH server...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        for label, config in commands.items():
            print(f"\n========== {label} ==========")
            stdin, stdout, stderr = ssh.exec_command(config["cmd"])
            raw_out = stdout.read().decode().strip()
            raw_err = stderr.read().decode().strip()

            print("\n--- RAW OUTPUT ---")
            print(raw_out or raw_err or "(no output)")

            print("\n--- FORMATTED OUTPUT ---")
            formatter_name = config.get("formatter")
            if formatter_name == "your_formatter":
                print(your_formatter(raw_out))
            else:
                print(raw_formatter(raw_out))

        ssh.close()
        print("\n[INFO] SSH session closed.")

    except Exception as e:
        print(f"[ERROR] SSH connection or command failed: {e}")

# --- Entry Point ---
if __name__ == "__main__":
    run_remote_commands()
