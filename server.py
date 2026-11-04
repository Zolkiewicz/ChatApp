import socket

HOST = '127.0.0.1'
PORT = 8000

clients = []

def broadcast(message):
    data = (message + "\n").encode("utf-8")

    for client in clients:
        try:
            client.sendall(data)
        except OSError as e:
            print(f"Error sending message from {client}: {e}")
            pass


def handle(client, addr):
    try:
        reader = client.makefile("r", encoding="utf-8")
        name = reader.readline().strip()
        if not name:
            name = "Unknown"
            client.close()
            return

        print(f"{name} joined.")
        broadcast(f"{name} joined.")

        clients.append(client)
        for line in reader:
            message = line.rstrip("\r\n")
            if message:
                print(f"{name} {addr}: {message}")
                broadcast(f"{name}: {message}")

    except Exception as e:
        print(f"Error adding client: {e}")
    finally:
        if client in clients:
            clients.remove(client)
            broadcast(f"{name} left the chat.")
        client.close()
        print(f"{name} {addr} left the chat.")
        

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started successfully on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"New connection from {addr}.")
        handle(client, addr)



if __name__ == "__main__":
    main()
