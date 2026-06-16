import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(__file__))

try:
    from database import init_db, get_all_library_items
    from library_manager import get_library_summary
    from llm_router import get_legal_response
except ImportError as e:
    st.error(f"❌ خطأ في الاستيراد: {e}")
    st.stop()

init_db()

st.set_page_config(
    page_title="Dilta-law | المساعد القانوني الذكي",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Dilta-law")
st.markdown("### المساعد القانوني الذكي للقانون المصري")
st.caption("يعتمد كلياً على المحتوى الذي ترفعه | نماذج مجانية")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.success("✅ التطبيق يعمل بنجاح")
    st.divider()
    model_choice = st.selectbox(
        "النموذج المستخدم",
        ["Gemini Flash (مجاني - موصى به)"]
    )
    st.caption("Dilta-law v0.2 | يونيو 2026")

tab1, tab2 = st.tabs(["🔍 البحث والتحليل", "📚 المكتبة (قريباً)"])

with tab1:
    st.header("🔍 المستشار القانوني الذكي")
    st.write("أسأل عن أي موضوع قانوني متعلق بالقانون المصري")
    
    query = st.text_area(
        "اكتب سؤالك القانوني:",
        height=120,
        placeholder="مثال: ما هي حقوق العامل في القانون المصري؟"
    )
    
    if st.button("🚀 احصل على الإجابة", type="primary", use_container_width=True):
        if not query.strip():
            st.warning("⚠️ من فضلك اكتب سؤالك أولاً")
        else:
            with st.spinner("جاري المعالجة..."):
                system_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "system.txt")
                system = ""
                
                if os.path.exists(system_path):
                    with open(system_path, "r", encoding="utf-8") as f:
                        system = f.read()
                
                response = get_legal_response(query, system_prompt=system, preferred_model="gemini")
                
                st.subheader("⚖️ الإجابة")
                st.markdown(response)
                
                with st.expander("💾 حفظ الإجابة"):
                    st.text_area("انسخ الإجابة", value=response, height=200)

with tab2:
    st.header("📚 المكتبة القانونية")
    st.info("قريباً: رفع وتخزين الوثائق القانونية")
