#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, json
from bs4 import BeautifulSoup

# المسارات الممكنة لملف الفيد
FEED_PATHS = ["products-feed.xml", "feed.xml"]

# النطاق الأساسي لروابط الصفحات
BASE = "https://sherow1982.github.io/saudi-matjar.arabsad.com"

def load_feed() -> BeautifulSoup:
    for p in FEED_PATHS:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return BeautifulSoup(f.read(), "xml")
    raise SystemExit("لم يتم العثور على products-feed.xml أو feed.xml")

def get_text(tag):
    return tag.get_text(strip=True) if tag else None

def price_to_number(price: str) -> str:
    # يحوّل "123.45 SAR" إلى "123.45" للـ JSON-LD
    if not price: return "0"
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)", price)
    return m.group(1) if m else "0"

def availability_schema(av: str) -> str:
    mapping = {
        "in_stock": "https://schema.org/InStock",
        "out_of_stock": "https://schema.org/OutOfStock",
        "preorder": "https://schema.org/PreOrder",
        "backorder": "https://schema.org/BackOrder",
    }
    return json.dumps(mapping.get((av or "").strip().lower(), "https://schema.org/InStock"))

def to_json_val(s: str) -> str:
    # يضمن الاقتباس الصحيح داخل JSON-LD
    return json.dumps(s or "")

def render_template(tpl_path: str, ctx: dict) -> str:
    with open(tpl_path, "r", encoding="utf-8") as f:
        html = f.read()
    # استبدال بسيط للوسوم {{ var }} دون اعتماديات إضافية
    for k, v in ctx.items():
        html = html.replace("{{ " + k + " }}", v)
    return html

def make_slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "item"

def main():
    soup = load_feed()
    items = soup.find_all("item")
    if not items:
        raise SystemExit("لا توجد عناصر <item> في الفيد")

    os.makedirs("product", exist_ok=True)

    for it in items:
        pid = get_text(it.find("g:id"))
        title = get_text(it.find("title"))
        link = get_text(it.find("link"))  # رابط خارجي أو نفس صفحة GitHub
        desc = get_text(it.find("description"))
        price = get_text(it.find("g:price"))
        avail = get_text(it.find("g:availability"))
        cond = get_text(it.find("g:condition")) or "new"
        brand = get_text(it.find("g:brand")) or ""
        img = get_text(it.find("g:image_link"))

        slug = make_slug(pid or title or "item")
        page_url = f"{BASE}/product/{slug}/"

        ctx = {
            # قيم HTML
            "title": title or pid or "Product",
            "description": desc or (title or ""),
            "price": price or "",
            "availability": (avail or "").replace("_", " "),
            "condition": cond,
            "brand": brand or "",
            "image_link": img or "",
            "link": link or page_url,  # يمكن تعيينه إلى page_url لعرض نفس الصفحة

            # قيم JSON-LD (مشفرة JSON)
            "title_json": to_json_val(title or pid or ""),
            "description_json": to_json_val(desc or ""),
            "brand_json": to_json_val(brand or ""),
            "image_json": to_json_val(img or ""),
            "link_json": to_json_val(page_url),
            "price_number": to_json_val(price_to_number(price or "")),
            "availability_schema": availability_schema(avail or ""),
        }

        html = render_template("templates/product.html", ctx)
        out_dir = os.path.join("product", slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

    print(f"تم إنشاء صفحات منتجات بعدد: {len(items)}")

if __name__ == "__main__":
    main()
