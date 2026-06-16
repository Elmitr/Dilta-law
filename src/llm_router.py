import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt: str, system_prompt: str = "") -> str:
    if not GEMINI_API_KEY:
        return "⚠️ خطأ: GEMINI_API_KEY غير موجود. يرجى التحقق من ملف .env"
    
    try:
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=system_prompt if system_prompt else None
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ خطأ في المعالجة: {str(e)}"

def get_legal_response(prompt: str, system_prompt: str = "", preferred_model: str = "gemini") -> str:
    return get_gemini_response(prompt, system_prompt)
