# تقرير المشروع - منصة المجوهرات والتجارة الإلكترونية مع التصميم بالذكاء الاصطناعي

## تاريخ الإنشاء: 2026-02-24

---

## ملخص المشروع

تم تطوير backend كامل لمنصة تجارة إلكترونية للمجوهرات مع ميزة توليد التصاميم باستخدام الذكاء الاصطناعي (Google Gemini API).

---

## التقنيات المستخدمة

| التقنية | الاستخدام |
|---------|-----------|
| FastAPI | إطار عمل الـ Backend |
| MySQL | قاعدة البيانات (عبر XAMPP) |
| SQLAlchemy | ORM للتعامل مع قاعدة البيانات |
| Pydantic | التحقق من البيانات |
| python-jose | JWT للمصادقة |
| passlib | تشفير كلمات المرور |
| Google Gemini API | توليد تصاميم المجوهرات |

---

## قاعدة البيانات (12 جدول)

### 1. Users (المستخدمين)
- `id` - المعرف الفريد
- `username` - اسم المستخدم
- `password` - كلمة المرور (مشفرة)
- `email` - البريد الإلكتروني
- `first_name` - الاسم الأول
- `last_name` - الاسم الأخير
- `phone` - رقم الهاتف
- `dob` - تاريخ الميلاد
- `gender` - الجنس
- `address` - العنوان
- `created_at` - تاريخ الإنشاء

### 2. Jewelers (الصائغين)
- `id`, `name`, `shop_name`, `bio`, `address`, `phone`, `email`, `rating`, `created_at`

### 3. Payment_Methods (طرق الدفع)
- `id`, `method_name`, `qr_code_image`, `is_active`, `notes`

### 4. Categories (التصنيفات)
- `id`, `name`, `parent_id` (لدعم التصنيفات الفرعية)

### 5. Products (المنتجات)
- `id`, `jeweler_id`, `name`, `material`, `karat`, `weight`, `price`, `stock_quantity`, `description`, `image_path`

### 6. Product_Images (صور المنتجات)
- `id`, `product_id`, `image_path`, `display_order`

### 7. Product_Categories (ربط المنتجات بالتصنيفات)
- علاقة Many-to-Many

### 8. Carts (سلات التسوق)
- `id`, `user_id`, `updated_at`

### 9. Cart_Items (عناصر السلة)
- `id`, `cart_id`, `product_id`, `quantity`

### 10. Orders (الطلبات)
- `id`, `user_id`, `payment_method_id`, `order_date`, `status`, `total_amount`, `shipping_address`, `transfer_receipt`

### 11. Order_Items (عناصر الطلب)
- `id`, `order_id`, `product_id`, `quantity`, `unit_price`, `subtotal`

### 12. User_Generated_Designs (تصاميم المستخدمين)
- `id`, `user_id`, `selected_options` (JSON), `generated_image_url`, `created_at`

### 13. Design_Requests (طلبات التصميم المخصص)
- `id`, `user_id`, `jeweler_id`, `generated_design_id`, `request_date`, `description`, `attachment_url`, `estimated_budget`, `jeweler_price_offer`, `status`

---

## API Endpoints

### المصادقة (`/api/auth`)
- `POST /register` - تسجيل مستخدم جديد
- `POST /login` - تسجيل الدخول والحصول على JWT token
- `GET /me` - الحصول على بيانات المستخدم الحالي

### المنتجات (`/api/products`)
- `GET /` - عرض جميع المنتجات (مع فلاتر)
- `GET /{product_id}` - عرض منتج واحد
- `GET /categories/` - عرض جميع التصنيفات

### سلة التسوق (`/api/cart`)
- `GET /` - عرض السلة
- `POST /add` - إضافة منتج للسلة
- `PUT /update/{item_id}` - تحديث الكمية
- `DELETE /remove/{item_id}` - حذف منتج
- `DELETE /clear` - تفريغ السلة

### الطلبات (`/api/orders`)
- `GET /` - عرض طلبات المستخدم
- `GET /{order_id}` - تفاصيل طلب
- `POST /checkout` - إنشاء طلب من السلة

### الإدارة (`/api/admin`)
- `POST /products` - إنشاء منتج
- `PUT /products/{id}` - تحديث منتج
- `DELETE /products/{id}` - حذف منتج
- `POST /categories` - إنشاء تصنيف
- `POST /payment-methods` - إنشاء طريقة دفع
- `GET /orders` - عرض جميع الطلبات
- `PUT /orders/{id}/status` - تحديث حالة الطلب
- `GET /design-requests` - عرض طلبات التصميم
- `PUT /design-requests/{id}` - تحديث طلب التصميم

### الذكاء الاصطناعي (`/api/ai`)
- `POST /generate-design` - توليد تصميم مجوهرات
- `GET /my-designs` - عرض تصاميم المستخدم

---

## ميزة توليد التصاميم بالذكاء الاصطناعي

### المدخلات المطلوبة:
```json
{
    "type": "Ring",           // نوع المجوهرات: Ring, Necklace, Bracelet, Earrings
    "color": "Gold",          // اللون الأساسي
    "shape": "Round",         // الشكل أو النمط
    "material": "Gold",       // المادة: Gold, Silver, Platinum
    "karat": "18k",          // العيار: 18k, 21k, 22k, 24k
    "gemstone_type": "Diamond", // نوع الحجر: Diamond, Ruby, Emerald, Sapphire, None
    "gemstone_color": "White"   // لون الحجر
}
```

