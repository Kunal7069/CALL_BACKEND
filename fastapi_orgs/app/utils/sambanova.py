import os
from openai import OpenAI
import traceback
import json
import re
import pytz
import pandas as pd
from datetime import datetime
from app.utils.csv_parser import save_summary_to_csv

# Load credentials from environment
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
SAMBANOVA_ENDPOINT = os.getenv("SAMBANOVA_ENDPOINT", "https://api.sambanova.ai/v1")

# Setup SambaNova client
client = OpenAI(
    api_key=SAMBANOVA_API_KEY,
    base_url=SAMBANOVA_ENDPOINT
)

async def ask_sambanova(description: dict, question: str) -> str:
    context = "\n".join([f"{k}: {v}" for k, v in description.items()])
    prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a hotel booking system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        top_p=1.0
    )

    return response.choices[0].message.content

async def extract_summary(session: dict) -> dict:
    convo = session["conversation"]
    phone_number = session.get("phone_number", "NA")

    # Convert start_time to IST readable string
    ist_time = session.get("start_time")
    
    if ist_time:
        ist = pytz.timezone("Asia/Kolkata")
        ist_time = ist.localize(ist_time).strftime("%d %B %I:%M:%S %p")
    else:
        ist_time = "NA"

    convo_text = "\n".join([f"Q: {m['question']}\nA: {m['answer']}" for m in convo])

    prompt = f"""
This is a call log between a customer and the booking assistant.
Conversation:
{convo_text}

Extract the following in JSON format with the exact field names and add call_time as "{ist_time}" and phone_number as "{phone_number}":
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

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct",
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes booking calls."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        top_p=1.0
    )

    try:
        # 📦 Log full response object
        print("🧾 Full response from SambaNova:")
        print(response)

        # ✅ Safe access to message content
        message = response.choices[0].message.content if response.choices[0].message else ""
        raw_content = message.strip()
        
        print("📨 Raw content received:")
        print(raw_content)

        if not raw_content:
            print("⚠️ Empty response content from SambaNova.")
            return {"error": "SambaNova returned empty content."}

        print("1️⃣ Parsing JSON")
        if raw_content.startswith("```"):
            raw_content = re.sub(r"^```(?:json)?\n?", "", raw_content)
            raw_content = re.sub(r"\n?```$", "", raw_content)
        print(raw_content)
        summary_json = json.loads(raw_content)
        print("2️⃣ JSON Parsed Successfully")

        # Add enriched fields
        summary_json["call_time"] = ist_time
        summary_json["phone_number"] = phone_number

        print("✅ Final Summary JSON to Save:")
        print(summary_json)

        # Save to CSV
        try:
            # from app.utils.csv_writer import save_summary_to_csv
            await save_summary_to_csv(summary_json)
            print("✅ CSV write successful")
        except Exception as file_err:
            print("❌ Failed to write CSV:", str(file_err))

        return summary_json

    except Exception as e:
        print("❌ Exception occurred while parsing or saving summary:")
        traceback.print_exc()
        return {"summary_raw_text": raw_content}