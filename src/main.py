import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(__file__))

from database import init_db, add_judgment, get_all_judgments
from pdf_utils import extract_text_from_pdf, create_judgment_pdf
from library_manager import upload_to_library, semantic_search_in_library, get_library_summary
from llm_router import get_legal_response

init_db()

st.set_page_config(
    page_title="Dilta-law | المساعد القانوني الذكي",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Dilta-law")
st.markdown("### المساعد القانوني الذكي للقانون المصري")
st.caption("يعتمد كلياً على المحتوى الذي ترفعه | نماذج مجانية")

# Sidebar
with st.sidebar:
    st.header("⚙️ الإعدادات")
    model_choice = st.selectbox(
        "النموذج المستخدم في التحليل",
        ["Gemini Flash (مجاني - موصى به)", "Grok (يتطلب API Key)"]
    )
    preferred_model = "gemini" if "Gemini" in model_choice else "grok"
    st.info("النموذج الافتراضي: Gemini Flash (طبقة مجانية)")
    st.caption("Dilta-law v0.2 | يونيو 2026")

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 المكتبة القانونية", "🔍 البحث والتحليل", "⚖️ إدارة الأحكام"])

# ==================== TAB 1: المكتبة القانونية ====================
with tab1:
    st.header("📚 المكتبة القانونية الشخصية")
    st.write("ارفع الوثائق القانونية وسيتم تصنيفها ذكياً تلقائياً باستخدام Gemini")

    uploaded_file = st.file_uploader("ارفع ملف PDF (حكم / قانون / كتاب)", type=["pdf"])

    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("عنوان الوثيقة", value=uploaded_file.name)
            item_type = st.selectbox("نوع الوثيقة", ["حكم قضائي", "قانون", "كتاب قانوني", "مذكرة", "أخرى"])
        with col2:
            tags = st.text_input("تصنيفات (اتركه فارغاً ليتم التصنيف الذكي تلقائياً)")

        if st.button("📥 رفع إلى المكتبة + تصنيف ذكي", type="primary"):
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = upload_to_library(
                file_path=temp_path,
                title=title,
                item_type=item_type,
                tags=tags
            )

            if result.get("success"):
                st.success(result["message"])
                if result.get("suggested_tags"):
                    st.info(f"**التصنيفات الذكية المقترحة:** {result['suggested_tags']}")
            else:
                st.error(result.get("message", "حدث خطأ"))

    st.divider()
    st.subheader("محتويات المكتبة")
    summary = get_library_summary()
    st.metric("إجمالي العناصر في المكتبة", summary["total_items"])

# ==================== TAB 2: البحث والتحليل ====================
with tab2:
    st.header("🔍 البحث الدلالي والتحليل الذكي")

    query = st.text_area("اكتب استشارتك أو سؤالك القانوني:", height=100)

    search_type = st.radio("نوع البحث", ["بحث دلالي في المكتبة", "تحليل مباشر بالـ AI"])

    if st.button("🚀 ابدأ التحليل", type="primary"):
        if query:
            with st.spinner("جاري المعالجة باستخدام النموذج الذكي..."):
                if search_type == "بحث دلالي في المكتبة":
                    results = semantic_search_in_library(query)
                    st.subheader("نتائج البحث الدلالي")

                    if results and results.get("documents"):
                        for i, doc in enumerate(results["documents"][0][:6]):
                            meta = results["metadatas"][0][i]
                            with st.container(border=True):
                                st.markdown(f"**📄 {meta.get('title', 'وثيقة')}**")
                                st.caption(f"النوع: {meta.get('item_type', '-')} | التصنيفات: {meta.get('tags', '-')}")
                                st.write(doc[:500] + "..." if len(doc) > 500 else doc)
                    else:
                        st.info("لم يتم العثور على نتائج. تأكد من وجود وثائق في المكتبة.")
                else:
                    system_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "system.txt")
                    with open(system_path, "r", encoding="utf-8") as f:
                        system = f.read()
                    response = get_legal_response(query, system_prompt=system, preferred_model=preferred_model)
                    st.subheader("إجابة الوكيل القانوني")
                    st.markdown(response)
