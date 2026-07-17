# deps: "py-genlayer:latest"
from genlayer import *
import json

class RoyJudgeArena(gl.Contract):
    def __init__(self):
        self.total = 0
        self.subs = {}

    @gl.public.write
    def submit_and_judge(self, user_addr: str, cat: str, content: str) -> str:
        prompt = f'Evaluate {cat}: "{content}". Reply ONLY in JSON: {{"is_valid": true, "score_out_of_10": 8, "feedback": "Nice"}}'
        res = gl.nondet.exec_prompt(prompt, response_format="json")
        v = json.loads(res)
        self.total += 1
        self.subs[self.total] = {
            "user": user_addr,
            "category": cat,
            "content": content,
            "score": v.get("score_out_of_10"),
            "feedback": v.get("feedback")
        }
        return json.dumps({"status": "Success"})

    @gl.public.view
    def get_leaderboard(self) -> dict:
        return self.subs
      
