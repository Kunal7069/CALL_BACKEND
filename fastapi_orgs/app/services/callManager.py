import uuid
from datetime import datetime
from typing import Dict, List


class CallManager:
    def __init__(self):
        self.call_sessions: Dict[str, Dict] = {}

    def initiate_call(self, org_id: str, phone_number: str) -> str:
        print(phone_number,datetime.now())
        call_id = str(uuid.uuid4())
        self.call_sessions[call_id] = {
            "org_id": org_id,
            "phone_number": phone_number,
            "start_time": datetime.now(),
            "conversation": []
        }
        return call_id

    def add_message(self, call_id: str, question: str, answer: str):
        if call_id not in self.call_sessions:
            raise ValueError("Invalid call ID")
        self.call_sessions[call_id]["conversation"].append({
            "question": question,
            "answer": answer
        })

    def end_call(self, call_id: str) -> Dict:
        if call_id not in self.call_sessions:
            raise ValueError("Invalid call ID")
        return self.call_sessions.pop(call_id)