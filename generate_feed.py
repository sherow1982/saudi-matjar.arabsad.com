#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
from typing import Optional, Iterable, Tuple, Dict, List
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

# إعداد namespace لـ Google Merchant
G_NS = "http://base.google.com/ns/1.0"
register_namespace('g', G_NS)  # يضمن xmlns:g في الجذر عند الكتابة [web:26][web:70]

def read_input_xml() -> str:
    # 1) إن وُجد stdin غير فارغ
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        if data.strip():
            return data

    # 2) إن وُجد ملف feed.xml محلي
    if os.path.exists("feed.xml"):
        with open("feed.xml", "r", encoding="utf-8") as f:
            return f.read()

    # 3) إن وُجد رابط عبر متغير بيئي
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
    # يدعم RSS (item) و Atom (entry)
    items = soup.find_all('item')
    if items:
        return items
    return soup.find_all('entry')

def extract_fields(item) -> Dict[str, Optional[str]]:
    # حقول Google أولاً ثم بدائل عامة [web:10][web:31]
    gid = item.find('g:id')
    plain_id = item.find('id')
    title = item.find('g:title') or item.find('title')
    link = item.find('g:link') or item.find('link')
    price = item.find('g:price') or item.find('price')
    availability = item.find('g:availability') or item.find('availability')
    image_link = item.find('g:image_link') or item.find('image_link') or item.find('image') or item.find('enclosure')
    description = item.find('g:description') or item.find('description') or item.find('summary')

    product_id = first_text(
        text_or_none(gid),
        text_or_none(plain_id),
        # fallback مستمد من عنوان/رابط إن اضطررنا
        text_or_none(title),
        text_or_none(link),
    )

    return {
        "id": product_id,
        "title": text_or_none(title),
        "link": text_or_none(link),
        "price": text_or_none(price),
        "availability": text_or_none(availability),
        "image_link": text_or_none(image_link),
        "description": text_or_none(description),
    }

def generate_google_records(xml_text: str) -> Tuple[List[Dict[str, Optional[str]]], List[str]]:
    """
    يعيد (records, skipped):
    - records: عناصر صالحة تم استخراجها
    - skipped: أسباب التخطي لكل عنصر بلا id
    """
    soup = BeautifulSoup(xml_text, 'xml')  # ضروري لاسماء مثل g:id [web:6]
    records: List[Dict[str, Optional[str]]] = []
    skipped: List[str] = []

    for idx, item in enumerate(iter_entries(soup), start=1):
        data = extract_fields(item)
        if not data["id"]:
            skipped.append(f"Entry #{idx} skipped: missing id (g:id/id/title/link).")
            continue
        records.append(data)

    return records, skipped

def write_google_rss(records: List[Dict[str, Optional[str]]], out_path: str = "products-feed.xml") -> None:
    """
    يكتب ملف RSS 2.0 مع xmlns:g، ويملأ الحقول الأساسية وفق Google Product Feed الشائعة [web:16][web:33][web:31].
    """
    # جذر RSS مع namespace g
    rss = Element('rss', attrib={"version": "2.0"})
    # إدراج xmlns:g يتم تلقائياً عبر register_namespace واستعمال QName عند الحاجة،
    # لكن هنا سنضع وسوم g: كعناصر اسمها النصي "g:..." ضمن بيئة إخراج ElementTree.
    # سنبني channel/items بالشكل الكلاسيكي لـ RSS 2.0 [web:16].

    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = "Products Feed"
    SubElement(channel, 'link').text = "https://example.com"
    SubElement(channel, 'description').text = "Auto-generated Google Products Feed"

    # لكل record، أنشئ item مع وسوم g: مطلوبة
    for rec in records:
        item = SubElement(channel, 'item')

        # عناصر Google تُكتب كعناصر ذات prefix g:
        # مع ElementTree، استخدام اسم "g:tag" يخرج بشكل صحيح إذا namespace مسجل [web:26][web:70]
        def g(tag: str, value: Optional[str]):
            if value:
                SubElement(item, f"{{{G_NS}}}{tag}").text = value  # QName via {ns}tag [web:26][web:70]

        g('id', rec.get('id'))
        g('title', rec.get('title'))
        g('description', rec.get('description'))
        g('link', rec.get('link'))
        g('image_link', rec.get('image_link'))
        g('price', rec.get('price'))
        g('availability', rec.get('availability'))

        # بعض المنصات تتوقع أيضاً <guid> أو <link> القياسيين في RSS
        if rec.get('link'):
            SubElement(item, 'link').text = rec['link']
        if rec.get('id'):
            SubElement(item, 'guid').text = rec['id']

    # كتابة الملف مع التصريح و UTF-8
    tree = ElementTree(rss)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)

def main():
    print("🔄 جاري جلب ومعالجة الفيد ...")
    xml_input = read_input_xml()
    records, skipped = generate_google_records(xml_input)

    print(f"✅ العناصر المعالجة: {len(records)}")
    print(f"⚠️ العناصر المتخطاة: {len(skipped)}")
    for msg in skipped[:10]:
        print(" -", msg)

    # كتابة ملف RSS النهائي
    write_google_rss(records, "products-feed.xml")
    print("📝 تم إنشاء الملف: products-feed.xml")

if __name__ == "__main__":
    main()
