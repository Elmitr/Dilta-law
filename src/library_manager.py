import os
from database import get_all_library_items

def get_library_summary():
    """الحصول على ملخص المكتبة"""
    try:
        items = get_all_library_items()
        return {"total_items": len(items), "items": items[:10]}
    except Exception as e:
        print(f"Error in get_library_summary: {str(e)}")
        return {"total_items": 0, "items": []}

def get_library_stats():
    """إحصائيات المكتبة"""
    try:
        items = get_all_library_items()
        types = {}
        for item in items:
            item_type = item.get("item_type", "unknown")
            types[item_type] = types.get(item_type, 0) + 1
        return types
    except Exception as e:
        print(f"Error in get_library_stats: {str(e)}")
        return {}
