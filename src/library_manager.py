import os
from database import get_all_library_items

def get_library_summary():
    try:
        items = get_all_library_items()
        return {"total_items": len(items), "items": items[:8]}
    except:
        return {"total_items": 0, "items": []}
