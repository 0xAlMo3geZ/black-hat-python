import sys
import socket
import threading

HEX_FILTER = "".join([(len(repr(chr(i))) == 3) and chr(i) or "." for i in range(256)])


def hexdump(src, length=16, show=True):
    """
    Returns a hex dump of a given input source string or byte sequence.
    If `src` is a bytes object, it is first decoded to a string.
    The output is formatted in rows of `length` bytes, each row showing the
    byte offset in hexadecimal, the hexadecimal representation of `length`
    bytes, and the ASCII representation of those bytes, substituting non-printable
    characters with a period '.'.
    If `show` is True, the output is printed to the console, otherwise it is
    returned as a list of strings.

    :param src: A string or bytes object to be hex dumped.
    :type src: str or bytes

    :param length: The number of bytes to be shown in each row.
    :type length: int

    :param show: Whether to print the output to console or return it as a list of strings.
    :type show: bool

    :return: If `show` is False, a list of strings containing the hex dump output.
            Otherwise, None.
    :rtype: list or None
    """
    if isinstance(src, bytes):
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i : i + length])
        printable = word.translate(HEX_FILTER)
        hexa = " ".join([f"{ord(c):02X}" for c in word])
        hexwidth = length * 3
        results.append(f"{i:04x}  {hexa:<{hexwidth}} {printable}")
    if show:
        for line in results:
            print(line)
        else:
            return results


def receive_from(connection):
    """
    Receives data from a connection and returns a buffer of the received data.

    :param connection: A connection object.
    :type connection: socket object
    :return: A buffer of the received data.
    :rtype: bytes
    """
    buffer = b""

    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception:
        pass
    return buffer


def request_handler(buffer):
    """
    Takes in a buffer and performs packet modifications on it. Returns the modified buffer.
    """
    # perform packet modifications
    return buffer


def response_handler(buffer):
    """
    Handles the response by performing packet modifications.

    :param buffer: A packet of data to be handled.
    :type buffer: Any
    :return: The modified packet of data.
    :rtype: Any
    """
    # perform packet modifications
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """
    Creates a proxy handler that receives data from a client socket and sends it to a remote host
    and vice versa. The function takes in four parameters:

    - client_socket: A socket object representing the client socket.
    - remote_host: A string representing the remote host to connect to.
    - remote_port: An integer representing the remote port to connect to.
    - receive_first: A boolean indicating whether to receive data from the remote host first.

    Returns: None
    """
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))

        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>]Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)

            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    """
    Creates a server socket and listens to incoming connections from a local host and port.
    It binds to the local host and port specified and creates a server socket with the provided
    address family and socket type. If it fails to bind, it prints the error message and exits.
    If successful, it listens for incoming connections and prints out the local connection information.
    Once a connection is accepted, it starts a new thread to handle the communication between client
    and remote host.

    Args:
        local_host (str): The IP address or hostname of the local machine.
        local_port (int): The port number on the local machine to listen to.
        remote_host (str): The IP address or hostname of the remote machine.
        remote_port (int): The port number on the remote machine to connect to.
        receive_first (bool): If True, receives data from the remote host before sending any data.

    Returns:
        None
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("problem on bind: %r" % e)
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first),
        )
        proxy_thread.start()


def main():
    """
    Runs the main function of the program which routes traffic between a local and remote socket.
    :return: None
    """
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end="")
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()
