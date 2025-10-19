import fs from "fs/promises";

const FEED_URL = "https://api.easy-orders.net/api/v1/products/feed/37ad236e4a0f46e29792dd52978832bc/channel/google";
const SITE_BASE = "https://sherow1982.github.io/saudi-matjar.arabsad.com";

function slugify(s){
  s = (s || "").trim().toLowerCase();
  s = s.replace(/[^a-z0-9\-]+/g,"-").replace(/\-+/g,"-").replace(/^\-|\-$/g,"");
  return s || "item";
}

async function fetchSlugs(){
  const res = await fetch(FEED_URL, { headers: { "Accept": "application/xml,text/xml;q=0.9,*/*;q=0.8" }});
  if(!res.ok) throw new Error("Feed HTTP " + res.status);
  const text = await res.text();
  const xml = new DOMParser().parseFromString(text, "application/xml");
  if(xml.querySelector("parsererror")) throw new Error("XML parse error");
  const items = Array.from(xml.querySelectorAll("item"));
  const slugs = items.map(item=>{
    const title = item.querySelector("title")?.textContent?.trim() || "item";
    const gid = item.querySelector("g\\:id, id")?.textContent?.trim() || title;
    return slugify(gid);
  });
  // إزالة التكرارات
  return Array.from(new Set(slugs));
}

function buildSitemap(urls){
  const head = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`;
  const tail = `</urlset>\n`;
  const baseUrls = [
    `${SITE_BASE}/`,
    `${SITE_BASE}/pages/shipping-policy.html`,
    `${SITE_BASE}/pages/who-we-are.html`,
    `${SITE_BASE}/pages/terms-and-conditions.html`,
    `${SITE_BASE}/pages/about-our-store.html`,
    `${SITE_BASE}/pages/social-media-pages.html`,
    `${SITE_BASE}/pages/privacy-policy.html`,
    `${SITE_BASE}/pages/contact-us.html`,
    `${SITE_BASE}/pages/refund-policy.html`
  ];
  const lines = [...baseUrls, ...urls.map(u => `${SITE_BASE}/product/${u}/`)]
    .map(u => `  <url><loc>${u}</loc></url>`)
    .join("\n");
  return `${head}\n${lines}\n${tail}`;
}

async function main(){
  const slugs = await fetchSlugs();
  const sitemap = buildSitemap(slugs);
  await fs.writeFile("sitemap.xml", sitemap, "utf-8");
  console.log("Wrote sitemap.xml with", slugs.length, "products");
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
