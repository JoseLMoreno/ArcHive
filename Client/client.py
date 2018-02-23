
"""
Currently basic agent prototype to check the observations given, and log them.
"""
import socket, pickle, sys
from pysc2.agents import base_agent
from pysc2.lib import actions

target = 'localhost'
port = 2323
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class ConnectAgent(base_agent.BaseAgent):
    def __init__(self):
        super(ConnectAgent,self).__init__()
        # self.agent = agent
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((target,port))
        self.id = self.connection.recv(8)
        print(self.id.decode())

    def step(self, obs):
        super(ConnectAgent,self)
        data = pickle.dumps(obs)
        self.connection.send(str(sys.getsizeof(data)).encode())
        # print(sys.getsizeof(data))        
        self.connection.sendall(data)
        # self.connection.send(b'')
        # with open("logfile.txt", 'a') as logfile:
        #     logfile.write(str(obs))
        readSize = int(self.connection.recv(sys.getsizeof(int)))
        action = pickle.loads(self.connection.recv(readSize))
        print(readSize,'\n',action)

        return action