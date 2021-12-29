import socket
import threading
import sys
import rsa
import re
from lazyme.string import color_print

publicKey, privateKey = rsa.newkeys(512)

client_publicKey = []

with open('public_server.txt', 'w') as file:
    file.write(str(publicKey))
with open('private_server.txt', 'w') as file:
    file.write(str(privateKey))

# encMessage = rsa.encrypt(message.encode(), publicKey)
# decMessage = rsa.decrypt(encMessage, privateKey).decode()

s = socket.socket()
host = socket.gethostname()
port = 12345
s = socket.socket()
s.bind((host, port))
s.listen(1)


def processMessages(conn, addr):
    while True:
        try:
            data = conn.recv(2048)
            color_print('Encrypted Client Message : ', color='green')
            color_print(str(data), color='yellow')
            data = rsa.decrypt(data, privateKey)
            if data.decode("utf-8") == 'exit':
                conn.close()
            color_print('Decrypted Client Message : ', color='green')
            color_print(data.decode("utf-8"), color='yellow')
            conn.sendall(bytes('ACK', 'utf-8'))
        except:
            conn.close()
            color_print("Connection closed by" + str(addr), color='red')
            # Quit the thread.
            sys.exit()


while True:

    # Wait for connections
    conn, addr = s.accept()
    ss = 'Got connection from ' + str(addr[0]) + '(' + str(addr[1]) + ')'
    color_print(ss, color='green')
    color_print('-----TRANSFER PUBLICKEYS-----', color='green')
    conn.sendall(bytes(str(publicKey), 'utf-8'))
    data = str(conn.recv(2048))
    client_publicKey = re.findall(r'\b\d+\b', data)
    client_publicKey = rsa.PublicKey(
        int(client_publicKey[0]), int(client_publicKey[1]))

    color_print('Client PublicKey : ' + str(client_publicKey), color='red')
    # Listen for messages on this connection
    listener = threading.Thread(target=processMessages, args=(conn, addr))
    listener.start()
