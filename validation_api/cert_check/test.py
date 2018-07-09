import socket
import ssl


domain = 'www.112misdaad.nl'

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()
print(context)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)
ssl_sock = context.wrap_socket(s, server_hostname=domain)
print(ssl_sock.connect((domain, 443)))

