import socket

HOST = '0.0.0.0'
PORT = 8000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server started successfully.")

    while True:
        client, addr = server.accept()
        print(f"New connection from {addr}.")

        try:
            reader = client.makefile("r", encoding="utf-8")
            name = reader.readline().strip()
            if not name:
                client.close()
                continue

            print(f"{name} joined.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    main()
