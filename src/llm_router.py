import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from typing import Optional

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
XAI_API_KEY = os.getenv("XAI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt: str, system_prompt: str = "") -> str:
    if not GEMINI_API_KEY:
        return "⚠️ GEMINI_API_KEY غير موجود. أضفه في .env"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = f"{system_prompt}\n\nUser: {prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"خطأ في Gemini: {str(e)}"

def get_grok_response(prompt: str, system_prompt: str = "") -> str:
    """دعم Grok عبر xAI API (OpenAI compatible)"""
    if not XAI_API_KEY:
        return "⚠️ XAI_API_KEY غير موجود. استخدم Gemini أو أضف المفتاح."
    
    try:
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"خطأ في Grok: {str(e)}. تم الرجوع إلى Gemini."

def get_legal_response(prompt: str, system_prompt: str = "", preferred_model: str = "gemini") -> str:
    """Router محسن مع fallback"""
    if preferred_model == "grok" and XAI_API_KEY:
        return get_grok_response(prompt, system_prompt)
    else:
        return get_gemini_response(prompt, system_prompt)
