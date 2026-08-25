#!/usr/bin/env node
/* Stamps css/js links with a content hash so a changed file can never be
   served from cache under an old ?v= number.  Run via: npm run build        */
const fs = require("fs"), crypto = require("crypto"), path = require("path");

const ASSETS = ["css/tailwind.css", "js/scripts.js"];
const PAGES = ["index.html", "404.html", "fa/index.html", "ku/index.html", "ar/index.html"];

const hash = f =>
  crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex").slice(0, 8);

const hashes = Object.fromEntries(ASSETS.map(a => [a, hash(a)]));

for (const page of PAGES) {
  if (!fs.existsSync(page)) continue;
  let html = fs.readFileSync(page, "utf8");
  const before = html;
  for (const asset of ASSETS) {
    // matches  css/tailwind.css  ../css/tailwind.css  /css/tailwind.css  (+ any existing ?v=)
    const re = new RegExp(`((?:\\.\\./|/)?${asset.replace(/[.]/g, "\\.")})(\\?v=[^"']*)?`, "g");
    html = html.replace(re, `$1?v=${hashes[asset]}`);
  }
  if (html !== before) fs.writeFileSync(page, html);
  console.log(`  stamped ${page}`);
}
console.log("\nhashes:");
for (const [a, h] of Object.entries(hashes)) console.log(`  ${a}  ->  ?v=${h}`);
