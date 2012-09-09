import socket
import sys
from select import select
from server import PORT, HOST, BUFFER_SIZE

if __name__ == '__main__':
    server_addr = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # tell the server you want to connect. This gives the server your public IP
    # and port
    print "Asking server to connect..."
    client_socket.sendto("connect me please", server_addr)
    print "Waiting for a response..."

    # now wait for server to send back the public IP and port of the peer
    message, addr = client_socket.recvfrom(BUFFER_SIZE)
    host, port = message.split(":")
    peer_addr = (host, int(port))

    print "You'll be chatting with %s:%d" % peer_addr

    # Fake sending a message to the peer so your router's NAT knows to send
    # responses back to this host. This message only has to reach your router.
    # So set the TTL to something low (like 2)
    old_ttl = client_socket.getsockopt(socket.SOL_IP, socket.IP_TTL)
    ttl_to_reach_router = 2
    client_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl_to_reach_router)
    client_socket.sendto("This will only reach your router before being discarded", peer_addr)
    # set the TTL to what it was before
    client_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, old_ttl)

    print "Start chatting"

    # wait for something from the socket or stdin. Either:
    # print out what comes from the socket (i.e. what the peer sends)
    # or send whatever you type to the peer
    while True:
        r, w, x = select([sys.stdin, client_socket], [], [])
        if sys.stdin in r:
            data = sys.stdin.readline() 
            client_socket.sendto(data, peer_addr)
        elif client_socket in r:
            data, addr = client_socket.recvfrom(BUFFER_SIZE)
            sys.stdout.write(data)

