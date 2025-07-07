import ast
import os

from dotenv import load_dotenv

load_dotenv()

# Read raw JSON (Python-style) from env and convert it safely
raw_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")
GOOGLE_CREDENTIALS = ast.literal_eval(raw_creds)


SPREADSHEET_ID = "1GwMoKuAGReebrve7MWgi-6xHYhQK2NoSnS2BdY2wZWM"
SHEET_NAME = "Sheet1"

CALL_SUMMARY_PROMPT_TEMPLATE = """
This is a call log between a customer and the booking assistant.
Conversation:
{conversation}

Extract the following in JSON format with the exact field names and add call_time as "{call_time}" and phone_number as "{phone_number}":
{{
  "call_outcome": "<Enquiry / Availability / Post-Booking / Misc>",
  "checkin_date": "<YYYY-MM-DD or NA>",
  "checkout_date": "<YYYY-MM-DD or NA>",
  "customer_name": "<Name or NA>",
  "room_name": "<Room Name or NA>",
  "num_guests": "<Number or NA>",
  "call_summary": "<Short summary>"
}}

Only return valid JSON, without any extra commentary or explanation and just return json.
"""


# Prompt template for answering questions
QUESTION_PROMPT_TEMPLATE = """Context:
{context}

Question:
{question}

Answer:"""


CALL_ROUTES = {
    "initiate": "/calls/initiate",
    "message": "/calls/{call_id}/message",
    "end": "/calls/{call_id}/end",
    "keys": "/keys/{call_id}",
}

ORG_ROUTES = {"create": "/organizations/", "get_by_name": "/organizations/{name}"}
