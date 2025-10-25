
# Create README file
readme_md = """# متجر تاجر السعودية - Saudi Store

## نظرة عامة | Overview

متجر إلكتروني متكامل لعرض وبيع المنتجات عبر الإنترنت مع دعم كامل للغة العربية وتكامل مع واتساب للطلبات.

A complete e-commerce store for displaying and selling products online with full Arabic language support and WhatsApp integration for orders.

## الميزات | Features

✅ واجهة عربية متجاوبة تماماً (Fully Responsive Arabic Interface)
✅ دعم RTL كامل (Full RTL Support)
✅ تكامل مع واتساب للطلبات (WhatsApp Integration)
✅ عرض المنتجات حسب الفئات (Category-based Product Display)
✅ بيانات تجريبية للاختبار (Demo Data for Testing)
✅ معالجة محسّنة للأخطاء (Enhanced Error Handling)
✅ تصميم حديث وجذاب (Modern and Attractive Design)
✅ سريع وخفيف (Fast and Lightweight)

## الملفات الأساسية | Essential Files

```
saudi-store/
│
├── index.html          # الصفحة الرئيسية
├── styles.css          # ملف التنسيقات
├── script.js           # الوظائف الأساسية
├── config.js           # ملف الإعدادات
└── README.md           # هذا الملف
```

## التثبيت والتشغيل | Installation & Setup

### الطريقة 1: استخدام البيانات التجريبية (Demo Mode)

1. قم بتحميل جميع الملفات
2. افتح ملف `index.html` في المتصفح
3. ستظهر المنتجات التجريبية تلقائياً

### الطريقة 2: الربط مع API حقيقي (Real API Integration)

1. افتح ملف `config.js`
2. غيّر القيم التالية:

```javascript
const CONFIG = {
    API_URL: 'https://your-api.com/products', // رابط API الخاص بك
    API_KEY: 'your-api-key-here',              // مفتاح API
    USE_DEMO_DATA: false,                      // غيرها إلى false
    WHATSAPP_NUMBER: '966500000000',           // رقم واتساب الخاص بك
};
```

## التخصيص | Customization

### تغيير الألوان

افتح `styles.css` وعدل المتغيرات في `:root`:

```css
:root {
    --primary-color: #2c7a3e;      /* اللون الأساسي */
    --secondary-color: #1a5a2e;    /* اللون الثانوي */
    --accent-color: #f4a442;       /* لون التمييز */
}
```

### إضافة منتجات جديدة (وضع تجريبي)

افتح `config.js` وأضف منتجات إلى `DEMO_PRODUCTS`:

```javascript
DEMO_PRODUCTS: [
    {
        id: 7,
        title: 'منتج جديد',
        price: 299.99,
        description: 'وصف المنتج',
        image: 'رابط الصورة',
        category: 'الفئة'
    }
]
```

## المشاكل الشائعة وحلولها | Common Issues & Solutions

### المنتجات لا تظهر

✅ **الحل:**
1. تأكد من أن `USE_DEMO_DATA: true` في `config.js`
2. افتح Console في المتصفح (F12) للتحقق من الأخطاء
3. تأكد من تحميل جميع الملفات بشكل صحيح

### الصور لا تظهر

✅ **الحل:**
1. تأكد من صحة روابط الصور
2. استخدم روابط HTTPS
3. تأكد من أن الصور متاحة للوصول العام

### واتساب لا يعمل

✅ **الحل:**
1. تأكد من تعديل `WHATSAPP_NUMBER` في `config.js`
2. استخدم التنسيق الدولي: 966XXXXXXXXX
3. تأكد من عدم وجود مسافات أو رموز خاصة

## الملفات الضرورية | Required Files

### ✅ ضروري (Essential):
- `index.html` - الصفحة الرئيسية
- `styles.css` - التنسيقات
- `script.js` - الوظائف
- `config.js` - الإعدادات

### ⚠️ اختياري (Optional):
- `README.md` - التوثيق
- `images/` - مجلد الصور المحلية
- `favicon.ico` - أيقونة الموقع

### ❌ يمكن حذفه (Can be Deleted):
- `node_modules/` - المكتبات
- `*.zip`, `*.rar` - ملفات مضغوطة
- `backup/` - نسخ احتياطية قديمة
- `.git/` - تاريخ Git (إن لم تستخدمه)
- `test/` - ملفات الاختبار
- `.psd`, `.ai` - ملفات التصميم الأولية
- `.DS_Store` - ملفات Mac
- `Thumbs.db` - ملفات Windows

## التقنيات المستخدمة | Technologies Used

- HTML5
- CSS3 (Flexbox & Grid)
- JavaScript (ES6+)
- Font Awesome Icons
- RTL Support

## المتطلبات | Requirements

- متصفح حديث يدعم ES6+
- اتصال بالإنترنت (لتحميل Font Awesome)

## الترخيص | License

هذا المشروع مفتوح المصدر ومتاح للاستخدام الحر.

This project is open source and available for free use.

## الدعم | Support

للدعم الفني أو الاستفسارات:
- WhatsApp: [رقمك هنا]
- Email: [بريدك هنا]

## التحديثات المستقبلية | Future Updates

- [ ] نظام سلة التسوق
- [ ] نظام الدفع الإلكتروني
- [ ] لوحة تحكم للإدارة
- [ ] نظام تقييم المنتجات
- [ ] البحث المتقدم
- [ ] الفلترة المتعددة

---

**تم التطوير بواسطة:** اعلانات العرب للتسويق الالكتروني

**Developed by:** Arab Ads for Digital Marketing

**Version:** 2.0 (محدث ومُصحح)
"""

with open('/tmp/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_md)

print("✅ تم إنشاء ملف README.md")
print("=" * 60)
