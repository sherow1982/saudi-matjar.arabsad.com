import fs from "fs/promises";
import path from "path";

// يحول href/src النسبية إلى مطلقة تجاه نطاق EasyOrder الأصلي
function absolutizeToSource(html, base) {
  return html
    .replace(/(href|src)\s*=\s*"(\/[^"]*)"/g, (_, attr, p) => `${attr}="${new URL(p, base).href}"`)
    .replace(/(href|src)\s*=\s*'(\/[^']*)'/g, (_, attr, p) => `${attr}='${new URL(p, base).href}'`);
}

// خيار بديل: إعادة كتابة الروابط المطلقة لتشير إلى مسار موقعك على GitHub Pages عند الحاجة
function rewriteToRepoBase(html, repoBase = "/") {
  // إن أردت أن تشير الروابط الداخلية التي تبدأ بـ / إلى جذر موقعك تحت اسم المستودع
  return html
    .replace(/(href|src)\s*=\s*"(\/(?!\/)[^"]*)"/g, (_, attr, p) => `${attr}="${repoBase.replace(/\/+$/,'')}${p}"`)
    .replace(/(href|src)\s*=\s*'(\/(?!\/)[^']*)'/g, (_, attr, p) => `${attr}='${repoBase.replace(/\/+$/,'')}${p}'`);
}

async function fetchHtml(url) {
  const res = await fetch(url, { headers: { "Accept": "text/html,*/*;q=0.8" }});
  if (!res.ok) throw new Error(`Failed ${res.status} ${res.statusText} for ${url}`);
  return await res.text();
}

function buildIndex(conf){
  const list = conf.pages.map(p => `<li><a href="${p.outfile}">${p.title}</a></li>`).join("\n        ");
  return `<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>صفحات المتجر</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;line-height:1.7;margin:24px;background:#f9fafb}
    h1{color:#0b57d0}
    ul{padding-inline-start:1.25rem}
    a{color:#0b57d0;text-decoration:none}
    a:hover{text-decoration:underline}
  </style>
</head>
<body>
  <h1>صفحات المتجر</h1>
  <ul>
        ${list}
  </ul>
  <p><a href="./">العودة للصفحة الرئيسية</a></p>
</body>
</html>`;
}

async function main(){
  const conf = JSON.parse(await fs.readFile("./urls.json", "utf-8"));

  // جلب وحفظ كل صفحة
  for (const p of conf.pages) {
    const url = new URL(p.path, conf.base).href;
    const html = await fetchHtml(url);

    // 1) ثبّت الأصول إلى نطاق المصدر كي لا تتكسر
    let normalized = absolutizeToSource(html, conf.base);

    // 2) إذا رغبت أن تشير الروابط الجذرية إلى موقعك على GitHub Pages، فعّل السطر التالي:
    // normalized = rewriteToRepoBase(normalized, conf.repoBase);

    // اكتب الملف
    await fs.mkdir(path.dirname(p.outfile), { recursive: true });
    await fs.writeFile(p.outfile, normalized, "utf-8");
    console.log("Wrote", p.outfile);
  }

  // أنشئ فهرس الصفحات
  const indexHtml = buildIndex(conf);
  await fs.writeFile("index.html", indexHtml, "utf-8");
  console.log("Wrote index.html");
}

await main();
