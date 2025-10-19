#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, sys, requests
from bs4 import BeautifulSoup

BASE = "https://sherow1982.github.io/saudi-matjar.arabsad.com"
# قيمة افتراضية تعمل حتى لو كانت FEED_URL فارغة
EASYORDERS_FEED = os.environ.get("FEED_URL") or "https://api.easy-orders.net/api/v1/products/feed/37ad236e4a0f46e29792dd52978832bc/channel/google"

def make_slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "item"

def text_or_none(tag):
    return tag.get_text(strip=True) if tag else None

def fetch_xml(url: str) -> str:
    print("🔄 fetching feed from EasyOrders ...")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.text

def build_output(items):
    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">')
    parts.append('  <channel>')
    parts.append('    <title><![CDATA[اعلانات العرب شريف سلامة]]></title>')
    parts.append(f'    <link>{BASE}/</link>')
    parts.append('    <description><![CDATA[تغذية المنتجات لمتجر السعودية - اعلانات العرب شريف سلامة]]></description>')
    parts.append('    <language>ar</language>')

    kept = 0
    for it in items:
        gid = it.get("gid")
        title = it.get("title")
        link = it.get("link")  # رابط EasyOrders الأصلي القادم من الفيد المصدر
        price = it.get("price")
        availability = it.get("availability")
        image = it.get("image")
        desc = it.get("description") or title or ""
        brand = it.get("brand") or ""
        condition = it.get("condition") or "new"
        gpc = it.get("google_product_category") or ""
        ptype = it.get("product_type") or ""

        # تحقق من الحقول الأساسية
        if not (title and price and availability and image):
            continue

        slug = make_slug(gid or title or link)
        page_url = f"{BASE}/product/{slug}/"

        parts.append("    <item>")
        parts.append(f"      <g:id>{slug}</g:id>")
        parts.append(f"      <title><![CDATA[{title}]]></title>")
        # نُبقي <link> يشير لصفحة GitHub Pages
        parts.append(f"      <link>{page_url}</link>")
        parts.append(f"      <guid>{slug}</guid>")
        parts.append(f"      <description><![CDATA[{desc}]]></description>")
        parts.append(f"      <g:price>{price}</g:price>")
        parts.append(f"      <g:availability>{availability}</g:availability>")
        parts.append(f"      <g:condition>{condition}</g:condition>")
        parts.append(f"      <g:image_link>{image}</g:image_link>")
        if brand:
            parts.append(f"      <g:brand><![CDATA[{brand}]]></g:brand>")
        if gpc:
            parts.append(f"      <g:google_product_category>{gpc}</g:google_product_category>")
        if ptype:
            parts.append(f"      <g:product_type><![CDATA[{ptype}]]></g:product_type>")
        # نضيف رابط الشراء الأصلي ليستخدمه build_pages.py في زر "اشترِ الآن"
        parts.append(f"      <g:link_source><![CDATA[{link or ''}]]></g:link_source>")
        parts.append("    </item>")
        kept += 1

    parts.append("  </channel>")
    parts.append("</rss>")
    xml = "\n".join(parts)
    return xml, kept

def main():
    try:
        raw = fetch_xml(EASYORDERS_FEED)
    except Exception as e:
        print("❌ failed to fetch feed:", e)
        sys.exit(1)

    soup = BeautifulSoup(raw, "xml")

    # دعم RSS أو Atom
    raw_items = soup.find_all("item")
    if not raw_items:
        raw_items = soup.find_all("entry")

    items = []
    for it in raw_items:
        gid = text_or_none(it.find("g:id") or it.find("id"))
        title = text_or_none(it.find("g:title") or it.find("title"))
        link = text_or_none(it.find("g:link") or it.find("link"))
        price = text_or_none(it.find("g:price") or it.find("price"))
        availability = text_or_none(it.find("g:availability") or it.find("availability"))
        image = text_or_none(it.find("g:image_link") or it.find("image_link") or it.find("image"))
        desc = text_or_none(it.find("g:description") or it.find("description") or it.find("summary"))
        brand = text_or_none(it.find("g:brand") or it.find("brand"))
        condition = text_or_none(it.find("g:condition") or it.find("condition"))
        gpc = text_or_none(it.find("g:google_product_category") or it.find("google_product_category"))
        ptype = text_or_none(it.find("g:product_type") or it.find("product_type"))

        items.append({
            "gid": gid, "title": title, "link": link, "price": price,
            "availability": availability, "image": image, "description": desc,
            "brand": brand, "condition": condition, "google_product_category": gpc,
            "product_type": ptype
        })

    xml, kept = build_output(items)
    with open("products-feed.xml", "w", encoding="utf-8") as f:
        f.write(xml)

    if kept == 0:
        print("⚠️ no valid items kept (missing required fields).")
        sys.exit(1)

    print(f"✅ products-feed.xml written with {kept} items.")

if __name__ == "__main__":
    main()
