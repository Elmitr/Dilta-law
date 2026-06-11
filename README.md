# Dilta-law

**AI-Powered Legal Agent**

مشروع ذكاء اصطناعي متقدم لإدارة وتحليل الأحكام القضائية، مع دعم نظام Tag، قاعدة بيانات، وتصدير PDF.

## المميزات الرئيسية

- AI Agent ذكي لتحليل الاستشارات القانونية
- نظام Tag لتصنيف الأحكام
- قاعدة بيانات لتخزين والبحث في الأحكام
- تصدير الأحكام كملفات PDF
- واجهة سهلة الاستخدام باستخدام Streamlit

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