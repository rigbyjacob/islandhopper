#!/usr/bin/env node
// Build data/starmap.js from the d3-celestial open datasets (CC-BY).
// Run once:  node build/build_starmap.js
// Produces window.STARMAP = { stars:[[raDeg,decDeg,mag,bv]...],
//                             lines:[{r:rank, seg:[[[ra,dec]...] ...]}],
//                             labels:[{n:name, ra, dec, r:rank}] }
// Stars are filtered to mag <= 5.4 (naked-eye-ish) to stay compact (~1500 stars).

const https = require('https');
const fs = require('fs');
const path = require('path');

const BASE = 'https://raw.githubusercontent.com/ofrohn/d3-celestial/master/data/';
const get = (file) => new Promise((res, rej) => {
  https.get(BASE + file, r => { let d=''; r.on('data', c=>d+=c); r.on('end', ()=>res(JSON.parse(d))); }).on('error', rej);
});

(async () => {
  const MAGCAP = 5.4;
  const [stars, lines, names] = await Promise.all([
    get('stars.6.json'), get('constellations.lines.json'), get('constellations.json')
  ]);

  const starOut = [];
  for (const f of stars.features) {
    const m = f.properties.mag;
    if (m == null || m > MAGCAP) continue;
    const [ra, dec] = f.geometry.coordinates;          // degrees, RA in [-180,180]
    const bv = (f.properties.bv == null) ? 0.0 : +f.properties.bv;
    starOut.push([ +ra.toFixed(3), +dec.toFixed(3), +m.toFixed(2), +bv.toFixed(2) ]);
  }

  const lineOut = lines.features.map(f => ({
    r: +f.properties.rank,
    seg: f.geometry.coordinates.map(seg => seg.map(([ra,dec]) => [ +ra.toFixed(3), +dec.toFixed(3) ]))
  }));

  const labelOut = names.features.map(f => ({
    n: f.properties.name,
    ra: +f.geometry.coordinates[0].toFixed(3),
    dec: +f.geometry.coordinates[1].toFixed(3),
    r: +f.properties.rank
  }));

  const payload = { stars: starOut, lines: lineOut, labels: labelOut };
  const outPath = path.resolve(__dirname, '..', 'data', 'starmap.js');
  fs.writeFileSync(outPath, 'window.STARMAP=' + JSON.stringify(payload) + ';\n');
  const kb = (fs.statSync(outPath).size/1024).toFixed(0);
  console.log(`starmap: ${starOut.length} stars, ${lineOut.length} constellations, ${labelOut.length} labels → data/starmap.js (${kb} KB)`);
})().catch(e => { console.error('build_starmap failed:', e.message); process.exit(1); });
