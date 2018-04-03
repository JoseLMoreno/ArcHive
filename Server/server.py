# import sys
# sys.path.insert(0,'./pysc2-tutorial/Building a Sparse Reward Agent')
import socket, pickle, sys, time
import threading
import connection
from agents.sparse_agent import SparseAgent
from agents.smart_agent import SmartAgent

bind_ip = 'localhost'
bind_port = 2323


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))

server.listen(5)  # max backlog of connections

print ('Listening on {}:{}'.format(bind_ip, bind_port))

def handle_client_connection(client_socket):
    agent = None
    agentid = None
    readSize = int(client_socket.recv(sys.getsizeof(int)))
    chunk = client_socket.recv(readSize)
    while (sys.getsizeof(chunk) < readSize):
        chunk += client_socket.recv(readSize)
    chunk = chunk.decode()
    print(chunk)
    if chunk == "Sparse Agent":
        agent = SparseAgent()
        agentid = 1
    elif chunk == "QTable Agent":
        agent = SmartAgent()
        agentid = 2
    history = connection.GameHistory(chunk)
    
    history = pickle.dumps(history)
    # print(history)
    readSize = sys.getsizeof(history)
    client_socket.send(str(readSize).encode())
    time.sleep(0.01)
    client_socket.send(history)
    # print(threading.get_ident())

    while True:
        readSize = int(client_socket.recv(sys.getsizeof(int)))
        chunk = client_socket.recv(readSize)
        while (sys.getsizeof(chunk) < readSize):
            chunk += client_socket.recv(readSize)
        obs = pickle.loads(chunk)
        if obs.last():
            connection.PostGame(obs,agentid)
        action = agent.step(obs)
        action = pickle.dumps(action)
        readSize = sys.getsizeof(action)
        client_socket.send(str(sys.getsizeof(action)).encode())
        time.sleep(0.01)
        # print(readSize)
        client_socket.sendall(action)
        obs = None
        # step += 1
    # print(obs)

while True:
    client_socket, address = server.accept()
    print("connected to {}:{}".format(address[0],address[1]))
    client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
    client_handler.start()

