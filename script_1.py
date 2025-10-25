
# Create corrected index.html
index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="متجر تاجر السعودية - أفضل العروض والمنتجات">
    <meta name="keywords" content="متجر, السعودية, تسوق, منتجات">
    <title>متجر تاجر السعودية</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Header Section -->
    <header class="header">
        <div class="container">
            <div class="logo">
                <h1>متجر تاجر السعودية</h1>
            </div>
            <nav class="nav">
                <ul>
                    <li><a href="#home">الرئيسية</a></li>
                    <li><a href="#categories">الفئات</a></li>
                    <li><a href="#about">من نحن</a></li>
                    <li><a href="#contact">اتصل بنا</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h2>مرحباً بك في متجر تاجر السعودية</h2>
            <p>أفضل العروض والمنتجات بأسعار تنافسية</p>
        </div>
    </section>

    <!-- Categories Section -->
    <section id="categories" class="categories">
        <div class="container">
            <h2>تسوق حسب الفئات</h2>
            <div id="categoriesContainer" class="categories-grid">
                <div class="loading">جارٍ تحميل الفئات...</div>
            </div>
        </div>
    </section>

    <!-- Products Section -->
    <section id="products" class="products">
        <div class="container">
            <h2>المنتجات المميزة</h2>
            <div id="productsContainer" class="products-grid">
                <div class="loading">جارٍ تحميل المنتجات...</div>
            </div>
            <div id="errorMessage" class="error-message" style="display: none;"></div>
        </div>
    </section>

    <!-- Footer Links -->
    <footer class="footer">
        <div class="container">
            <div class="footer-section">
                <h3>روابط مهمة</h3>
                <ul class="footer-links">
                    <li><a href="#shipping">سياسة الشحن</a></li>
                    <li><a href="#about">من نحن</a></li>
                    <li><a href="#terms">شروط الاستخدام</a></li>
                    <li><a href="#privacy">سياسات الخصوصية</a></li>
                    <li><a href="#return">سياسة الاستبدال والاسترجاع</a></li>
                    <li><a href="#contact">اتصل بنا</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>صفحات التواصل الاجتماعي</h3>
                <div class="social-links">
                    <a href="#" aria-label="Facebook"><i class="fab fa-facebook"></i></a>
                    <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                    <a href="#" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                </div>
            </div>
            <div class="footer-section">
                <h3>تواصل معنا</h3>
                <a href="https://wa.me/966500000000" class="whatsapp-btn" target="_blank">
                    <i class="fab fa-whatsapp"></i> راسلنا واتساب الآن
                </a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 متجر تاجر السعودية. جميع الحقوق محفوظة.</p>
        </div>
    </footer>

    <!-- Config and Scripts -->
    <script src="config.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

# Save index.html
with open('/tmp/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("✅ تم إنشاء ملف index.html المُصحح")
print("=" * 60)
