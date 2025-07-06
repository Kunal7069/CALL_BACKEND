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
}

ORG_ROUTES = {"create": "/organizations/", "get_by_name": "/organizations/{name}"}
