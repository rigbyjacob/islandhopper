#!/usr/bin/env node
// Bundle the dev build (index.html + external data/*.js) into a single
// self-contained dist/index.html for distribution.
//
// Dev layout keeps the heavy GIS blobs in data/*.js (classic scripts that set
// window.* before the deferred module runs) so index.html stays editable.
// Packing inlines each <script src="data/..."></script> with the file's
// contents, producing one portable file that needs no local server paths.
//
// Usage:  node build/pack.js   (or: just pack)

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const srcPath = path.join(root, 'index.html');
const outDir = path.join(root, 'dist');
const outPath = path.join(outDir, 'index.html');
// GitHub Pages publish dir: serve the same self-contained file from /docs on the
// default branch (Settings → Pages → Deploy from a branch → main / docs).
const docsDir = path.join(root, 'docs');
const docsPath = path.join(docsDir, 'index.html');

let html = fs.readFileSync(srcPath, 'utf8');

// Inline every <script src="data/xxx.js"></script> with the file's contents.
const re = /<script\s+src="(data\/[^"]+\.js)"><\/script>/g;
let count = 0;
html = html.replace(re, (_m, rel) => {
  const code = fs.readFileSync(path.join(root, rel), 'utf8').replace(/\s*$/, '');
  count++;
  return `<script>/* inlined ${rel} */\n${code}\n</script>`;
});

if (count === 0) {
  console.warn('pack: no data/*.js includes found — nothing to inline. ' +
               'Is index.html already packed?');
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, html);

// Also publish to /docs for GitHub Pages. .nojekyll stops Pages' Jekyll pass from
// mangling the static file (and is required if any asset path starts with "_").
fs.mkdirSync(docsDir, { recursive: true });
fs.writeFileSync(docsPath, html);
fs.writeFileSync(path.join(docsDir, '.nojekyll'), '');

const mb = (Buffer.byteLength(html) / (1024 * 1024)).toFixed(2);
console.log(`pack: inlined ${count} data file(s) → dist/index.html + docs/index.html (${mb} MB)`);
