# deps: "py-genlayer:latest"
from genlayer import *
import json

class RoyJudgeArena(gl.Contract):
    def __init__(self):
        self.total = 0
        self.subs = {}

    @gl.public.write
    def submit_and_judge(self, user_addr: str, cat: str, content: str) -> str:
        prompt = 'Evaluate ' + cat + ': ' + content + '. Reply strictly in JSON format: {"score": 8, "feedback": "Good"}'
        res = gl.nondet.exec_prompt(prompt)
        
        try:
            v = json.loads(res)
            score = v.get("score", 5)
            feedback = v.get("feedback", "No feedback")
        except:
            score = 5
            feedback = res
            
        self.total += 1
        self.subs[str(self.total)] = {
            "user": user_addr,
            "category": cat,
            "content": content,
            "score": score,
            "feedback": feedback
        }
        return "Success"

    @gl.public.view
    def get_leaderboard(self) -> str:
        return json.dumps(self.subs)
        
