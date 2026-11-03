import socket

HOST = '127.0.0.1'
PORT = 8000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    name = input("input nick: ").strip()
    if name:
        client.sendall((name + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
