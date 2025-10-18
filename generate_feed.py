#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import requests
from typing import Optional, Iterable, Tuple, Dict, List
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

# إعداد namespace لـ Google Merchant
G_NS = "http://base.google.com/ns/1.0"
register_namespace('g', G_NS)  # يضمن xmlns:g في الجذر عند الكتابة [web:26][web:179]

ALLOWED_AVAIL = {"in_stock", "out_of_stock", "preorder", "backorder"}  # [web:80][web:16]

def read_input_xml() -> str:
    # 1) stdin إن كان غير فارغ
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        if data.strip():
            return data
    # 2) ملف محلي
    if os.path.exists("feed.xml"):
        with open("feed.xml", "r", encoding="utf-8") as f:
            return f.read()
    # 3) رابط خارجي
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

def extract_fields(item) -> Dict[str, Optional[str]]:
    # الحقول الشائعة حسب مواصفات Google Merchant [web:80]
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
    }

def normalize_price(val: Optional[str]) -> Optional[str]:
    # يقبل أشكال متعددة ويرجع "123.45 SAR" مثلًا [web:80]
    if not val:
        return None
    s = val.strip()
    # إزالة مسافات زائدة داخل الرقم
    s = re.sub(r"\s+", " ", s)
    # التقاط رقم + عملة
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*([A-Z]{3})$", s)
    if m:
        amount, cur = m.groups()
        return f"{amount} {cur}"
    # لو كانت العملة في البداية "SAR 123.45" اقلب
    m2 = re.match(r"^([A-Z]{3})\s*([0-9]+(?:\.[0-9]+)?)$", s)
    if m2:
        cur, amount = m2.groups()
        return f"{amount} {cur}"
    # إزالة أي محارف غير رقمية ونقطة من الجزء الرقمي ومحاولة توقع SAR كافتراضي
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
    return v if v in ALLOWED_AVAIL else None  # غير المسموح يحذف [web:80]

def generate_google_records(xml_text: str) -> Tuple[List[Dict[str, Optional[str]]], List[str]]:
    soup = BeautifulSoup(xml_text, 'xml')  # parser XML ضروري مع g: [web:6]
    records: List[Dict[str, Optional[str]]] = []
    skipped: List[str] = []

    for idx, item in enumerate(iter_entries(soup), start=1):
        data = extract_fields(item)
        if not data["id"]:
            skipped.append(f"Entry #{idx} skipped: missing id (g:id/id/title/link).")
            continue
        # تحقق من الحقول الضرورية قبل الإضافة: id, title, link, image_link, price, availability [web:80][web:16]
        required_missing = [k for k in ("title", "link", "image_link", "price", "availability") if not data.get(k)]
        if required_missing:
            skipped.append(f"Entry #{idx} skipped: missing required {required_missing}.")
            continue
        records.append(data)

    return records, skipped

def write_google_rss(records: List[Dict[str, Optional[str]]], out_path: str = "products-feed.xml") -> None:
    rss = Element('rss', attrib={"version": "2.0"})
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = "Products Feed"
    SubElement(channel, 'link').text = "https://example.com"
    SubElement(channel, 'description').text = "Auto-generated Google Products Feed"

    for rec in records:
        item = SubElement(channel, 'item')

        def g(tag: str, value: Optional[str]):
            if value:
                SubElement(item, f"{{{G_NS}}}{tag}").text = value  # {ns}tag [web:26][web:179]

        # الحقول المطلوبة
        g('id', rec.get('id'))
        g('title', rec.get('title'))
        g('description', rec.get('description') or rec.get('title'))
        g('link', rec.get('link'))
        g('image_link', rec.get('image_link'))
        g('price', rec.get('price'))
        g('availability', rec.get('availability'))

        # الحقول الاختيارية المفيدة
        g('brand', rec.get('brand'))
        g('condition', rec.get('condition') or "new")

        # RSS القياسية
        if rec.get('link'):
            SubElement(item, 'link').text = rec['link']
        if rec.get('id'):
            SubElement(item, 'guid').text = rec['id']

    tree = ElementTree(rss)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)

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
