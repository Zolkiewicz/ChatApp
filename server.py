import socket
import threading

HOST = '0.0.0.0'
PORT = 8000

clients = []
clients_lock = threading.Lock()

def broadcast(message):
    data = (message + "\n").encode("utf-8")

    with clients_lock:
        current_clients = list(clients)

    for client in current_clients:
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
            print(f"Unable to get client's name. client's address: {addr}")
            client.close()
            return

        print(f"{name} joined.")
        broadcast(f"{name} joined.")

        with clients_lock:
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
            with clients_lock:
                clients.remove(client)
            broadcast(f"{name} left the chat.")
        client.close()
        print(f"{name} {addr} left the chat.")
        

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started successfully on {HOST}:{PORT}")

    try:
        while True:
            client, addr = server.accept()
            threading.Thread(
                target=handle,
                args=(client, addr),
                daemon=True,
            ).start()
    except KeyboardInterrupt:
        print("\nServer shutdown")
    finally:
        with clients_lock:
            for client in clients:
                try:
                    client.close()
                except OSError:
                    print(f"Unable to close client {client}.")
                    pass
        server.close()

if __name__ == "__main__":
    main()
