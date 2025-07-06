import uuid
from datetime import datetime
from typing import Dict


class CallManager:
    """
    Manages call sessions for customer inquiries.

    Tracks call sessions including organization ID, phone number,
    start time, and conversation logs. Each session is identified
    by a unique call ID (UUID).
    """

    def __init__(self):
        """
        Initializes an empty dictionary to store active call sessions.
        """
        self.call_sessions: Dict[str, Dict] = {}

    def initiate_call(self, org_id: str, phone_number: str) -> str:
        """
        Starts a new call session and returns a unique call ID.

        Args:
            org_id (str): The ID of the organization associated with the call.
            phone_number (str): The customer's phone number.

        Returns:
            str: A unique UUID representing the call session.
        """
        call_id = str(uuid.uuid4())
        self.call_sessions[call_id] = {
            "org_id": org_id,
            "phone_number": phone_number,
            "start_time": datetime.now(),
            "conversation": [],
        }
        return call_id

    def add_message(self, call_id: str, question: str, answer: str):
        """
        Adds a question-answer message pair to the specified call session.

        Args:
            call_id (str): The unique call ID of the session.
            question (str): The customer's question during the call.
            answer (str): The system-generated answer.

        Raises:
            ValueError: If the call ID does not exist.
        """
        if call_id not in self.call_sessions:
            raise ValueError("Invalid call ID")
        self.call_sessions[call_id]["conversation"].append(
            {"question": question, "answer": answer}
        )

    def end_call(self, call_id: str) -> Dict:
        if call_id not in self.call_sessions:
            raise ValueError("Invalid call ID")
        return self.call_sessions.pop(call_id)
