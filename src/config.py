from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

VECTOR_DB_PATH = "vector_store"

# Document type mappings
DOCUMENT_TYPES = {
    "project_overview": {
        "description": "Project guidelines, expectations and logistics",
        "files": ["project_overview.txt", "project_proposal_guideline.txt", 
                 "presentation_guideline.txt", "final_project_report_guideline.txt"]
    },
    "project": {
        "description": "Project reference papers and our project title",
        "files": [
            "title.txt", 
            "ref_A Finite Time Analysis of Temporal Difference Learning With Linear Function Approximation_latex.txt",
            "ref_Learning the Target Network in Function Space.txt",
            "ref_Proximal Gradient Temporal Difference Learning: Stable Reinforcement Learning with Polynomial Sample Complexity.txt",
            "ref_TD Convergence: An Optimization Perspective.txt"
        ]
    },
    "a1": {
        "description": "Assignment 1 materials",
        "files": ["answer.html", "cmpt_409_981_a1.py", "feedback.txt", "submission_latex.txt"]
    },
    "a2": {
        "description": "Assignment 2 materials", 
        "files": ["answer.html", "q3_q4_a2.py", "feedback.txt", "submission_latex.txt"]
    }
}