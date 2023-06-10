import socket
import threading

IP = "0.0.0.0"
PORT = 9999


def main():
    """
    Creates a socket server, binds it to the IP address and port provided,
    listens for incoming connections, and handles each connection in a separate
    thread. No parameters are taken. No return types.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((IP, PORT))

    server.listen(5)

    print(f"[*] listening on {IP}:{PORT}")

    while True:
        client, addr = server.accept()

        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")

        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    """
    Handle a client connection by receiving a message from a socket and sending an acknowledgement message.

    :param client_socket: A socket object representing the client connection.
    :type client_socket: socket.socket
    :return: None
    """
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b"ACK!")


if __name__ == "__main__":
    main()
