import requests
import xml.etree.ElementTree as ET

# رابط الفيد الحقيقي من EasyOrders
EASYORDERS_FEED_URL = "https://api.easy-orders.net/api/v1/products/feed/37ad236e4a0f46e29792dd52978832bc/channel/google"

# دومين GitHub Pages اللي هيظهر في Google Merchant
GITHUB_PAGES_BASE = "https://sherow1982.github.io/saudi-matjar.arabsad.com"

OUTPUT_FILE = "products-feed.xml"


def fetch_easyorders_feed():
    print("Fetching EasyOrders feed...")
    response = requests.get(EASYORDERS_FEED_URL)
    response.raise_for_status()
    return ET.fromstring(response.content)


def transform_links(root):
    """يعدل روابط المنتجات والصور لتشير إلى GitHub Pages بدل EasyOrders"""
    for item in root.findall(".//item"):
        link = item.find("link")
        image_link = item.find("{http://base.google.com/ns/1.0}image_link")

        if link is not None and link.text:
            product_path = link.text.split("/products/")[-1]
            link.text = f"{GITHUB_PAGES_BASE}/products/{product_path}"

        if image_link is not None and image_link.text:
            image_path = image_link.text.split("/")[-1]
            image_link.text = f"{GITHUB_PAGES_BASE}/uploads/{image_path}"


def save_feed(root):
    print("Saving updated feed...")
    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)


def main():
    root = fetch_easyorders_feed()
    transform_links(root)
    save_feed(root)
    print("✅ Feed updated successfully and saved as products-feed.xml")


if __name__ == "__main__":
    main()
