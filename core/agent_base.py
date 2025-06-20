from abc import ABC, abstractmethod
from typing import Dict

class agent(ABC):
    
    # Base interface for all agents
    # All agents must implement can_handle and handle methods.
    
    @abstractmethod
    def can_handle(self, query:str)->bool:
        
        # Decide whether the agent can respond to given query
        
        pass
    
    @abstractmethod
    def handle(self, query:str, context: Dict = {})->str:
        # Return a response to the query
        
        pass
    