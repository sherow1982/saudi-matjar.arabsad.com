#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
from bs4 import BeautifulSoup

# مسارات الفيد الممكنة
FEED_PATHS = ["products-feed.xml", "feed.xml"]

# نطاق موقع GitHub Pages
BASE = "https://sherow1982.github.io/saudi-matjar.arabsad.com"


def load_feed():
    for p in FEED_PATHS:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return BeautifulSoup(f.read(), "xml")
    raise SystemExit("لم يتم العثور على products-feed.xml أو feed.xml")


def T(tag):
    return tag.get_text(strip=True) if tag else None


# توحيد الـ slug مع generate_feed.py
def make_slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9\\-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "item"


def price_to_number(price: str) -> str:
    if not price:
        return "0"
    m = re.search(r"([0-9]+(?:\\.[0-9]+)?)", price)
    return m.group(1) if m else "0"


def availability_schema(av: str) -> str:
    m = {
        "in_stock": "https://schema.org/InStock",
        "out_of_stock": "https://schema.org/OutOfStock",
        "preorder": "https://schema.org/PreOrder",
        "backorder": "https://schema.org/BackOrder",
    }
    import json as _json
    return _json.dumps(m.get((av or "").strip().lower(), "https://schema.org/InStock"))


def to_json_val(s: str) -> str:
    import json as _json
    return _json.dumps(s or "")


def render_template(tpl_path: str, ctx: dict) -> str:
    with open(tpl_path, "r", encoding="utf-8") as f:
        html = f.read()
    for k, v in ctx.items():
        html = html.replace("{{ " + k + " }}", v)
    return html


def main():
    soup = load_feed()
    items = soup.find_all("item")
    if not items:
        raise SystemExit("لا توجد عناصر <item> في الفيد")

    os.makedirs("product", exist_ok=True)

    count = 0
    for it in items:
        pid = T(it.find("g:id")) or T(it.find("id")) or ""
        title = T(it.find("title")) or pid or "Product"
        desc = T(it.find("description")) or title
        price = T(it.find("g:price")) or ""
        avail = T(it.find("g:availability")) or ""
        cond = T(it.find("g:condition")) or "new"
        brand = T(it.find("g:brand")) or ""
        img = T(it.find("g:image_link")) or ""

        # رابط الشراء الأصلي من الفيد:
        # الأولوية لحقل g:link_source إن أضفته في generate_feed.py، ثم <link> كبديل.
        buy_src = T(it.find("g:link_source"))
        link = T(it.find("link"))
        slug = make_slug(pid or title or link)
        page_url = f"{BASE}/product/{slug}/"
        buy_url = buy_src or link or page_url  # احتياطيًا صفحة GitHub إن لم يوجد رابط أصلي

        # تحضير سياق القالب
        ctx = {
            "title": title,
            "description": desc,
            "price": price,
            "availability": (avail or "").replace("_", " "),
            "condition": cond,
            "brand": brand,
            "image_link": img,

            # زر الشراء يذهب للمتجر الأصلي
            "buy_url": buy_url,

            # JSON-LD
            "title_json": to_json_val(title),
            "description_json": to_json_val(desc),
            "brand_json": to_json_val(brand),
            "image_json": to_json_val(img),
            "link_json": to_json_val(page_url),
            "price_number": to_json_val(price_to_number(price)),
            "availability_schema": availability_schema(avail),
        }

        html = render_template("templates/product.html", ctx)

        out_dir = os.path.join("product", slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        count += 1

    print(f"تم إنشاء صفحات منتجات بعدد: {count}")


if __name__ == "__main__":
    main()
