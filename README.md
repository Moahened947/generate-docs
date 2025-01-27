# مولد الأبحاث الذكي | AI Research Document Generator

نظام ذكي لإنشاء الأبحاث والتقارير باستخدام الذكاء الاصطناعي Google Gemini.

## المميزات | Features

- واجهة ويب سهلة الاستخدام باللغة العربية
- إنشاء أبحاث شاملة ومنظمة
- تنسيق تلقائي للمستندات مع أحجام خطوط مختلفة:
  - العناوين الرئيسية: 16 نقطة
  - العناوين الفرعية: 14 نقطة
  - المحتوى: 12 نقطة
- حفظ الملفات في مجلد مخصص (Researchs)
- تحميل مباشر للملفات بصيغة Word
- واجهة تفاعلية مع رسائل نجاح وتنبيهات
- إمكانية إنشاء أبحاث متعددة بسهولة

## المتطلبات | Requirements

```bash
pip install -r requirements.txt
```

المتطلبات الأساسية:
- Python 3.8+
- Flask
- python-docx
- google-generativeai
- Internet connection

## الإعداد | Setup

1. قم بتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

2. احصل على مفتاح API من Google:
   - اذهب إلى https://makersuite.google.com/app/apikey
   - أنشئ مفتاح API جديد
   - استبدل `YOUR_GOOGLE_API_KEY` في ملف `main.py` بمفتاح API الخاص بك

## التشغيل | Usage

1. شغل التطبيق:
```bash
python app.py
```

2. افتح المتصفح على العنوان:
```
http://localhost:5000
```

3. استخدام التطبيق:
   - أدخل موضوع البحث في الحقل المخصص
   - انقر على "إنشاء البحث"
   - انتظر حتى اكتمال العملية
   - اضغط على "تحميل البحث" لتحميل الملف
   - يمكنك إنشاء بحث جديد باستخدام زر "موضوع جديد"

## هيكل المشروع | Project Structure

```
generate docs/
│
├── app.py              # تطبيق Flask الرئيسي
├── main.py             # منطق إنشاء المستندات
├── requirements.txt    # متطلبات المشروع
├── README.md          # توثيق المشروع
│
├── templates/         # قوالب HTML
│   └── index.html    # الصفحة الرئيسية
│
└── Researchs/        # مجلد حفظ الأبحاث المولدة
```

## المخرجات | Output

- يتم إنشاء ملف Word لكل بحث
- يحتوي كل بحث على:
  - عنوان رئيسي
  - مقدمة
  - المفاهيم والتعريفات الرئيسية
  - الحالة الراهنة والتطورات
  - التطبيقات وحالات الاستخدام
  - التوقعات المستقبلية
  - الخاتمة

## الأمان | Security

- يجب حماية مفتاح API الخاص بك
- في بيئة الإنتاج، استخدم متغيرات البيئة لتخزين المفاتيح الحساسة
- تأكد من تقييد الوصول إلى التطبيق حسب الحاجة

## المساهمة | Contributing

نرحب بمساهماتكم! يرجى:
1. عمل Fork للمشروع
2. إنشاء فرع لميزتك (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى الفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## الترخيص | License

هذا المشروع مرخص تحت رخصة MIT - انظر ملف `LICENSE` للتفاصيل.

## الدعم | Support

إذا واجهت أي مشاكل أو لديك اقتراحات، يرجى فتح issue في GitHub.
