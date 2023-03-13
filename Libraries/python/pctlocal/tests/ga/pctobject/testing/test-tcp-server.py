

# import socket
# import json

# class Server():
#     def __init__(self, host='localhost', port=6666 , buf_size=1024):
#         self.buf_size = buf_size
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.bind((host, port))
#             s.listen()
#             print(f"Waiting for connection on {host}:{port}")
#             self.connection, addr = s.accept()
#             print(f"Connected by {addr}")
            
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

from  pct.network import Server

server = Server()
# rec = server.get()
# print(rec)
# server.put('Goodbye')

while server.isOpen():
    rec = server.get_dict()
    print(rec)
    if rec['msg'] == 'close':
        server.finish()
    else:
        dict = {'msg': 'values', 'leg': 0.1}
        server.put_dict(dict)

server.close()





