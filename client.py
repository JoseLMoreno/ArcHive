from pysc2.agents import base_agent
from pysc2.lib import actions

class LoginAgent(base_agent.BaseAgent):
    def step(self, obs):
        super(LoginAgent,self)
        with open("logfile.txt", 'a') as logfile:
            logfile.write(str(obs))

        return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])