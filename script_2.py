
# Create corrected CSS file
styles_css = """/* General Reset and RTL Support */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #2c7a3e;
    --secondary-color: #1a5a2e;
    --accent-color: #f4a442;
    --text-color: #333;
    --bg-color: #f5f5f5;
    --white: #ffffff;
    --border-radius: 8px;
    --transition: all 0.3s ease;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
    direction: rtl;
    text-align: right;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header Styles */
.header {
    background-color: var(--primary-color);
    color: var(--white);
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.logo h1 {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav ul {
    list-style: none;
    display: flex;
    gap: 2rem;
}

.nav a {
    color: var(--white);
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition);
}

.nav a:hover {
    color: var(--accent-color);
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--white);
    padding: 4rem 0;
    text-align: center;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Categories Section */
.categories {
    padding: 3rem 0;
    background-color: var(--white);
}

.categories h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
    color: var(--primary-color);
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.category-card {
    background: var(--white);
    border: 2px solid var(--bg-color);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: var(--transition);
}

.category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border-color: var(--primary-color);
}

.category-card i {
    font-size: 3rem;
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.category-card h3 {
    font-size: 1.2rem;
    color: var(--text-color);
}

/* Products Section */
.products {
    padding: 3rem 0;
    background-color: var(--bg-color);
}

.products h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
    color: var(--primary-color);
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.product-card {
    background: var(--white);
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: var(--transition);
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.product-image {
    width: 100%;
    height: 250px;
    object-fit: cover;
    background-color: var(--bg-color);
}

.product-info {
    padding: 1rem;
}

.product-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-color);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.product-price {
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.product-description {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.product-btn {
    width: 100%;
    padding: 0.75rem;
    background-color: var(--primary-color);
    color: var(--white);
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: var(--transition);
}

.product-btn:hover {
    background-color: var(--secondary-color);
}

/* Loading and Error States */
.loading {
    text-align: center;
    padding: 2rem;
    font-size: 1.2rem;
    color: var(--primary-color);
}

.error-message {
    background-color: #fee;
    border: 1px solid #fcc;
    color: #c33;
    padding: 1rem;
    border-radius: var(--border-radius);
    text-align: center;
    margin: 1rem 0;
}

/* Footer Styles */
.footer {
    background-color: var(--secondary-color);
    color: var(--white);
    padding: 3rem 0 1rem;
}

.footer .container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: var(--accent-color);
}

.footer-links {
    list-style: none;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    color: var(--white);
    text-decoration: none;
    transition: var(--transition);
}

.footer-links a:hover {
    color: var(--accent-color);
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    width: 40px;
    height: 40px;
    background-color: var(--primary-color);
    color: var(--white);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: var(--transition);
    text-decoration: none;
}

.social-links a:hover {
    background-color: var(--accent-color);
    transform: scale(1.1);
}

.whatsapp-btn {
    display: inline-block;
    background-color: #25d366;
    color: var(--white);
    padding: 0.75rem 1.5rem;
    border-radius: var(--border-radius);
    text-decoration: none;
    font-weight: 600;
    transition: var(--transition);
}

.whatsapp-btn:hover {
    background-color: #1da851;
    transform: scale(1.05);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
    .header .container {
        flex-direction: column;
        text-align: center;
    }
    
    .nav ul {
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .hero h2 {
        font-size: 1.8rem;
    }
    
    .products-grid,
    .categories-grid {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 1rem;
    }
}

@media (max-width: 480px) {
    .products-grid,
    .categories-grid {
        grid-template-columns: 1fr;
    }
}"""

with open('/tmp/styles.css', 'w', encoding='utf-8') as f:
    f.write(styles_css)

print("✅ تم إنشاء ملف styles.css المُصحح")
print("=" * 60)
