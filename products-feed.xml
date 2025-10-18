import requests
import os
import xml.etree.ElementTree as ET

# رابط الفيد من EasyOrders
EASYORDERS_FEED_URL = "https://api.easy-orders.net/api/v1/products/feed/37ad236e4a0f46e29792dd52978832bc/channel/google"

# نطاق الموقع الأساسي (اللي عايز الزوار يتحولوا عليه)
SITE_BASE_URL = "https://saudi-matjar.arabsad.com"

# مجلد صفحات المنتجات
PRODUCTS_DIR = "products"

def fetch_easyorders_feed():
    print("🔄 جاري جلب الفيد من EasyOrders ...")
    response = requests.get(EASYORDERS_FEED_URL)
    response.raise_for_status()
    return ET.fromstring(response.content)

def generate_product_page(product_id, title, description, image, price):
    """ينشئ صفحة HTML بسيطة لكل منتج"""
    os.makedirs(PRODUCTS_DIR, exist_ok=True)
    file_path = os.path.join(PRODUCTS_DIR, f"{product_id}.html")

    html_content = f"""<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
</head>
<body dir="rtl" style="font-family: Arial; margin: 20px;">
<h1>{title}</h1>
<img src="{image}" alt="{title}" style="max-width: 300px; border-radius: 10px;">
<p style="font-size: 18px;">{description}</p>
<p style="font-weight: bold;">السعر: {price}</p>
</body>
</html>"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_google_feed(root):
    """ينشئ ملف XML متوافق مع Google Merchant"""
    rss = ET.Element("rss", version="2.0", attrib={"xmlns:g": "http://base.google.com/ns/1.0"})
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "اعلانات العرب شريف سلامة"
    ET.SubElement(channel, "link").text = SITE_BASE_URL
    ET.SubElement(channel, "description").text = "تغذية المنتجات لمتجر السعودية - اعلانات العرب شريف سلامة"

    for item in root.findall("./channel/item"):
        product_id = item.find("g:id").text.strip()
        title = item.find("title").text.strip()
        description = item.find("description").text.strip()
        price = item.find("g:price").text.strip()
        image = item.find("g:image_link").text.strip()
        brand = item.find("g:brand").text.strip() if item.find("g:brand") is not None else "Brand"
        category = item.find("g:google_product_category").text.strip() if item.find("g:google_product_category") is not None else "0"

        # إنشاء صفحة المنتج
        generate_product_page(product_id, title, description, image, price)

        # بناء عنصر XML جديد
        xml_item = ET.SubElement(channel, "item")
        ET.SubElement(xml_item, "g:id").text = product_id
        ET.SubElement(xml_item, "title").text = title
        ET.SubElement(xml_item, "link").text = f"{SITE_BASE_URL}/product/{product_id}"
        ET.SubElement(xml_item, "description").text = description
        ET.SubElement(xml_item, "g:price").text = price
        ET.SubElement(xml_item, "g:availability").text = "in stock"
        ET.SubElement(xml_item, "g:condition").text = "new"
        ET.SubElement(xml_item, "g:image_link").text = f"{SITE_BASE_URL}/uploads/{os.path.basename(image)}"
        ET.SubElement(xml_item, "g:brand").text = brand
        ET.SubElement(xml_item, "g:google_product_category").text = category

    tree = ET.ElementTree(rss)
    tree.write("products-feed.xml", encoding="utf-8", xml_declaration=True)
    print("✅ تم إنشاء ملف products-feed.xml بنجاح.")

def main():
    root = fetch_easyorders_feed()
    generate_google_feed(root)
    print("🎉 تم تحديث الفيد وإنشاء الصفحات بنجاح.")

if __name__ == "__main__":
    main()
