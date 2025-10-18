import requests
from bs4 import BeautifulSoup
import re

FEED_URL = "https://api.easy-orders.net/api/v1/products/feed/437a38bb829245a3934e1d2fe153b417/channel/google"
OUTPUT_FILE = "products-feed.xml"

def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text

def generate_feed():
    print("Fetching EasyOrders feed...")
    response = requests.get(FEED_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")

    print(f"Fetched {len(items)} products. Generating new feed...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n')
        f.write("  <channel>\n")
        f.write("    <title>منتجات تاجر السعودية</title>\n")
        f.write("    <link>https://sherow1982.github.io/saudi-matjar.arabsad.com/</link>\n")
        f.write("    <description>تغذية منتجات تاجر السعودية - موقع اعلانات العرب شريف سلامة</description>\n\n")

        for item in items:
            title = item.find("title").text if item.find("title") else ""
            image = item.find("g:image_link").text if item.find("g:image_link") else ""
            price = item.find("g:price").text if item.find("g:price") else ""
            desc = item.find("description").text if item.find("description") else ""

            # إنشاء رابط نظيف لكل منتج باسم المنتج
            title_slug = slugify(title)
            link = f"https://sherow1982.github.io/saudi-matjar.arabsad.com/products/{title_slug}"

            f.write("    <item>\n")
            f.write(f"      <title>{title}</title>\n")
            f.write(f"      <link>{link}</link>\n")
            f.write(f"      <g:image_link>{image}</g:image_link>\n")
            f.write(f"      <description>{desc}</description>\n")
            f.write(f"      <g:price>{price}</g:price>\n")
            f.write("      <g:availability>in stock</g:availability>\n")
            f.write("      <g:condition>new</g:condition>\n")
            f.write("    </item>\n")

        f.write("  </channel>\n</rss>\n")

    print("✅ products-feed.xml generated successfully!")

if __name__ == "__main__":
    generate_feed()

