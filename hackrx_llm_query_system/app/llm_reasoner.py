# app/llm_reasoner.py
import os
import openai
import re
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def synthesize_llm_answer(question, chunks):
    # Compose prompt
    context = ""
    for c in chunks:
        context += f"{c['clause_id']}: {c['text']}\n---\n"
    user_query = f"""
DOCUMENT EXCERPTS:
{context}
USER QUESTION: "{question}"

INSTRUCTION: Answer clearly and concisely, only with supporting policy information. If unsure, say so.
"""
    messages = [
        {"role": "system", "content": "You are a precise insurance policy summarizer."},
        {"role": "user", "content": user_query}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo if no GPT-4 access
        messages=messages,
        temperature=0,
        max_tokens=256
    )
    ans = response['choices'][0]['message']['content'].strip()
    # Optionally, just extract the first paragraph/line as the answer:
    ans = ans.split("\n")[0]
    return ans
