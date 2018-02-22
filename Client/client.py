
"""
Currently basic agent prototype to check the observations given, and log them.
"""
from pysc2.agents import base_agent
from pysc2.lib import actions

class ConnectAgent(base_agent.BaseAgent):
    def __init__(self, agent):
        super(ConnectAgent,self).__init__()
        self.agent = agent
        self.connection = None

    def step(self, obs):
        super(ConnectAgent,self)
        with open("logfile.txt", 'a') as logfile:
            logfile.write(str(obs))

        return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])