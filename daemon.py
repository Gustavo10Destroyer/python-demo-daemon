import os
from time import time
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR

from daemon_utils import daemon_is_running

def main() -> None:
    if daemon_is_running():
        print("[ERR!] Outra instância do daemon já está em execução!")
        return

    lock_file = os.path.expanduser("~/.daemon.lock")
    with open(lock_file, "w") as file:
        file.write(str(os.getpid()))
        file.flush()

        server = Socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 8669))
        server.listen(1)

        boot_time = round(time() * 1000)

        while True:
            client, address = server.accept()
            client.settimeout(6)

            try:
                message = client.recv(1024)
                if len(message) == 0:
                    client.close()
                    continue
            except (OSError, TimeoutError):
                client.close()
                continue

            if message == b"status":
                client.send((round(time() * 1000) - boot_time).to_bytes(4, "big"))
                ack = client.recv(3)
                client.close()
            elif message == b"stop":
                client.send(b"ACK")
                client.close()
                server.close()
                break

if __name__ == "__main__":
    main()
