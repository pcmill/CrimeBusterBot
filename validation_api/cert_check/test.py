import nmap
import socket
import ssl


domain = 'www.112misdaad.nl'
#domain = '165.231.102.206'
#domain = 'www.adidaisclimacool.nl'

nm = nmap.PortScanner()
nm.scan(domain)
#print(nm.scaninfo())
print(nm.all_hosts())
print(nm['165.231.102.206'].hostnames())
print(nm['165.231.102.206'].state())
print(nm['165.231.102.206'].tcp(80))

#context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#context.verify_mode = ssl.CERT_REQUIRED
#context.check_hostname = True
#context.load_default_certs()
#print(context)
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print(s)
#ssl_sock = context.wrap_socket(s, server_hostname=domain)
#print(ssl_sock.connect((domain, 443)))
