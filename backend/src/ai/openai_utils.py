# src/ai/openai_utils.py

from openai import OpenAI
import os
import json

def get_ai_score(prompt: str):
    """
    Calls OpenAI to generate an AI-powered score and summary based on the given prompt.
    Returns a dictionary: {"score": float, "summary": str}
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt,
            max_output_tokens=200
        )
        return json.loads(response.output_text)
    except Exception as e:
        print(f"AI call failed: {e}")
        return {"score": 0, "summary": "AI analysis failed."}
