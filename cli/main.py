from core.router import Router
from agents.dummy_agent import dummy_agent
from agents.github_agent import Github_Agent

def load_agents():
    return [
        dummy_agent(),
        Github_Agent()
    ]

def main():
    agents=load_agents()
    router = Router(agents)
    
    print("Welcome to DevMind (type exit or quit to leave) \n" )
    
    while True:
        query=input("You: ").strip()
        if query.lower() in ("exit", "quit"):
            print ("DevMind: GoodBye👋")
            break
        
        response = router.route(query)
        print(f'DevMind: {response} \n')
        

if __name__== "__main__":
    main()
        