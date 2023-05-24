# Black Hat Python 2nd Edition

<img align="center" src="https://i.ebayimg.com/images/g/2IEAAOSwHFFjroow/s-l500.jpg" />

## Resources:

- https://www.amazon.com/Black-Hat-Python-Programming-Pentesters/dp/1593275900

## Exercises:

1.  [**TCP Client**](./tcp_client.py):

        how to build:
          1 - We first create a socket object with the AF_INET and SOCK_STREAM parameters
          2 - The AF_INET parameter is saying we are going to use a standard IPv4 address or hostname, and SOCK_STREAM indicates that this will be a TCP client. We then connect the client to the server
          3 - and send it some data
          4 - The last step is to receive some data back and print out the response

2.  [**UDP Client**](./udp_client.py):

        how to build:
          1 - As you can see, we change the socket type to SOCK_DGRAM
          2 - when creating the socket object. The next step is to simply call sendto()
          3 - passing in the data and the server you want to send the data to. Because UDP is a connectionless protocol, there is no call to connect() beforehand. The last step is to call recvfrom() to receive UDP data back.

3.  [**TCP Server**](./tcp_server.py):

        how to build:
          1 - To start off, we pass in the IP address and port we want the server to listen on
          2 - Next we tell the server to start listening
          3 - and our main server loop is ready to handle another incoming connection. The handle_client function performs the recv() and then sends a simple message back to the client.
          4 - with a maximum backlog of connections set to 5. We then put the server into its main loop, where it is waiting for an incoming connection. When a client connects
          5 - we receive the client socket into the client variable, and the remote connection details into the addr variable. We then create a new thread object that points to our handle_client function, and we pass it the client socket object as an argument. We then start the thread to handle the client connection

4.  [**Netcat Replacement**](./netcat.py):

        how to build:
          - the book, page 32 to page 40
