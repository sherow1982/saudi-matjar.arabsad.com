import requests

# رابط الفيد من EasyOrders
EASYORDERS_FEED = "https://saudi-matjar.arabsad.com/products-feed.xml"

# المكان اللي هيتحفظ فيه الفيد داخل الريبو
OUTPUT_FILE = "products-feed.xml"

response = requests.get(EASYORDERS_FEED)
response.raise_for_status()

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(response.text)

print("✅ Feed updated successfully!")
