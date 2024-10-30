import os
import sys
import subprocess

from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM

def start_daemon() -> None:
    current_path = os.path.dirname(os.path.abspath(__file__))
    daemon_path = os.path.join(current_path, "daemon.py")

    subprocess.Popen([
            sys.executable, daemon_path
        ],
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def stop_daemon() -> None:
    if not daemon_is_running():
        return

    client = Socket(AF_INET, SOCK_STREAM)
    client.connect(("127.0.0.1", 8669))

    client.send(b"stop")
    ack = client.recv(3)
    client.close()

def daemon_is_running() -> bool:
    lock_file = os.path.expanduser("~/.daemon.lock")
    if not os.path.isfile(lock_file):
        return False

    with open(lock_file, "r") as file:
        try:
            pid = int(file.read())
            os.kill(pid, 0)
            return True
        except (ValueError, ProcessLookupError):
            return False

def get_daemon_status() -> int | None:
    if not daemon_is_running():
        return

    client = Socket(AF_INET, SOCK_STREAM)
    client.connect(("127.0.0.1", 8669))

    client.send(b"status")
    status = client.recv(4)
    client.send(b"ACK")
    client.close()
    return int.from_bytes(status, "big")
