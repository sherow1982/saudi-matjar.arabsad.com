import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# رابط الفيد أو API من EasyOrders (استبدله برابط الفيد الحقيقي)
EASYORDERS_FEED_URL = "https://saudi-matjar.arabsad.com/products-feed.xml"

# الدومين اللي عايز يظهر في جوجل
GITHUB_DOMAIN = "https://sherow1982.github.io/saudi-matjar.arabsad.com"

# اسم ملف الفيد النهائي
OUTPUT_FILE = "products-feed.xml"

def fetch_easyorders_feed():
    print("جاري جلب البيانات من EasyOrders ...")
    response = requests.get(EASYORDERS_FEED_URL)
    response.raise_for_status()
    return ET.fromstring(response.text)

def rewrite_feed_links(root):
    print("يتم تعديل روابط المنتجات ...")
    for item in root.findall(".//item"):
        link = item.find("link")
        if link is not None and link.text:
            original_link = link.text.strip()
            product_slug = original_link.split("/")[-1]
            # الرابط اللي هيظهر في جوجل (من GitHub)
            link.text = f"{GITHUB_DOMAIN}/products/{product_slug}"
    return root

def save_feed(root):
    print("يتم حفظ الفيد المعدل ...")
    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"تم حفظ الملف بنجاح باسم {OUTPUT_FILE}")

def main():
    root = fetch_easyorders_feed()
    new_root = rewrite_feed_links(root)
    save_feed(new_root)
    print(f"تم إنشاء الفيد بتاريخ {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
