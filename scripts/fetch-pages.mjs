import fs from "fs/promises";
import path from "path";

function absolutizeLinks(html, base) {
  return html
    .replace(/(href|src)\s*=\s*"(\/[^"]*)"/g, (_, attr, p) => `${attr}="${new URL(p, base).href}"`)
    .replace(/(href|src)\s*=\s*'(\/[^']*)'/g, (_, attr, p) => `${attr}='${new URL(p, base).href}'`);
}

async function fetchHtml(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed ${res.status} ${res.statusText} for ${url}`);
  return await res.text();
}

async function main() {
  const conf = JSON.parse(await fs.readFile("./urls.json", "utf-8"));
  for (const p of conf.pages) {
    const url = new URL(p.path, conf.base).href;
    const html = await fetchHtml(url);
    const normalized = absolutizeLinks(html, conf.base);
    await fs.mkdir(path.dirname(p.outfile), { recursive: true });
    await fs.writeFile(p.outfile, normalized, "utf-8");
    console.log(`Wrote ${p.outfile}`);
  }

  const index = `<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>صفحات المتجر</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <h1>صفحات المتجر</h1>
  <ol>
    ${conf.pages.map(p => `<li><a href="/${p.outfile}">${p.title}</a></li>`).join("\n    ")}
  </ol>
</body>
</html>`;
  await fs.writeFile("index.html", index, "utf-8");
  console.log("Wrote index.html");
}

await main();
