
# Create config.js file
config_js = """// Configuration File for Saudi Store
// ملف الإعدادات لمتجر السعودية

const CONFIG = {
    // API Configuration
    API_URL: 'https://api.example.com/products', // غيّر هذا الرابط إلى API الخاص بك
    API_KEY: '', // ضع مفتاح API هنا إن وُجد
    
    // Store Settings
    STORE_NAME: 'متجر تاجر السعودية',
    CURRENCY: 'ر.س',
    LANGUAGE: 'ar',
    
    // WhatsApp Configuration
    WHATSAPP_NUMBER: '966500000000', // غيّر هذا الرقم إلى رقمك
    
    // Pagination
    PRODUCTS_PER_PAGE: 12,
    
    // Cache Settings
    CACHE_DURATION: 300000, // 5 minutes in milliseconds
    
    // Demo Mode - استخدم هذا إذا لم يكن لديك API
    USE_DEMO_DATA: true, // غيّرها إلى false عند استخدام API حقيقي
    
    // Demo Products Data
    DEMO_PRODUCTS: [
        {
            id: 1,
            title: 'منتج تجريبي 1',
            price: 99.99,
            description: 'وصف المنتج التجريبي الأول',
            image: 'https://via.placeholder.com/300x300?text=Product+1',
            category: 'إلكترونيات'
        },
        {
            id: 2,
            title: 'منتج تجريبي 2',
            price: 149.99,
            description: 'وصف المنتج التجريبي الثاني',
            image: 'https://via.placeholder.com/300x300?text=Product+2',
            category: 'أزياء'
        },
        {
            id: 3,
            title: 'منتج تجريبي 3',
            price: 79.99,
            description: 'وصف المنتج التجريبي الثالث',
            image: 'https://via.placeholder.com/300x300?text=Product+3',
            category: 'منزل'
        },
        {
            id: 4,
            title: 'منتج تجريبي 4',
            price: 199.99,
            description: 'وصف المنتج التجريبي الرابع',
            image: 'https://via.placeholder.com/300x300?text=Product+4',
            category: 'إلكترونيات'
        },
        {
            id: 5,
            title: 'منتج تجريبي 5',
            price: 59.99,
            description: 'وصف المنتج التجريبي الخامس',
            image: 'https://via.placeholder.com/300x300?text=Product+5',
            category: 'رياضة'
        },
        {
            id: 6,
            title: 'منتج تجريبي 6',
            price: 129.99,
            description: 'وصف المنتج التجريبي السادس',
            image: 'https://via.placeholder.com/300x300?text=Product+6',
            category: 'أزياء'
        }
    ],
    
    // Demo Categories
    DEMO_CATEGORIES: [
        { id: 1, name: 'إلكترونيات', icon: 'fa-laptop' },
        { id: 2, name: 'أزياء', icon: 'fa-shirt' },
        { id: 3, name: 'منزل', icon: 'fa-house' },
        { id: 4, name: 'رياضة', icon: 'fa-dumbbell' },
        { id: 5, name: 'كتب', icon: 'fa-book' },
        { id: 6, name: 'ألعاب', icon: 'fa-gamepad' }
    ]
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}"""

with open('/tmp/config.js', 'w', encoding='utf-8') as f:
    f.write(config_js)

print("✅ تم إنشاء ملف config.js المُصحح")
print("=" * 60)
