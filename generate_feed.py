#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import requests
from typing import Optional, Iterable, Tuple, Dict, List
from bs4 import BeautifulSoup
from lxml import etree  # استخدام lxml لتسهيل CDATA [web:245]

G_NS = "http://base.google.com/ns/1.0"
NSMAP = {"g": G_NS}
ALLOWED_AVAIL = {"in_stock", "out_of_stock", "preorder", "backorder"}  # [web:80][web:16]

def read_input_xml() -> str:
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        if data.strip():
            return data
    if os.path.exists("feed.xml"):
        with open("feed.xml", "r", encoding="utf-8") as f:
            return f.read()
    feed_url = os.getenv("FEED_URL")
    if feed_url:
        resp = requests.get(feed_url, timeout=30)
        resp.raise_for_status()
        return resp.text
    raise RuntimeError("لم يتم العثور على مدخل XML. مرّر البيانات عبر stdin أو ضع feed.xml أو اضبط FEED_URL.")

def text_or_none(tag) -> Optional[str]:
    return tag.get_text(strip=True) if tag and hasattr(tag, "get_text") else None

def first_text(*candidates) -> Optional[str]:
    for t in candidates:
        if t:
            return t
    return None

def iter_entries(soup: BeautifulSoup) -> Iterable:
    items = soup.find_all('item')
    if items:
        return items
    return soup.find_all('entry')

def normalize_price(val: Optional[str]) -> Optional[str]:
    if not val:
        return None
    s = re.sub(r"\s+", " ", val.strip())
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*([A-Z]{3})$", s)
    if m:
        amount, cur = m.groups()
        return f"{amount} {cur}"
    m2 = re.match(r"^([A-Z]{3})\s*([0-9]+(?:\.[0-9]+)?)$", s)
    if m2:
        cur, amount = m2.groups()
        return f"{amount} {cur}"
    digits = re.findall(r"[0-9]+(?:\.[0-9]+)?", s)
    cur = re.findall(r"[A-Z]{3}", s)
    if digits:
        amount = digits[0]
        currency = cur[0] if cur else "SAR"
        return f"{amount} {currency}"
    return None

def normalize_availability(val: Optional[str]) -> Optional[str]:
    if not val:
        return None
    v = val.strip().lower().replace(" ", "_")
    return v if v in ALLOWED_AVAIL else None  # [web:80]

def extract_fields(item) -> Dict[str, Optional[str]]:
    gid = item.find('g:id')
    plain_id = item.find('id')
    title = item.find('g:title') or item.find('title')
    link = item.find('g:link') or item.find('link')
    price = item.find('g:price') or item.find('price')
    availability = item.find('g:availability') or item.find('availability')
    image_link = item.find('g:image_link') or item.find('image_link') or item.find('image') or item.find('enclosure')
    description = item.find('g:description') or item.find('description') or item.find('summary')
    brand = item.find('g:brand') or item.find('brand')
    condition = item.find('g:condition') or item.find('condition')
    product_type = item.find('g:product_type') or item.find('product_type')
    google_cat = item.find('g:google_product_category') or item.find('google_product_category')

    product_id = first_text(
        text_or_none(gid),
        text_or_none(plain_id),
        text_or_none(title),
        text_or_none(link),
    )

    return {
        "id": product_id,
        "title": text_or_none(title),
        "link": text_or_none(link),
        "price": normalize_price(text_or_none(price)),
        "availability": normalize_availability(text_or_none(availability)),
        "image_link": text_or_none(image_link),
        "description": text_or_none(description),
        "brand": text_or_none(brand),
        "condition": text_or_none(condition),
        "product_type": text_or_none(product_type),
        "google_product_category": text_or_none(google_cat),
    }

def generate_google_records(xml_text: str) -> Tuple[List[Dict[str, Optional[str]]], List[str]]:
    soup = BeautifulSoup(xml_text, 'xml')  # parser=xml مع g: [web:16]
    records: List[Dict[str, Optional[str]]] = []
    skipped: List[str] = []

    for idx, item in enumerate(iter_entries(soup), start=1):
        data = extract_fields(item)
        if not data["id"]:
            skipped.append(f"Entry #{idx} skipped: missing id (g:id/id/title/link).")
            continue
        required_missing = [k for k in ("title", "link", "image_link", "price", "availability") if not data.get(k)]
        if required_missing:
            skipped.append(f"Entry #{idx} skipped: missing required {required_missing}.")
            continue
        records.append(data)

    return records, skipped

def write_google_rss(records: List[Dict[str, Optional[str]]], out_path: str = "products-feed.xml") -> None:
    # بناء الجذر مع NSMAP لضمان xmlns:g
    rss = etree.Element("rss", nsmap=NSMAP)
    rss.set("version", "2.0")
    channel = etree.SubElement(rss, "channel")

    # عناوين القناة مع CDATA
    title_el = etree.SubElement(channel, "title")
    title_el.text = etree.CDATA("Products Feed")  # يمكنك تخصيصه
    link_el = etree.SubElement(channel, "link")
    link_el.text = "https://example.com"
    desc_el = etree.SubElement(channel, "description")
    desc_el.text = etree.CDATA("Auto-generated Google Products Feed")

    for rec in records:
        item = etree.SubElement(channel, "item")

        def g(tag: str, value: Optional[str], cdata: bool = False):
            if value is None:
                return
            el = etree.SubElement(item, f"{{{G_NS}}}{tag}")
            el.text = etree.CDATA(value) if cdata else value

        # الحقول المطلوبة (استخدم CDATA للنصوص)
        g("id", rec.get("id"))
        t = etree.SubElement(item, "title"); t.text = etree.CDATA(rec["title"])  # RSS title [web:16]
        l = etree.SubElement(item, "link"); l.text = rec["link"]
        d = etree.SubElement(item, "description"); d.text = etree.CDATA(rec.get("description") or rec["title"])
        g("link", rec.get("link"))
        g("image_link", rec.get("image_link"))
        g("price", rec.get("price"))
        g("availability", rec.get("availability"))

        # الحقول الاختيارية
        g("brand", rec.get("brand"), cdata=True)
        g("condition", rec.get("condition") or "new")
        g("product_type", rec.get("product_type"), cdata=True)
        g("google_product_category", rec.get("google_product_category"))

        # RSS القياسية
        guid = etree.SubElement(item, "guid"); guid.text = rec["id"]

    # كتابة الملف
    tree = etree.ElementTree(rss)
    tree.write(out_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)

def main():
    print("🔄 جاري جلب ومعالجة الفيد ...")
    xml_input = read_input_xml()
    records, skipped = generate_google_records(xml_input)

    print(f"✅ العناصر المعالجة: {len(records)}")
    print(f"⚠️ العناصر المتخطاة: {len(skipped)}")
    for msg in skipped[:20]:
        print(" -", msg)

    write_google_rss(records, "products-feed.xml")
    print("📝 تم إنشاء الملف: products-feed.xml")

if __name__ == "__main__":
    main()
