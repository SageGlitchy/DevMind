import os
from github import Github
from dotenv import load_dotenv
from core.agent_base import agent
from core.intent import infer_intent

load_dotenv()

class Github_Agent(agent):
    def __init__(self):
        token=os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN not set in the environment variables")
        
        self.github= Github(token)
        self.last_intent=""
        
        
    def can_handle(self, query: str)->bool:
        intent=infer_intent(query)
        self.last_intent=intent
        print(f'[GithubAgent] Inferred intent:{intent}')
        return intent in ["github.pull_requests", 'github.issues']
        
        
        
    
    def handle(self, query, context: dict = {})-> str:
        repo_name="octocat/Hello-World"    #TODO: Dynamically extract repo name
        
        
        try:
            repo=self.github.get_repo(repo_name)
        except Exception as e:
            return f"Eroor accessing the repository {repo_name}: {str(e)}"
        
        if self.last_intent=="github.issues":
            issues=repo.get_issues(state= "open")
            issue_list= [f"- #{issue.number} {issue.title}" for issue in issues[:5]]
            
            return "Open issues: \n"+ "\n".join(issue_list) if issue_list else "No open issues found."
        
        if self.last_intent=="github.pull_requests":
            prs=repo.get_pulls(state="open")
            pr_list= [f" - #{pr.number} {pr.title}" for pr in prs[:5]]
            return "Open Pull Requests: \n"+ "\n".join(pr_list) if pr_list else "No open Pull Requests found."
        
        
        return "I can currently fetch only open issues or pull requests. Try asking that!!"