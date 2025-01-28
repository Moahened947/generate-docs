# مولد الأبحاث والتقارير الذكي 📚

تطبيق ويب مبني على Python وFlask يستخدم نموذج Google Gemini لإنشاء أبحاث وتقارير احترافية بشكل تلقائي.

## المميزات 🌟

- **دعم أنواع متعددة من المستندات**:
  - بحث علمي
  - تقرير فني
  - تقرير إداري
  - تقرير علمي
  - تقرير مالي
  - تقرير مشروع

- **واجهة مستخدم سهلة الاستخدام**:
  - تصميم عصري وجذاب
  - تجربة مستخدم سلسة
  - إشعارات مباشرة (Toasts)
  - مؤشرات تحميل تفاعلية

- **تخصيص المحتوى**:
  - إضافة تعليمات خاصة للمحتوى
  - تحديد نوع المستند
  - اختيار لغة المستند (العربية/الإنجليزية)

- **تنسيق تلقائي للمستندات**:
  - دعم كامل للغة العربية (RTL)
  - تنسيق احترافي للعناوين والمحتوى
  - أحجام خطوط متناسقة
  - تنسيق النقاط والقوائم

## المتطلبات 📋

```bash
pip install -r requirements.txt
```

المتطلبات الرئيسية:
- Python 3.7+
- Flask
- python-docx
- google.generativeai
- Bootstrap 5
- Font Awesome

## التثبيت والتشغيل 🚀

1. قم بنسخ المستودع:
```bash
git clone <repository-url>
cd generate-docs
```

2. قم بتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. قم بإضافة مفتاح API الخاص بـ Google Gemini:
```python
# في ملف main.py
genai.configure(api_key='your-api-key')
```

4. قم بتشغيل التطبيق:
```bash
python app.py
```

5. افتح المتصفح على العنوان:
```
http://localhost:5000
```

## كيفية الاستخدام 📝

1. اختر نوع المستند من القائمة المنسدلة
2. أدخل موضوع المستند
3. أضف أي تعليمات خاصة (اختياري)
4. اختر لغة المستند (العربية/الإنجليزية)
5. انقر على "إنشاء المستند"
6. انتظر حتى يتم إنشاء المستند
7. قم بتحميل المستند بصيغة Word

## الهيكل التنظيمي للمشروع 📂

```
generate-docs/
├── app.py              # تطبيق Flask الرئيسي
├── main.py            # المنطق الرئيسي وتوليد المحتوى
├── requirements.txt   # متطلبات المشروع
├── static/           # الملفات الثابتة
└── templates/        # قوالب HTML
    └── index.html    # الصفحة الرئيسية
```

## المساهمة 🤝

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:
1. Fork المستودع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى الفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## الترخيص 📄

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## الاتصال 📧

- المطور: [اسم المطور]
- البريد الإلكتروني: [البريد الإلكتروني]
- موقع المشروع: [رابط المشروع]

---
صنع بـ ❤️ في مصر 🇪🇬
