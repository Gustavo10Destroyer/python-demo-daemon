import sys
from daemon_utils import start_daemon, stop_daemon, daemon_is_running, get_daemon_status

def main() -> None:
    state = "em execução" if daemon_is_running() else "parado"
    print(f"[INFO] Estado do daemon: {state}")

    if daemon_is_running():
        print(f"[INFO] O daemon está rodando há: {get_daemon_status()}ms.")

    if len(sys.argv) == 1:
        return

    if sys.argv[1] == "start":
        if daemon_is_running():
            print("[ERR!] O daemon já está em execução!")
            return

        start_daemon()
        print("[INFO] O daemon foi iniciado!")
    elif sys.argv[1] == "stop":
        if not daemon_is_running():
            print("[ERR!] O daemon não está em execução!")
            return

        stop_daemon()
        print("[INFO] O daemon foi parado!")

if __name__ == "__main__":
    main()
