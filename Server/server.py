# import sys
# sys.path.insert(0,'./pysc2-tutorial/Building a Sparse Reward Agent')
import socket, pickle, sys, time
import threading
from agents.sparse_agent import SparseAgent

bind_ip = 'localhost'
bind_port = 2323
agent = SparseAgent()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))

server.listen(5)  # max backlog of connections

print ('Listening on {}:{}'.format(bind_ip, bind_port))

def handle_client_connection(client_socket):
    client_socket.send(str(threading.get_ident()).encode())
    print(threading.get_ident())
    # chunk = client_socket.recv(4096)
    # obs = chunk
    # print(chunk)
    # while True:
    while True:
        readSize = int(client_socket.recv(sys.getsizeof(int)))
        # print(readSize)
        chunk = client_socket.recv(readSize)
        while (sys.getsizeof(chunk) < readSize):
            chunk += client_socket.recv(readSize)
        obs = pickle.loads(chunk)
        # print('sending')
        action = agent.step(obs)
        # print(action)
        action = pickle.dumps(action)
        readSize = sys.getsizeof(action)
        client_socket.send(str(sys.getsizeof(action)).encode())
        time.sleep(0.01)
        # print(readSize)
        client_socket.sendall(action)
        obs = None
    # print(obs)

while True:
    client_socket, address = server.accept()
    print("connected to {}:{}".format(address[0],address[1]))
    client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
    client_handler.start()

