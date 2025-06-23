import os
from github import Github
from dotenv import load_dotenv
from core.agent_base import agent
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()


class Github_Agent(agent):
    def __init__(self):
        token=os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN not set in the environment variables")
        
        self.github= Github(token)
        
        self.model= SentenceTransformer('all-mpnet-base-v2')
        self.examples= [
            "get open issues from a repo",
            "list open pull requests",
            "fetch commits from github",
            "show me Github PRs",
            "display repository issues",
            "retrieve pull requests",
            "how many PRs are there",
            "check repository status",
            "any issues still open",
            "get repo activity"
        ]
        
        self.example_embeddings= self.model.encode(self.examples, convert_to_tensor=True)
    
    def can_handle(self, query: str)->bool:
        query_embedding= self.model.encode(query, convert_to_tensor=True)
        similarity_scores=cosine_similarity(
            query_embedding.cpu().numpy().reshape(1,-1),
            self.example_embeddings.cpu().numpy())[0]
        max_score= max(similarity_scores)
        
        print(f"[GithubAgent] Similarity score: {max_score: .3f} for query: {query}" )
        
        return max_score>0.55
        
        
        
    
    def handle(self, query, context: dict = {})-> str:
        repo_name="octocat/Hello-World"    #TODO: Dynamically extract repo name
        
        
        try:
            repo=self.github.get_repo(repo_name)
        except Exception as e:
            return f"Eroor accessing the repository {repo_name}: {str(e)}"
        
        query=query.lower()
        
        if "issue" in query:
            issues=repo.get_issues(state= "open")
            issue_list= [f"- #{issue.number} {issue.title}" for issue in issues[:5]]
            
            return "Open issues: \n"+ "\n".join(issue_list) if issue_list else "No open issues found."
        
        if "pr" in query or "pull request" in query:
            prs=repo.get_pulls(state="open")
            pr_list= [f" - #{pr.number} {pr.title}" for pr in prs[:5]]
            return "Open Pull Requests: \n"+ "\n".join(pr_list) if pr_list else "No open Pull Requests found."
        
        
        return "I can currently fetch only open issues or pull requests. Try asking that!!"