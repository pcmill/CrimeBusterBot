import socket
import ssl
import struct


domain = 'www.112misdaad.nl'

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_OPTIONAL  # CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = context.wrap_socket(
    s,
    server_hostname=domain,
)
ssl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#l_onoff, l_linger = 1, 1 # send RST (hard reset the socket) after 1 second
#ssl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
#                    struct.pack('ii', l_onoff, l_linger))
print(ssl_sock)
ssl_sock.connect((domain, 80))
print(ssl_sock)
ssl_sock.close()
