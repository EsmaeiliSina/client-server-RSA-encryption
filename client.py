import socket
import sys
import rsa
import re
from lazyme.string import color_print


publicKey, privateKey = rsa.newkeys(512)

server_publikkey = []

with open('public_client.txt', 'w') as file:
    file.write(str(publicKey))
with open('private_client.txt', 'w') as file:
    file.write(str(privateKey))

host = socket.gethostname()
port = 12345
conn = socket.socket()

color_print('-----TRANSFER PUBLICKEYS-----', color='green')

conn.connect((host, port))
data = str(conn.recv(2048))
server_publikkey = re.findall(r'\b\d+\b', data)
server_publikkey = rsa.PublicKey(
    int(server_publikkey[0]), int(server_publikkey[1]))
color_print('Server PublicKey : ' + str(server_publikkey), color='red')
conn.sendall(bytes(str(publicKey), 'utf-8'))

# conn.sendall(b'Connected. Wait for data...')

while True:

    intosend = input("message to send (q for exit): ").encode('utf-8')
    if intosend.decode('utf-8') == 'q':
        sys.exit()
    intosend = rsa.encrypt(intosend, server_publikkey)
    conn.sendall(intosend)
    # data received back from sever
    data = conn.recv(1024)
    color_print("Server : " + data.decode('utf-8'), color="green")
