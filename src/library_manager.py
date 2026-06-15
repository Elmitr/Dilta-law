import os
import chromadb
from chromadb.utils import embedding_functions
from database import add_library_item, get_all_library_items
from pdf_utils import extract_text_from_pdf
from llm_router import get_legal_response

CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma")
os.makedirs(CHROMA_PATH, exist_ok=True)

# محاولة تهيئة ChromaDB مع معالجة الأخطاء
collection = None
try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    
    if gemini_key:
        embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=gemini_key,
            model_name="models/embedding-001"
        )
        collection = client.get_or_create_collection(
            name="legal_library", 
            embedding_function=embedding_function
        )
    else:
        print("تحذير: GEMINI_API_KEY غير موجود - ChromaDB سيكون معطلاً")
except Exception as e:
    print(f"خطأ في تهيئة ChromaDB: {e}")
    collection = None

LIBRARY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "library")
os.makedirs(LIBRARY_DIR, exist_ok=True)

def generate_smart_tags(document_text: str, item_type: str) -> str:
    """نظام التصنيف الذكي"""
    if len(document_text) < 100:
        return "قانون مصري, عام"
    
    prompt = f"""أنت خبير تصنيف قانوني مصري. أعطني 5 تصنيفات مناسبة مفصولة بفاصلة فقط للوثيقة التالية:
نوع الوثيقة: {item_type}
النص: {document_text[:2800]}"""
    
    try:
        response = get_legal_response(prompt, system_prompt="", preferred_model="gemini")
        if response and not response.startswith("⚠️") and not response.startswith("❌"):
            return response.strip()[:130]
        return "قانون مصري, عام"
    except Exception as e:
        print(f"خطأ في التصنيف الذكي: {e}")
        return "قانون مصري, عام"

def upload_to_library(file_path: str, title: str, item_type: str, description: str = "", tags: str = "") -> dict:
    """رفع وثيقة إلى المكتبة"""
    try:
        if not os.path.exists(file_path):
            return {"success": False, "message": "الملف غير موجود"}

        filename = os.path.basename(file_path)
        dest_path = os.path.join(LIBRARY_DIR, filename)
        
        import shutil
        shutil.copy(file_path, dest_path)

        text_content = extract_text_from_pdf(dest_path)
        if not text_content:
            return {"success": False, "message": "فشل استخراج النص من الملف"}

        # نظام التصنيف الذكي
        final_tags = tags.strip() if tags.strip() else generate_smart_tags(text_content, item_type)

        # حفظ في SQLite
        item_id = add_library_item(title, item_type, description, dest_path, final_tags)

        # حفظ في ChromaDB (اختياري)
        if collection:
            try:
                collection.add(
                    documents=[text_content[:7000]],
                    metadatas=[{"title": title, "item_type": item_type, "tags": final_tags, "file_path": dest_path}],
                    ids=[f"lib_{item_id}"]
                )
            except Exception as e:
                print(f"تحذير: فشل إضافة الوثيقة إلى ChromaDB: {e}")

        return {
            "success": True,
            "message": f"تم رفع '{title}' بنجاح",
            "suggested_tags": final_tags
        }
    except Exception as e:
        return {"success": False, "message": f"خطأ في الرفع: {str(e)}"}

def semantic_search_in_library(query: str, n_results: int = 6):
    """البحث الدلالي في المكتبة"""
    try:
        if not collection:
            return None
        return collection.query(query_texts=[query], n_results=n_results)
    except Exception as e:
        print(f"خطأ في البحث: {e}")
        return None

def get_library_summary():
    """الحصول على ملخص المكتبة"""
    try:
        items = get_all_library_items()
        return {"total_items": len(items), "items": items[:8]}
    except Exception as e:
        print(f"خطأ في الحصول على ملخص المكتبة: {e}")
        return {"total_items": 0, "items": []}
