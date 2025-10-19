import fs from "fs/promises";
import path from "path";

// Convert relative /href and /src to absolute against source domain
function absolutizeToSource(html, base) {
  return html
    .replace(/(href|src)\s*=\s*"(\/[^"]*)"/g, (_, attr, p) => `${attr}="${new URL(p, base).href}"`)
    .replace(/(href|src)\s*=\s*'(\/[^']*)'/g,  (_, attr, p) => `${attr}='${new URL(p, base).href}'`);
}

// Optional: rewrite root-leading links to your repo base on GitHub Pages (disabled by default)
function rewriteToRepoBase(html, repoBase = "/") {
  const prefix = repoBase.replace(/\/+$/,'');
  return html
    .replace(/(href|src)\s*=\s*"(\/(?!\/)[^"]*)"/g, (_, attr, p) => `${attr}="${prefix}${p}"`)
    .replace(/(href|src)\s*=\s*'(\/(?!\/)[^']*)'/g,  (_, attr, p) => `${attr}='${prefix}${p}'`);
}

async function fetchHtml(url) {
  const res = await fetch(url, { headers: { "Accept": "text/html,*/*;q=0.8", "User-Agent": "Mozilla/5.0 PageSyncBot" }});
  if (!res.ok) throw new Error(`Failed ${res.status} ${res.statusText} for ${url}`);
  return await res.text();
}

function buildPagesIndex(conf){
  const list = conf.pages.map(p => `<li><a href="../${p.outfile}">${p.title}</a></li>`).join("\n        ");
  return `<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>صفحات المتجر</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;line-height:1.7;margin:24px;background:#f9fafb}
    h1{color:#0b57d0}
    a{color:#0b57d0;text-decoration:none}
    a:hover{text-decoration:underline}
    ul{padding-inline-start:1.25rem}
  </style>
</head>
<body>
  <h1>صفحات المتجر</h1>
  <ul>
        ${list}
  </ul>
  <p><a href="../">العودة للصفحة الرئيسية</a></p>
</body>
</html>`;
}

async function main(){
  const conf = JSON.parse(await fs.readFile("./urls.json", "utf-8"));

  for (const p of conf.pages) {
    const url = new URL(p.path, conf.base).href;
    const html = await fetchHtml(url);

    // 1) normalize assets to source so CSS/images don't break on Pages
    let normalized = absolutizeToSource(html, conf.base);

    // 2) if needed, rewrite root-leading href/src to your repo base on Pages (optional)
    // normalized = rewriteToRepoBase(normalized, conf.repoBase);

    const outFile = p.outfile;
    await fs.mkdir(path.dirname(outFile), { recursive: true });
    await fs.writeFile(outFile, normalized, "utf-8");
    console.log("Wrote", outFile);
  }

  // write index of pages under pages/ to avoid overriding site home
  const pagesIndex = buildPagesIndex(conf);
  await fs.writeFile("pages/index-pages.html", pagesIndex, "utf-8");
  console.log("Wrote pages/index-pages.html");
}

await main();
