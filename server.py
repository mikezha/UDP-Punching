import socket
PORT = 8000
HOST = "8.8.8.8"
BUFFER_SIZE = 1024

if __name__ == '__main__':
    # create the UDP socket
    host = socket.gethostbyname(socket.gethostname())
    addr = (host, PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(addr)

    print "Server is waiting for clients on %s:%s\n" % (host, PORT)
    # pair off clients
    clients = []
    while 1:
        # wait for a UDP message for a client
        message, client_addr = server_socket.recvfrom(BUFFER_SIZE)
        print "connection from %s:%d" % client_addr

        clients.append(client_addr)

        # if we have a pair of clients connected, inform each of the other's
        # ip and port. Then our job is done
        if len(clients) == 2:
            a, b = clients
            server_socket.sendto(str(b[0]) + ":" + str(b[1]), a)
            server_socket.sendto(str(a[0]) + ":" + str(a[1]), b)
            print "linked a pair"
            clients = []


