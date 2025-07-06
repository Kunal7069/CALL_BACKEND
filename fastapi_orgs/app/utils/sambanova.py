import json
import re
import traceback

import pytz

from fastapi_orgs.app.config.sambanova import client
from fastapi_orgs.app.settings import (
    CALL_SUMMARY_PROMPT_TEMPLATE,
    QUESTION_PROMPT_TEMPLATE,
)
from fastapi_orgs.app.utils.csv_parser import save_summary_to_csv


class SambaNovaService:
    async def ask_question(self, description: dict, question: str) -> str:
        """
        Asks SambaNova a contextual question using provided description and returns the assistant's answer.

        Args:
            description (dict): Dictionary containing organization-specific contextual info.
            question (str): The user query.

        Returns:
            str: AI-generated answer from SambaNova.
        """
        context = "\n".join([f"{k}: {v}" for k, v in description.items()])
        prompt = QUESTION_PROMPT_TEMPLATE.format(context=context, question=question)

        return self._call_llm(
            prompt, role="You are a helpful assistant for a hotel booking system."
        )

    async def extract_summary(self, session: dict) -> dict:
        """
        Extracts structured summary from a call session and saves it as a CSV row.

        Args:
            session (dict): Call session containing phone number, conversation, and start time.

        Returns:
            dict: Structured call summary with metadata.
        """
        convo = session["conversation"]
        phone_number = session.get("phone_number", "NA")
        ist_time = session.get("start_time")

        # Convert time to readable IST
        if ist_time:
            ist = pytz.timezone("Asia/Kolkata")
            ist_time = ist.localize(ist_time).strftime("%d %B %I:%M:%S %p")
        else:
            ist_time = "NA"
        convo_text = "\n".join([f"Q: {m['question']}\nA: {m['answer']}" for m in convo])
        prompt = CALL_SUMMARY_PROMPT_TEMPLATE.format(
            conversation=convo_text, call_time=ist_time, phone_number=phone_number
        )
        try:
            raw_content = self._call_llm(
                prompt, role="You are an AI assistant that summarizes booking calls."
            ).strip()
            if not raw_content:
                return {"error": "SambaNova returned empty content."}

            # Clean triple backtick formatting
            if raw_content.startswith("```"):
                raw_content = re.sub(r"^```(?:json)?\n?", "", raw_content)
                raw_content = re.sub(r"\n?```$", "", raw_content)

            summary_json = json.loads(raw_content)
            summary_json["call_time"] = ist_time
            summary_json["phone_number"] = phone_number

            await save_summary_to_csv(summary_json)

            return summary_json

        except Exception:
            traceback.print_exc()
            return {"summary_raw_text": raw_content}

    def _call_llm(self, prompt: str, role: str) -> str:
        """
        Calls the SambaNova LLM with a system role and user prompt.

        Args:
            prompt (str): The user-provided prompt or template.
            role (str): The system role defining the assistant's behavior.

        Returns:
            str: The AI's message content response.
        """
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            top_p=1.0,
        )
        return response.choices[0].message.content
