#!/usr/bin/env python3
"""Multi-bot Telegram gateway manager.

Usage:
  python3 manage_bots.py status     # show all bot gateway status
  python3 manage_bots.py start cmo  # start one bot
  python3 manage_bots.py start all  # start cmo + manager + employee + cto
  python3 manage_bots.py stop cmo   # stop one bot
  python3 manage_bots.py stop all   # stop all role bots (CEO untouched)
  python3 manage_bots.py restart cmo
  python3 manage_bots.py test cmo   # send a test message via the bot
"""
import os
import signal
import subprocess
import sys
import time
import json
from pathlib import Path

HERMES_AGENT = Path.home() / ".hermes" / "hermes-agent"
VENV_PYTHON = HERMES_AGENT / "venv" / "bin" / "python"
GATEWAY_MAIN = HERMES_AGENT / "hermes_cli" / "main.py"

BOT_HOMES = Path.home() / ".hermes" / "ops" / "bot_homes"

ROLE_TO_TOKEN_ENV = {
    "cmo": "HERMES_CMO_TELEGRAM_TOKEN",
    "manager": "HERMES_MANAGER_TELEGRAM_TOKEN",
    "employee": "HERMES_EMPLOYEE_TELEGRAM_TOKEN",
    "cto": "HERMES_CTO_TELEGRAM_TOKEN",
}

ALL_ROLES = ["cmo", "manager", "employee", "cto"]


def bot_home(role):
    return BOT_HOMES / role


def bot_pid_file(role):
    return bot_home(role) / "gateway.pid"


def bot_log(role):
    return bot_home(role) / "logs" / "gateway.log"


def is_running(role):
    pid_file = bot_pid_file(role)
    if not pid_file.exists():
        return False
    try:
        pid = int(pid_file.read_text().strip())
    except Exception:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def get_pid(role):
    pid_file = bot_pid_file(role)
    if not pid_file.exists():
        return None
    try:
        return int(pid_file.read_text().strip())
    except Exception:
        return None


def resolve_token(role):
    env_name = ROLE_TO_TOKEN_ENV.get(role)
    if not env_name:
        return None
    return os.environ.get(env_name)


def launch_bot(role, quiet=True):
    home = bot_home(role)
    home.mkdir(parents=True, exist_ok=True)
    (home / "logs").mkdir(exist_ok=True)
    (home / "sessions").mkdir(exist_ok=True)
    (home / "state").mkdir(exist_ok=True)

    token = resolve_token(role)
    if not token:
        print(f"ERROR: {ROLE_TO_TOKEN_ENV[role]} is not set")
        return None

    log_file = bot_log(role)
    env = os.environ.copy()
    env["HERMES_HOME"] = str(home)
    env["TELEGRAM_BOT_TOKEN"] = token
    env["_HERMES_GATEWAY"] = "1"
    env["HERMES_QUIET"] = "1" if quiet else "0"

    cmd = [
        str(VENV_PYTHON),
        str(GATEWAY_MAIN),
        "gateway",
        "run",
        "--external-supervisor",
    ]

    with open(log_file, "ab") as log_f:
        proc = subprocess.Popen(
            cmd,
            env=env,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    time.sleep(8)

    if proc.poll() is not None:
        print(f"ERROR: {role} gateway exited with code {proc.returncode}")
        print("Last 20 log lines:")
        try:
            lines = log_file.read_text(errors="replace").strip().splitlines()
            for line in lines[-20:]:
                print(f"  {line}")
        except Exception:
            pass
        return None

    pid = proc.pid
    pid_file = bot_pid_file(role)
    pid_file.write_text(str(pid))
    print(f"OK: {role} bot gateway running (pid={pid})")
    return pid


def stop_bot(role):
    pid = get_pid(role)
    if pid is None:
        print(f"{role}: no pid file")
        return
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"{role}: sent SIGTERM to pid {pid}")
    except ProcessLookupError:
        print(f"{role}: process {pid} already gone")
    except Exception as e:
        print(f"{role}: error killing {pid}: {e}")

    for _ in range(10):
        time.sleep(1)
        try:
            os.kill(pid, 0)
            continue
        except OSError:
            break

    try:
        os.kill(pid, 0)
        print(f"{role}: still alive after 10s, forcing...")
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    except OSError:
        pass

    pid_file = bot_pid_file(role)
    if pid_file.exists():
        pid_file.unlink()
    print(f"{role}: stopped")


def show_status():
    print(f"{'role':<10} {'pid':<8} {'running':<10} {'token':<25} {'home':<50}")
    print("-" * 110)
    for role in ALL_ROLES:
        token = resolve_token(role)
        token_info = f"{token[:20]}..." if token else "NOT SET"
        home = bot_home(role)
        pid = get_pid(role)
        running = is_running(role)
        print(f"{role:<10} {str(pid) if pid else 'N/A':<8} "
              f"{'YES' if running else 'no':<10} "
              f"{token_info:<25} "
              f"{str(home):<50}")

    print("-" * 110)
    print("NOTE: CEO bot runs as the main Hermes gateway (pid from gateway_state.json)")
    try:
        state = Path.home() / ".hermes" / "gateway_state.json"
        if state.exists():
            data = json.loads(state.read_text())
            print(f"  CEO gateway pid={data.get('pid')} state={data.get('gateway_state')}")
    except Exception:
        pass


def send_test_message(role):
    token = resolve_token(role)
    if not token:
        print(f"ERROR: no token for {role}")
        return
    chat_id = "5191016577"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    import urllib.request
    payload = json.dumps({"chat_id": chat_id, "text": f"✅ {role.upper()} bot is LIVE — role-based access active."}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                msg = result["result"]
                print(f"{role}: message sent — from={msg.get('from',{}).get('username')} "
                      f"update_id={msg.get('update_id')}")
            else:
                print(f"{role}: send failed: {result.get('description')}")
    except Exception as e:
        print(f"{role}: API error: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 manage_bots.py <command> [role|all]")
        print("Commands: status, start, stop, restart, test")
        sys.exit(1)

    cmd = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "all"

    if cmd == "status":
        show_status()
    elif cmd == "start":
        roles = ALL_ROLES if target == "all" else [target]
        for role in roles:
            if is_running(role):
                print(f"{role}: already running (pid={get_pid(role)})")
                continue
            print(f"Starting {role}...")
            launch_bot(role)
    elif cmd == "stop":
        roles = ALL_ROLES if target == "all" else [target]
        for role in roles:
            stop_bot(role)
    elif cmd == "restart":
        roles = ALL_ROLES if target == "all" else [target]
        for role in roles:
            print(f"Restarting {role}...")
            stop_bot(role)
            time.sleep(2)
            launch_bot(role)
    elif cmd == "test":
        roles = ALL_ROLES if target == "all" else [target]
        for role in roles:
            print(f"Sending test message via {role}...")
            send_test_message(role)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
