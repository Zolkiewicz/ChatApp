import socket
import threading

def receive(client):
    try:
        with client.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                print(line, end="", flush=True)
    except (OSError, UnicodeError):
        pass
    finally:
        print("\nConnection with server has been lost")


def main():
    host = input("Input server IP [default: 127.0.0.1]: ").strip() or '127.0.0.1'
    
    port_input = input("Input server port [default: 8000]: ").strip()
    port = int(port_input) if port_input else 8000

    while True:
        name = input("Input nick: ").strip()
        if name and "\n" not in name and "\r" not in name:
            break
        print("Invalid nick. Try again.")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((host, port))
        client.sendall((name + "\n").encode("utf-8"))

        threading.Thread(
            target=receive,
            args=(client,),
            daemon=True,
        ).start()

        while True:
            message = input()
            client.sendall((message + "\n").encode("utf-8"))

    except (ConnectionRefusedError, socket.gaierror, OSError) as e:
        print(f"Couldn't connect with server: {e}")
    finally:
        client.close()
        print("Disconnect")


if __name__ == "__main__":
    main()
