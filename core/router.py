from typing import List
from core.agent_base import agent

class Router:
    def __init__(self, agents: List[agent]):
        self.agents=agents
    
    
    def route(self, query:str, context: dict= {})->str:
        for agent in self.agents:
            if agent.can_handle(query):
                return agent.handle(query, context)
        
        return "Sorry, I couldn't find an agent to solve that query."