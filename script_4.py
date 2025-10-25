
# Create script.js file
script_js = """// Main JavaScript File for Saudi Store
// الملف الرئيسي لجافاسكريبت لمتجر السعودية

// Global Variables
let productsData = [];
let categoriesData = [];
let currentCategory = 'all';

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('تم تحميل الصفحة بنجاح');
    initializeApp();
});

// Initialize Application
async function initializeApp() {
    try {
        // Load categories
        await loadCategories();
        
        // Load products
        await loadProducts();
        
        // Setup event listeners
        setupEventListeners();
        
    } catch (error) {
        console.error('خطأ في تهيئة التطبيق:', error);
        showError('حدث خطأ في تحميل البيانات. يرجى المحاولة لاحقاً.');
    }
}

// Load Categories
async function loadCategories() {
    const categoriesContainer = document.getElementById('categoriesContainer');
    
    try {
        if (CONFIG.USE_DEMO_DATA) {
            // Use demo data
            categoriesData = CONFIG.DEMO_CATEGORIES;
        } else {
            // Fetch from API
            const response = await fetch(`${CONFIG.API_URL}/categories`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${CONFIG.API_KEY}`
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            categoriesData = await response.json();
        }
        
        // Display categories
        displayCategories(categoriesData);
        
    } catch (error) {
        console.error('خطأ في تحميل الفئات:', error);
        categoriesContainer.innerHTML = '<p class="error-message">فشل تحميل الفئات</p>';
    }
}

// Display Categories
function displayCategories(categories) {
    const categoriesContainer = document.getElementById('categoriesContainer');
    
    if (!categories || categories.length === 0) {
        categoriesContainer.innerHTML = '<p>لا توجد فئات متاحة</p>';
        return;
    }
    
    categoriesContainer.innerHTML = categories.map(category => `
        <div class="category-card" onclick="filterByCategory('${category.name}')" data-category="${category.name}">
            <i class="fas ${category.icon}"></i>
            <h3>${category.name}</h3>
        </div>
    `).join('');
}

// Load Products
async function loadProducts() {
    const productsContainer = document.getElementById('productsContainer');
    const errorMessage = document.getElementById('errorMessage');
    
    try {
        if (CONFIG.USE_DEMO_DATA) {
            // Use demo data
            productsData = CONFIG.DEMO_PRODUCTS;
        } else {
            // Fetch from API
            const response = await fetch(CONFIG.API_URL, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${CONFIG.API_KEY}`
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            productsData = await response.json();
        }
        
        // Display products
        displayProducts(productsData);
        
        // Hide error message if visible
        errorMessage.style.display = 'none';
        
    } catch (error) {
        console.error('خطأ في تحميل المنتجات:', error);
        productsContainer.innerHTML = '';
        showError('فشل تحميل المنتجات. يرجى التحقق من اتصال الإنترنت والمحاولة مرة أخرى.');
    }
}

// Display Products
function displayProducts(products) {
    const productsContainer = document.getElementById('productsContainer');
    
    if (!products || products.length === 0) {
        productsContainer.innerHTML = '<p class="error-message">لا توجد منتجات متاحة</p>';
        return;
    }
    
    productsContainer.innerHTML = products.map(product => `
        <div class="product-card" data-id="${product.id}">
            <img src="${product.image}" alt="${product.title}" class="product-image" 
                 onerror="this.src='https://via.placeholder.com/300x300?text=No+Image'">
            <div class="product-info">
                <h3 class="product-title">${product.title}</h3>
                <p class="product-price">${product.price} ${CONFIG.CURRENCY}</p>
                <p class="product-description">${product.description || 'لا يوجد وصف'}</p>
                <button class="product-btn" onclick="orderProduct(${product.id})">
                    <i class="fab fa-whatsapp"></i> اطلب عبر واتساب
                </button>
            </div>
        </div>
    `).join('');
}

// Filter Products by Category
function filterByCategory(category) {
    currentCategory = category;
    
    if (category === 'all') {
        displayProducts(productsData);
    } else {
        const filteredProducts = productsData.filter(product => 
            product.category === category
        );
        displayProducts(filteredProducts);
    }
    
    // Update active category styling
    document.querySelectorAll('.category-card').forEach(card => {
        card.classList.remove('active');
    });
    
    const activeCard = document.querySelector(`[data-category="${category}"]`);
    if (activeCard) {
        activeCard.classList.add('active');
    }
}

// Order Product via WhatsApp
function orderProduct(productId) {
    const product = productsData.find(p => p.id === productId);
    
    if (!product) {
        alert('المنتج غير موجود');
        return;
    }
    
    const message = `مرحباً، أود الاستفسار عن المنتج التالي:\n\n` +
                   `المنتج: ${product.title}\n` +
                   `السعر: ${product.price} ${CONFIG.CURRENCY}\n\n` +
                   `يرجى التواصل معي للمزيد من التفاصيل.`;
    
    const whatsappUrl = `https://wa.me/${CONFIG.WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

// Show Error Message
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Search Products (if needed in future)
function searchProducts(query) {
    const filteredProducts = productsData.filter(product =>
        product.title.toLowerCase().includes(query.toLowerCase()) ||
        (product.description && product.description.toLowerCase().includes(query.toLowerCase()))
    );
    displayProducts(filteredProducts);
}

// Refresh Products
function refreshProducts() {
    loadProducts();
}

// Console log for debugging
console.log('السكريبت تم تحميله بنجاح');
console.log('استخدام البيانات التجريبية:', CONFIG.USE_DEMO_DATA);"""

with open('/tmp/script.js', 'w', encoding='utf-8') as f:
    f.write(script_js)

print("✅ تم إنشاء ملف script.js المُصحح")
print("=" * 60)
