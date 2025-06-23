from core.agent_base import agent


class dummy_agent(agent):
    def can_handle(self, query:str)->bool:
        keywords=['hi', 'hey', 'hello']
        return any(word in query.lower() for word in keywords)
    
    def handle(self, query, context = {})->str:
        return "Hello! I'm DevMind. How may I assist you today?"