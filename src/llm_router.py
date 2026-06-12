import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
XAI_API_KEY = os.getenv("XAI_API_KEY", "")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt: str, system_prompt: str = "") -> str:
    """Get response from Google Gemini Flash (free tier)."""
    if not GEMINI_API_KEY:
        return "⚠️ لم يتم تعيين GEMINI_API_KEY. يرجى إضافته في ملف .env"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ في Gemini: {str(e)}"

def get_grok_response(prompt: str, system_prompt: str = "") -> str:
    """Placeholder for Grok support."""
    if not XAI_API_KEY:
        return "⚠️ لم يتم تعيين XAI_API_KEY. يمكنك استخدام Gemini كبديل مجاني."
    return "🚧 دعم Grok قيد التطوير. استخدم Gemini حالياً."

def get_legal_response(prompt: str, system_prompt: str = "", 
                       preferred_model: str = "gemini") -> str:
    """Main router function."""
    if preferred_model == "grok":
        return get_grok_response(prompt, system_prompt)
    else:
        return get_gemini_response(prompt, system_prompt)
