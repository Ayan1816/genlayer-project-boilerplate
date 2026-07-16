# deps: "py-genlayer:latest"
from genlayer import *
import json

class RoyJudgeArena(gl.Contract):
    def __init__(self):
        # State variables
        self.total_submissions = 0
        self.submissions = {}
        # Vector store to track text embeddings for plagiarism checking
        self.submission_vectors = {} 

    @gl.public.write
    def submit_and_judge(self, user_address: str, category: str, content: str) -> str:
        """
        Users submit their content here. The AI will judge it and check for originality.
        Allowed categories: 'Startup', 'Meme', 'Poem'
        """
        if category not in ['Startup', 'Meme', 'Poem']:
            raise gl.vm.UserError("Invalid category! Must be 'Startup', 'Meme', or 'Poem'.")
            
        if len(content) < 20:
             raise gl.vm.UserError("Content too short. Please provide more details.")

        # Step 1: Generate Embedding for the new content
        new_emb = gl.get_embedding(content)
        
        # Step 2: Check for Plagiarism (Originality Check)
        is_original = True
        highest_similarity = 0.0
        
        for sub_id, emb in self.submission_vectors.items():
            # In a real GenLayer vector store, we would use vector distance
            # Here we mock a basic check for demonstration of the logic
            # A real implementation would use gl.vector_store_insert_emb and query logic
            pass 
            
        # Step 3: AI Judgment using Optimistic Democracy
        prompt = f"""
        You are an expert AI Judge evaluating a {category} submission.
        
        Submission Content: "{content}"
        
        Evaluate the content strictly based on the {category} category.
        If it's a Startup, judge innovation and practicality.
        If it's a Meme, judge humor and relatability.
        If it's a Poem, judge creativity and rhythm.
        
        If the content is spam, gibberish, or completely irrelevant to the category, set "is_valid" to false.
        
        Respond ONLY using this JSON format:
        {{
            "is_valid": true/false,
            "score_out_of_10": <number 1-10>,
            "feedback": "<One sentence sharp and witty feedback>"
        }}
        """

        # Execute non-deterministic AI prompt
        result_str = gl.nondet.exec_prompt(prompt, response_format="json")
        
        try:
            clean_result = result_str.replace("```json", "").replace("```", "").strip()
            verdict = json.loads(clean_result)
            
            if not verdict.get("is_valid"):
                raise gl.vm.UserError("Submission rejected by AI: Deemed as spam or irrelevant.")
                
            # Step 4: Save successful submission to state
            self.total_submissions += 1
            self.submissions[self.total_submissions] = {
                "user": user_address,
                "category": category,
                "content": content,
                "score": verdict.get("score_out_of_10"),
                "feedback": verdict.get("feedback")
            }
            
            # Store embedding for future plagiarism checks
            self.submission_vectors[self.total_submissions] = new_emb
            
            return json.dumps({
                "status": "Success",
                "id": self.total_submissions,
                "score": verdict.get("score_out_of_10"),
                "feedback": verdict.get("feedback")
            })
            
        except json.JSONDecodeError:
            raise gl.vm.UserError("Failed to parse AI verdict. Please try again.")

    @gl.public.view
    def get_submission(self, sub_id: int) -> dict:
        if sub_id not in self.submissions:
            raise gl.vm.UserError("Submission not found.")
        return self.submissions[sub_id]
        
    @gl.public.view
    def get_leaderboard(self) -> dict:
        # Simple view to fetch all submissions for the frontend leaderboard
        return self.submissions
      
