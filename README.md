# ⚖️ Dilta-law

**AI-Powered Legal Agent** — متخصص في **القانون المصري**

يعتمد كلياً على رفعك للوثائق (لا يتصل بأي مصادر خارجية).

### المميزات الحالية
- رفع أحكام، قوانين، كتب (PDF)
- **تصنيف ذكي تلقائي** بـ Gemini
- **بحث دلالي** قوي داخل المكتبة
- دعم Gemini Flash (مجاني) + Grok
- تصدير PDF

### تشغيل سريع

```bash
pip install -r requirements.txt
streamlit run src/main.py
## هيكل المشروع

```
Dilta-law/
├── src/
│   ├── main.py                 # التطبيق الرئيسي (Streamlit)
│   ├── agent.py                # الـ AI Agent الرئيسي
│   ├── database.py             # إدارة قاعدة البيانات
│   ├── tagging.py              # نظام Tag للأحكام
│   ├── pdf_generator.py        # تصدير PDF
│   └── utils/
├── prompts/
│   └── system.txt
├── requirements.txt
├── Dockerfile
└── README.md
```
