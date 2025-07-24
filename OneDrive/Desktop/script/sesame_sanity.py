import paramiko
from tabulate import tabulate

hostname = "your.remote.host"
port = 22
username = "your-username"
password = "your-password" 


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


def your_formatter(output):
    """
    Example formatter function.
    Adapt this to parse and format your command output.
    """
    rows = []
    for line in output.splitlines():
        rows.append([line.strip()])
    return tabulate(rows, headers=["Output"], tablefmt="grid")


def raw_formatter(output):
    return tabulate([[line] for line in output.splitlines()], headers=["Output"], tablefmt="grid")

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
