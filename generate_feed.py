#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from typing import Optional, Iterable, Tuple, Dict, Any
import sys

def text_or_none(tag) -> Optional[str]:
    return tag.get_text(strip=True) if tag and hasattr(tag, "get_text") else None

def first_text(*candidates) -> Optional[str]:
    for t in candidates:
        if t:
            return t
    return None

def iter_entries(soup: BeautifulSoup) -> Iterable:
    # يدعم RSS (item) وAtom (entry)
    entries = soup.find_all('item')
    if entries:
        return entries
    return soup.find_all('entry')

def extract_fields(item) -> Dict[str, Optional[str]]:
    # حاول أولاً وسوم Google namespace، ثم بدائل عامة إذا لم تتوفر
    gid = item.find('g:id')
    plain_id = item.find('id')
    title = item.find('g:title') or item.find('title')
    link = item.find('g:link') or item.find('link')
    price = item.find('g:price') or item.find('price')
    availability = item.find('g:availability') or item.find('availability')
    image_link = item.find('g:image_link') or item.find('image_link') or item.find('image')
    description = item.find('g:description') or item.find('description')

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

def generate_google_feed(xml_text: str) -> Tuple[list, list]:
    """
    يعيد (records, skipped) حيث:
    - records: عناصر صالحة تم استخراجها
    - skipped: قائمة بأسباب التخطي لكل عنصر لم يملك id صالح
    """
    soup = BeautifulSoup(xml_text, 'xml')  # ضروري مع namespaces مثل g: [web:6][web:9]
    records = []
    skipped = []

    # التأكد من وجود تصريح namespace في الجذر يساعد على صحة الفيد عند المصدر [web:16][web:18]
    # لكن BeautifulSoup لا يتطلب تسجيل namespace بالبحث النصي "g:tag" [web:9]
    for idx, item in enumerate(iter_entries(soup), start=1):
        data = extract_fields(item)
        if not data["id"]:
            skipped.append(f"Entry #{idx} skipped: missing id (g:id/id/title/link).")
            continue
        records.append(data)

    return records, skipped

def main():
    # مثال: قراءة محتوى XML من stdin في CI أو من ملف
    # xml_input = open('feed.xml', 'r', encoding='utf-8').read()
    xml_input = sys.stdin.read()

    print("🔄 جاري جلب ومعالجة الفيد ...")

    records, skipped = generate_google_feed(xml_input)

    # اطبع ملخصاً واضحاً يُفيد في الـ CI
    print(f"✅ العناصر المعالجة: {len(records)}")
    print(f"⚠️ العناصر المتخطاة: {len(skipped)}")
    for msg in skipped[:10]:
        print(" -", msg)

    # تابع بما يلزمك: كتابة CSV/JSON أو بناء XML جديد لرفعٍ لاحق
    # هنا مثال طباعة مختصر لكل عنصر
    for r in records[:5]:
        print(f"[ID={r['id']}] title={r['title']} price={r['price']} availability={r['availability']}")

if __name__ == "__main__":
    main()
