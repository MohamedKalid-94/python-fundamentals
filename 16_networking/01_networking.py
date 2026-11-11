import ipaddress
import socket
import struct
import sys

# NETWORKING lets programs on different computers (or on the same one) exchange data.
#
# THE LAYERS (TCP/IP model)
#   Application   HTTP, HTTPS, DNS, MQTT, Modbus-TCP, SSH     what the programs say
#   Transport     TCP, UDP                                    ports, reliability
#   Internet      IP (IPv4, IPv6)                             addresses, routing
#   Link          Ethernet, Wi-Fi, CAN, UART                  one hop on a wire or radio
#
# ADDRESS = which computer (IP).  PORT = which program on it (0..65535).
#   0-1023 well known (80 http, 443 https, 22 ssh, 53 dns)
#   1024-49151 registered (1883 mqtt, 502 modbus, 5432 postgres)
#   49152-65535 ephemeral (the client side of a connection)
#
#              TCP                               UDP
#   connection yes (handshake)                   no
#   delivery   reliable, ordered, no duplicates  may be lost, reordered or duplicated
#   data       a continuous BYTE STREAM          separate DATAGRAMS (message boundaries kept)
#   speed      more overhead                     light and fast
#   use for    web, files, databases, commands   sensor streams, discovery, DNS, video

# 1. localhost and DNS (the name -> address lookup)
print(socket.gethostbyname("localhost"))        # 127.0.0.1
info = socket.getaddrinfo("localhost", 80, family=socket.AF_INET, type=socket.SOCK_STREAM)
print(info[0][4])                               # ('127.0.0.1', 80)
print(isinstance(socket.gethostname(), str))    # True

# 2. The ipaddress module: work with addresses and networks (no network access needed)
ip = ipaddress.ip_address("192.168.1.10")
print(ip, ip.version, ip.is_private, ip.is_loopback)    # 192.168.1.10 4 True False
print(ipaddress.ip_address("127.0.0.1").is_loopback)    # True
print(ipaddress.ip_address("8.8.8.8").is_global)        # True
v6 = ipaddress.ip_address("::1")
print(v6.is_loopback, v6.version)                       # True 6

net = ipaddress.ip_network("192.168.1.0/24")
print(net.netmask, net.broadcast_address, net.num_addresses)    # 255.255.255.0 192.168.1.255 256
print(ip in net, ipaddress.ip_address("10.0.0.1") in net)       # True False
print(list(ipaddress.ip_network("192.168.1.0/30").hosts()))
# [IPv4Address('192.168.1.1'), IPv4Address('192.168.1.2')]
print([str(n) for n in net.subnets(new_prefix=26)])
# ['192.168.1.0/26', '192.168.1.64/26', '192.168.1.128/26', '192.168.1.192/26']
print(int(ip), ipaddress.ip_address(3232235786))        # 3232235786 192.168.1.10

# 3. An IPv4 address is just 4 bytes
print(socket.inet_aton("192.168.1.10"))                 # b'\xc0\xa8\x01\n'
print(socket.inet_ntoa(b"\xc0\xa8\x01\n"))              # 192.168.1.10

# 4. BYTE ORDER: the network uses BIG-endian ("network byte order")
print(struct.pack(">H", 0x1234).hex(), struct.pack("<H", 0x1234).hex())    # 1234 3412
print(socket.htons(socket.ntohs(0x1234)) == 0x1234)     # True    (htons/ntohs exist, as in C)

# 5. struct: pack and unpack binary protocol fields, like a C struct
#    > big-endian   B 1 byte unsigned   H 2 bytes unsigned   I 4 bytes unsigned   h/i signed
header = struct.pack(">BBH", 1, 2, 500)
print(header.hex(), struct.unpack(">BBH", header), struct.calcsize(">BBH"))
# 010201f4 (1, 2, 500) 4

# 6. The constants you pass to socket()
print(socket.IPPROTO_TCP, socket.IPPROTO_UDP)           # 6 17
print(socket.AF_INET.name, socket.SOCK_STREAM.name, socket.SOCK_DGRAM.name)
# AF_INET SOCK_STREAM SOCK_DGRAM
#   AF_INET = IPv4, AF_INET6 = IPv6, SOCK_STREAM = TCP, SOCK_DGRAM = UDP

# CLIENT-SERVER MODEL
#   server   waits for connections on a known address and port
#   client   starts the conversation; the OS gives it a temporary (ephemeral) port
#   Many protocols use REQUEST -> RESPONSE (HTTP). Others stream (MQTT, UART-like data).