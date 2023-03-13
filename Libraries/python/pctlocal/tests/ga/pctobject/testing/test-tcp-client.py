
from pyserver.network import *

class ClientSocketHandler(ITcpSocketCallback):
    def __init__(self):
        pass

    # called when connected to the server
    def on_newconnection(self, sock, err):
        print('Connected to the server')

    # called when disconnected from the server
    def on_disconnect(self, sock):
        print('Disconnected from the server')

    # called when new packet arrived
    def on_received(self, sock, data):
        print('Received : ' + str(data))
        # print('Received : ' + str(data.decode())) # Python3 
        #sock.send(data)

    # called when packet is sent
    def on_sent(self, sock, status, data):
        print('Sent with status code (' + str(status) + ')')
        
        
# hostname = 'localhost'
# port = 6666
# handler = ClientSocketHandler()
# no_delay = True # If True, Nagle's algorithm is not used, otherwise use Nagle's Algorithm
# tcp_client = AsyncTcpClient(hostname, port, handler, no_delay)        



# tcp_client.send('Hello'.encode())

# tcp_client.close()



# import socket
# import json



# class Client():
    
#     def __init__(self, host='localhost', port=6666 , buf_size=1024):
#         self.buf_size = buf_size
#         self.connection = socket.create_connection((host,port))

#     def get(self):
#         data = self.connection.recv(self.buf_size)
#         return data.decode()
    
#     def put(self, data):
#         d = str.encode(data)
#         self.connection.sendall(d)

#     def get_dict(self):
#         data = self.connection.recv(self.buf_size)
#         dict = eval(data.decode())
#         return dict
    
#     def put_dict(self, dict):
#         json_object = json.dumps(dict, indent = 4) 
#         d = str.encode(json_object)
#         self.connection.sendall(d)
        
#     def close(self):
#         self.connection.close()


# client = Client()
# # client.put('Hello')
# # recv = client.get()
# # print(recv)

# dict = {'val': 1.23}
# client.put_dict(dict)
# recv = client.get_dict()
# print(recv['val'])

# client.close()

from pct.environments import WebotsWrestler

wrestler = WebotsWrestler()
wrestler()
wrestler()
wrestler()
wrestler.done=True
wrestler()