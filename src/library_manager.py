import os
import chromadb
from chromadb.utils import embedding_functions
from src.database import add_library_item, get_all_library_items
from src.pdf_utils import extract_text_from_pdf
from src.llm_router import get_legal_response

CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma")
os.makedirs(CHROMA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=os.getenv("GEMINI_API_KEY", ""),
    model_name="models/embedding-001"
)
collection = client.get_or_create_collection(name="legal_library", embedding_function=embedding_function)

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
        response = get_legal_response(prompt, preferred_model="gemini")
        return response.strip()[:130]
    except:
        return "قانون مصري, عام"

def upload_to_library(file_path: str, title: str, item_type: str, description: str = "", tags: str = "") -> dict:
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

    item_id = add_library_item(title, item_type, description, dest_path, final_tags)

    collection.add(
        documents=[text_content[:7000]],
        metadatas=[{"title": title, "item_type": item_type, "tags": final_tags, "file_path": dest_path}],
        ids=[f"lib_{item_id}"]
    )

    return {
        "success": True,
        "message": f"تم رفع '{title}' بنجاح",
        "suggested_tags": final_tags
    }

def semantic_search_in_library(query: str, n_results: int = 6):
    try:
        return collection.query(query_texts=[query], n_results=n_results)
    except:
        return None

def get_library_summary():
    items = get_all_library_items()
    return {"total_items": len(items), "items": items[:8]}