### آلية العمل:
1. استقبال البيانات من المستخدم
2. بناء prompt تفصيلي للـ AI
3. استدعاء Google Gemini API (`gemini-3-pro-image-preview`)
4. حفظ الصورة المولدة في `/static/generated_designs/`
5. حفظ السجل في قاعدة البيانات
6. إرجاع رابط الصورة للمستخدم

---

## بيانات التجربة (Seeder)

### المستخدمين (5):
| Username | Password |
|----------|----------|
| admin | admin123 |
| john_doe | password123 |
| jane_smith | password123 |
| mohammed_ali | password123 |
| sarah_wilson | password123 |

### الصائغين (3):
1. Ahmed Goldsmith - Golden Dreams Jewelry (Dubai)
2. Maria Silva - Elegance Jewelers (New York)
3. Omar Hassan - Heritage Gold (Jeddah)

### التصنيفات (مع تصنيفات فرعية):
- Rings (Engagement Rings, Wedding Bands, Fashion Rings)
- Necklaces (Pendants, Chains, Chokers)
- Bracelets

### طرق الدفع (2):
1. Bank Transfer
2. PayPal

### المنتجات (10):
منتجات متنوعة من الخواتم والقلائد والأساور بمختلف الأعيرة والمواد

---

## هيكل المشروع

```
G:\Hamdo\
├── main.py                 # نقطة الدخول
├── config.py               # الإعدادات
├── database.py             # الاتصال بقاعدة البيانات
├── requirements.txt        # المكتبات المطلوبة
├── .env.example            # نموذج المتغيرات البيئية
├── seeder.py               # بيانات تجريبية
├── models/                 # نماذج قاعدة البيانات
├── schemas/                # مخططات Pydantic
├── routers/                # مسارات API
├── utils/                  # وظائف مساعدة
└── static/                 # الملفات الثابتة
    └── generated_designs/  # التصاميم المولدة
```

---

## تعليمات التشغيل

### 1. إعداد XAMPP:
- تشغيل Apache و MySQL
- إنشاء قاعدة بيانات `jewelry_db`

### 2. تثبيت المكتبات:
```bash
pip install -r requirements.txt
```

### 3. إعداد المتغيرات البيئية:
```bash
copy .env.example .env
# تعديل الملف وإضافة GEMINI_API_KEY
```

### 4. تشغيل Seeder:
```bash
python seeder.py
```

### 5. تشغيل الخادم:
```bash
uvicorn main:app --reload
```

### 6. الوصول للتطبيق:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ملاحظات مهمة

1. **CORS مفعّل** - يقبل الطلبات من أي origin للتوافق مع Frontend HTML/CSS/JS
2. **JWT Authentication** - جميع الـ endpoints المحمية تتطلب Header: `Authorization: Bearer <token>`
3. **تشفير كلمات المرور** - باستخدام bcrypt
4. **AI Generation** - يتطلب مفتاح Gemini API صالح

---

## التحديثات المستقبلية المحتملة

- [ ] إضافة نظام صلاحيات للمستخدمين (Admin, User, Jeweler)
- [ ] إضافة نظام التقييمات والمراجعات للمنتجات
- [ ] إضافة نظام الإشعارات
- [ ] دعم رفع الصور للمنتجات
- [ ] إضافة نظام القسائم والخصومات
- [ ] إضافة تقارير وإحصائيات للمدير

---

## سجل التثبيت والتنفيذ

### تم تنفيذ الخطوات التالية بنجاح (2026-02-24):

1. **تثبيت Python 3.12.2** - تم تحميل وتثبيت Python من python.org
2. **إنشاء Virtual Environment** - تم إنشاء بيئة افتراضية في `G:\Hamdo\venv`
3. **تثبيت المكتبات** - تم تثبيت جميع المكتبات من requirements.txt
4. **إنشاء ملف .env** - تم نسخ .env.example إلى .env
5. **إنشاء قاعدة البيانات** - تم إنشاء `jewelry_db` في MySQL
6. **إنشاء الجداول** - تم إنشاء جميع جداول قاعدة البيانات
7. **تعبئة البيانات التجريبية** - تم إضافة:
   - 5 مستخدمين
   - 3 صائغين
   - 9 تصنيفات (مع تصنيفات فرعية)
   - 2 طرق دفع
   - 10 منتجات
8. **تشغيل الخادم** - الخادم يعمل على http://localhost:8000

### اختبارات API الناجحة:
- ✅ `GET /` - رسالة الترحيب
- ✅ `GET /api/products/` - عرض 10 منتجات
- ✅ `POST /api/auth/login` - تسجيل دخول ناجح مع JWT token

### بيانات الدخول:
| Username | Password |
|----------|----------|
| admin | admin123 |
| john_doe | password123 |
| jane_smith | password123 |
| mohammed_ali | password123 |
| sarah_wilson | password123 |

---

*تم إنشاء هذا التقرير تلقائياً بواسطة Kilo AI Assistant*