#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, json, requests
from bs4 import BeautifulSoup

FEED_URL = os.environ.get("FEED_URL")
SITE_BASE = os.environ.get("SITE_BASE")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def make_slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9\\-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "item"

def ai_shorten_desc(title, desc):
    if not OPENAI_API_KEY:
        return (desc or title or "")[:280]
    # مبدئي: اختصر النص محليًا بدون استدعاء API إن لم يتوفر
    return (desc or title or "")[:280]

def fetch_xml(url: str) -> str:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.text

def parse_items(xml_text: str):
    soup = BeautifulSoup(xml_text, "xml")
    items = soup.find_all("item") or soup.find_all("entry")
    out=[]
    for it in items:
        gid = (it.find("g:id") or it.find("id"))
        title = (it.find("g:title") or it.find("title"))
        link = (it.find("g:link") or it.find("link"))
        price = (it.find("g:price") or it.find("price"))
        availability = (it.find("g:availability") or it.find("availability"))
        image = (it.find("g:image_link") or it.find("image_link") or it.find("image"))
        desc = (it.find("g:description") or it.find("description") or it.find("summary"))
        brand = (it.find("g:brand") or it.find("brand"))
        condition = (it.find("g:condition") or it.find("condition"))
        gpc = (it.find("g:google_product_category") or it.find("google_product_category"))
        ptype = (it.find("g:product_type") or it.find("product_type"))

        def T(tag): return tag.get_text(strip=True) if tag else None

        out.append({
            "gid": T(gid), "title": T(title), "link": T(link), "price": T(price),
            "availability": T(availability), "image": T(image), "description": T(desc),
            "brand": T(brand), "condition": T(condition), "google_product_category": T(gpc),
            "product_type": T(ptype)
        })
    return out

def build_feed_and_pages(items):
    os.makedirs("product", exist_ok=True)

    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">')
    parts.append('  <channel>')
    parts.append('    <title><![CDATA[اعلانات العرب شريف سلامة]]></title>')
    parts.append(f'    <link>{SITE_BASE}/</link>')
    parts.append('    <description><![CDATA[تغذية المنتجات لمتجر السعودية - اعلانات العرب شريف سلامة]]></description>')
    parts.append('    <language>ar</language>')

    kept=0
    for it in items:
        title=it.get("title")
        price=it.get("price")
        availability=it.get("availability")
        image=it.get("image")
        desc=it.get("description") or ""
        brand=it.get("brand") or ""
        condition=it.get("condition") or "new"
        gpc=it.get("google_product_category") or ""
        ptype=it.get("product_type") or ""

        if not (title and price and availability and image):
            continue

        slug = make_slug(it.get("gid") or title or it.get("link"))
        page_url = f"{SITE_BASE}/product/{slug}/"

        # وصف مختصر محسّن
        desc = ai_shorten_desc(title, desc)

        # اكتب عنصر الفيد
        parts.append("    <item>")
        parts.append(f"      <g:id>{slug}</g:id>")
        parts.append(f"      <title><![CDATA[{title}]]></title>")
        parts.append(f"      <link>{page_url}</link>")
        parts.append(f"      <guid>{slug}</guid>")
        parts.append(f"      <description><![CDATA[{desc}]]></description>")
        parts.append(f"      <g:price>{price}</g:price>")
        parts.append(f"      <g:availability>{availability}</g:availability>")
        parts.append(f"      <g:condition>{condition}</g:condition>")
        parts.append(f"      <g:image_link>{image}</g:image_link>")
        if brand: parts.append(f"      <g:brand><![CDATA[{brand}]]></g:brand>")
        if gpc: parts.append(f"      <g:google_product_category>{gpc}</g:google_product_category>")
        if ptype: parts.append(f"      <g:product_type><![CDATA[{ptype}]]></g:product_type>")
        parts.append("    </item>")

        # ابنِ صفحة المنتج البسيطة
        out_dir=f"product/{slug}"
        os.makedirs(out_dir, exist_ok=True)
        with open(f"{out_dir}/index.html","w",encoding="utf-8") as f:
            f.write(f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<title>{title} | متجر السعودية</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<link rel="canonical" href="{page_url}">
<style>body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:24px;background:#fafafa;color:#222}}
.wrap{{max-width:900px;margin:0 auto}}
img{{max-width:420px;height:auto;border-radius:8px;border:1px solid #eee;background:#fff}}
.price{{font-size:1.4rem;color:#0b8457;margin:8px 0}}</style>
</head><body><div class="wrap">
<h1>{title}</h1>
<img src="{image}" alt="{title}">
<p class="price">{price}</p>
<p>{desc}</p>
<p>التوفر: {availability} — الحالة: {condition} — العلامة: {brand}</p>
<p><a href="{page_url}">الرابط الدائم</a></p>
</div></body></html>""")
        kept+=1

    parts.append("  </channel>")
    parts.append("</rss>")

    with open("products-feed.xml","w",encoding="utf-8") as f:
        f.write("\n".join(parts))

    return kept

def main():
    xml = fetch_xml(FEED_URL)
    items = parse_items(xml)
    kept = build_feed_and_pages(items)
    print(f"✅ Wrote products-feed.xml and {kept} product pages.")

if __name__ == "__main__":
    main()
