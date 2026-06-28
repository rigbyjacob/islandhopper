# New Regions — Spec Scaffold (first step)

Research-backed specs for 8 candidate regions. This is the **input to the terrain bake**:
each region becomes a `data/<id>.js` (`window.<ID> = {K, lon0, lat0, islandPolys, seaTint, foam, …}`)
generated from GEBCO bathymetry + coastline, then registered in `REGIONS` with weather defaults,
biome, tour route, and an art `resembles` mapping.

All coordinates are real (verified against Wikipedia / gazetteers). Latitudes are **negative for
Solomon**; longitudes are **negative (West)** for Aran, Faroe, Hebrides, Montauk, Kodiak.

## Summary

| id | display | center (lat, lon) | biome | resembles | character |
|----|---------|-------------------|-------|-----------|-----------|
| halong-bay | Hạ Long Bay | 20.88, 107.09 | trop | thailand | jade water, limestone towers, haze |
| el-nido-coron | Bacuit & Calamian (Palawan) | 11.55, 119.80 | trop | thailand | karst cliffs, turquoise lagoons |
| solomon-gizo | Gizo & New Georgia | -8.10, 156.95 | trop | hawaii | volcanic rainforest, reef lagoons |
| aran-islands | Aran Islands | 53.09, -9.64 | temp | sweden | grey karst, Atlantic cliffs, drystone walls |
| faroe-islands | Faroe Islands | 62.05, -6.95 | nord | sweden | basalt sea-cliffs, fjords, low cloud |
| small-isles-skye | Small Isles & Skye | 57.05, -6.30 | temp | sweden | Cuillin peaks, sea-lochs, misty light |
| montauk-east-end | Montauk & East End (LI) | 41.06, -72.05 | temp | sweden | moraine bluffs, dunes, salt marsh |
| kodiak-archipelago | Kodiak & Barren Is. | 58.05, -152.55 | nord | sweden | fjords, spruce ridges, fog |

**Art-style gap:** 5 of 8 high-latitude regions map to `sweden` as the nearest cool/treeless
archipelago preset. Faroe + Kodiak (basalt/fjord) and Hebrides + Aran (Atlantic cliffs) would be
the natural anchors for a future **"North Atlantic / Scotland"** art+water style if we add one.

---

## halong-bay — Hạ Long Bay (Vietnam)
- center: 20.880, 107.090 · bbox [106.95, 20.70, 107.30, 21.00]
- biome **trop** · resembles **thailand**
- Forests of grey-white limestone fengcong/fenglin towers from calm jade water; sea caves, hidden
  lagoons, pocket beaches; soft haze blurs receding karst rows.
- Islands: Cat Ba (Đảo Cát Bà) 20.795,107.011 ~17km · Bo Hon (Bồ Hòn) 20.883,107.100 — Surprise Cave ·
  Ti Top (Ti Tốp) 20.901,107.056 · Dau Go (Đầu Gỗ) 20.908,107.042 · Dau Be (Đầu Bê) 20.795,107.145 ·
  Monkey/Cat Dua 20.777,106.998 · Trong Mai islet (Fighting Cocks) 20.910,107.035 · Cong Do (Cống Đỏ)
  20.840,107.210 · Ngoc Vung (Ngọc Vừng) 20.865,107.400 · Quan Lan (Quan Lạn) 20.950,107.483 ·
  Co To (Cô Tô) 20.991,107.756
- Towns: Hạ Long City (Bãi Cháy) 20.960,107.043 · Cat Ba Town 20.728,107.048 · Cai Rong 21.064,107.420
- Tour: Hạ Long City → Trong Mai → Ti Top → Bo Hon → Cong Do → Dau Be → Monkey → Cat Ba Town
- Weather: timeOfDay 7.5, windDirDeg 45, windStrength 8, waveHeight 0.3, atmosphere 0.7

## el-nido-coron — Bacuit Archipelago & Calamian Islands (Palawan, Philippines)
- center: 11.55, 119.80 · bbox [119.25, 11.05, 120.30, 12.20] (El Nido SW → Coron/Busuanga NE)
- biome **trop** · resembles **thailand**
- Sheer jagged karst cliffs, vivid jungle tops, glass turquoise-to-cobalt water; hidden lagoons through
  cliff gaps, white sandbars, fringing reefs; strong sun glare.
- Islands: Cadlao 11.221,119.350 ~4.5km · Miniloc 11.151,119.316 (Big/Small Lagoon) · Matinloc
  11.167,119.284 · Tapiutan 11.208,119.264 · Pinagbuyutan 11.122,119.392 (tower islet) · Dilumacad
  "Helicopter" 11.201,119.338 · Snake/Vigan 11.095,119.341 (sandbar) · Coron 11.929,120.241 (lakes) ·
  Culion 11.819,119.970 · Busuanga 12.145,120.028 · Malcapuya 11.791,120.113 · Banana/Dicalubuan 11.771,120.127
- Towns: El Nido (Poblacion) 11.196,119.408 · Coron Town 11.999,120.205
- Tour: El Nido → Cadlao → Miniloc → Matinloc → Tapiutan → Pinagbuyutan → Snake → Helicopter
- Weather: timeOfDay 10, windDirDeg 60, windStrength 11, waveHeight 0.6, atmosphere 0.35

## solomon-gizo — Gizo & New Georgia (Western Province, Solomon Islands)
- center: -8.10, 156.95 · bbox [156.60, -8.20, 157.20, -7.85] (Gizo–Kolombangara core)
- biome **trop** · resembles **hawaii** (high volcanic, not karst)
- Rainforest volcanic islands — Kolombangara a near-perfect 1,770 m cone — fringed by coral reefs and
  pale-aqua lagoons; deep cobalt channels, jewel reef islets, towering afternoon cumulus.
- Islands: Ghizo -8.10,156.84 ~12km · Kolombangara -7.967,157.067 (Mt Veve cone) · Vella Lavella (Mbilua)
  -7.735,156.653 · Kennedy/Kasolo -8.108,156.903 (PT-109 islet) · Njari -8.015,156.758 (reef) ·
  Mbabanga -8.120,156.887 · New Georgia -8.230,157.582 · Rendova -8.534,157.307 · Tetepare -8.717,157.550
  (largest uninhabited in S Pacific) · Vangunu -8.626,157.982 · Uepi -8.422,157.940 (Marovo drop-off) ·
  Skull/Nusa Kunda -8.300,157.165 (shrine islet)
- Towns: Gizo -8.103,156.842 · Munda -8.328,157.267 · Noro -8.242,157.199
- Tour: Gizo → Kennedy → Mbabanga → Njari → Kolombangara → Vella Lavella → Skull → Munda
- Weather: timeOfDay 15, windDirDeg 135, windStrength 10, waveHeight 0.5, atmosphere 0.45
- Alt cluster: Marovo/Vona Vona (Vangunu/Uepi/Skull) for reef-threading.

## aran-islands — Aran Islands (Oileáin Árann, Ireland)
- center: 53.090, -9.640 · bbox [-9.90, 53.04, -9.50, 53.16] (+ Brannock/Straw rocks)
- biome **temp** · resembles **sweden** (cool treeless rocky archipelago; geologically karst, like a cold Burren)
- Bare grey limestone karst laced with drystone walls, near-treeless; sheer 80–100 m Atlantic cliffs on
  SW faces, sheltered shingle/sand on NE; steel-grey to deep-teal cold ocean, big swell, shifting light.
- Islands: Inishmore (Árainn/Inis Mór) 53.121,-9.723 ~13km — Dún Aonghasa · Inishmaan (Inis Meáin)
  53.085,-9.590 · Inisheer (Inis Oírr) 53.058,-9.528 — Plassy wreck · Brannock (Oileán Dá Bhranóg)
  53.145,-9.840 — Eeragh lighthouse · Straw (Oileán na Tuí) 53.118,-9.631 · Inishbofin (Inis Bó Finne)
  53.621,-10.209 · Inishark (Inis Airc) 53.612,-10.283 · St MacDara's (Oileán Mhic Dara) 53.305,-9.921 ·
  Mason (Oileán Máisean) 53.301,-9.888 · Gorumna (Garmna) 53.262,-9.678
- Towns: Kilronan (Cill Rónáin) 53.123,-9.661 · Kilmurvey 53.132,-9.753 · Inis Meáin village 53.085,-9.584 ·
  Cleggan pier 53.557,-10.114
- Tour: Kilronan → Dún Aonghasa cliffs → Brannock → Straw → Inishmaan → Inisheer
- Weather: timeOfDay 17, windDirDeg 225, windStrength 18, waveHeight 1.8, atmosphere 0.55

## faroe-islands — Faroe Islands
- center: 62.05, -6.95 · bbox [-7.70, 61.35, -6.25, 62.42]
- biome **nord** · resembles **sweden**
- Steep basalt sea-cliffs and stratified flat-topped peaks from deep cold water, narrow fjords/sounds;
  near-treeless emerald grass over dark rock, low cloud, slate-grey to teal water, white cliff-base surf.
- Islands: Streymoy 62.13,-7.00 ~47km (Tórshavn) · Eysturoy 62.22,-6.85 (Slættaratindur; Gjógv gorge) ·
  Vágar 62.07,-7.30 (Sørvágsvatn; Múlafossur) · Mykines 62.10,-7.64 (puffins) · Suðuroy 61.50,-6.85
  (Beinisvørð cliffs) · Sandoy 61.83,-6.80 · Borðoy 62.27,-6.55 (Klaksvík) · Kalsoy 62.30,-6.70 (Kallur
  lighthouse) · Kunoy 62.30,-6.65 · Viðoy 62.36,-6.52 · Svínoy 62.28,-6.32 · Fugloy 62.34,-6.30
- Towns: Tórshavn 62.01,-6.77 · Klaksvík 62.23,-6.59 · Sørvágur 62.07,-7.31 · Gjógv 62.33,-6.94 ·
  Vestmanna 62.16,-7.17 · Tvøroyri 61.55,-6.81 · Viðareiði 62.36,-6.53
- Tour: Tórshavn → Vestmanna → Vágar → Mykines → Streymoy → Gjógv → Kalsoy → Klaksvík → Viðoy
- Weather: timeOfDay 8, windDirDeg 225, windStrength 22, waveHeight 2.4, atmosphere 0.75

## small-isles-skye — Small Isles & Skye (Inner Hebrides, Scotland)
- center: 57.05, -6.30 · bbox [-6.55, 56.78, -5.95, 57.42]
- biome **temp** · resembles **sweden**
- Cuillin gabbro/basalt mountains + heather-bracken moorland to sea-lochs; grey-green water turning
  turquoise over white shell-sand and pink granite; Rùm Cuillin and Eigg's Sgùrr landmarks, misty light.
- Islands: Rùm 57.00,-6.33 ~13km (Cuillin; Kinloch) · Eigg 56.90,-6.13 (An Sgùrr ridge) · Muck 56.83,-6.23
  (Port Mòr) · Canna 57.06,-6.53 (basalt plateau) · Sanday 57.04,-6.50 (tidal twin) · Soay 57.16,-6.22
  (Loch Scavaig) · Skye Sleat/Cuillin coast 57.18,-6.10 ~35km (Elgol, ferry hub) · Scalpay 57.30,-5.97 ·
  Raasay 57.40,-6.04 (Dùn Caan) · Oigh-sgeir/Hyskeir 56.97,-6.68 (lighthouse skerry)
- Towns: Kinloch (Rùm) 57.01,-6.28 · Galmisdale (Eigg) 56.88,-6.13 · Port Mòr (Muck) 56.83,-6.23 ·
  A' Chill (Canna) 57.06,-6.49 · Elgol (Skye) 57.15,-6.11 · Armadale (Skye) 57.07,-5.89 · Mallaig 57.00,-5.83
- Tour: Elgol → Soay → Eigg → Muck → Rùm → Canna → Sanday → Armadale → Raasay
- Weather: timeOfDay 17, windDirDeg 240, windStrength 16, waveHeight 1.6, atmosphere 0.6

## montauk-east-end — Montauk & the East End (Long Island, NY)
- center: 41.06, -72.05 · bbox [-72.45, 40.92, -71.50, 41.22]
- biome **temp** · resembles **sweden**
- Glacial-moraine coast of low bluffs, dune Atlantic beaches, salt-marsh bays; bayberry/beach-grass/scrub
  oak; striped Montauk lighthouse on clay cliffs, Block Island's tan bluffs offshore; ocean-blue → bay green.
- Islands/headlands: Montauk Point (South Fork tip) 41.07,-71.86 · North Fork/Orient 41.10,-72.30 ~30km ·
  Shelter Island 41.06,-72.33 · Gardiners (Manchonake) 41.10,-72.10 · Plum Island 41.18,-72.18 ·
  Great Gull 41.20,-72.12 (terns) · Fishers Island (Munnawtawkit) 41.27,-72.00 ~14km · Block Island
  (Manisses, RI) 41.17,-71.58 · Robins Island 40.97,-72.47 · Ram Island 41.07,-72.28
- Towns: Montauk 41.04,-71.95 · Sag Harbor 41.00,-72.29 · Greenport 41.10,-72.36 · Orient 41.16,-72.20 ·
  Shelter Island Heights 41.08,-72.36 · New Shoreham 41.17,-71.56 · Fishers Island village 41.27,-71.99
- Tour: Montauk Point → Gardiners → Shelter Island → Greenport → Plum Island → Fishers Island → Block Island → Sag Harbor
- Weather: timeOfDay 18, windDirDeg 200, windStrength 12, waveHeight 1.0, atmosphere 0.4
- Native names (historical, not official): Gardiners=Manchonake, Block=Manisses, Fishers=Munnawtawkit.

## kodiak-archipelago — Kodiak Archipelago & Barren Islands (Alaska)
- center: 58.05, -152.55 · bbox [-153.30, 57.55, -151.90, 58.95]
- biome **nord** · resembles **sweden**
- Drowned-mountain coast of deep fjords and spruce-tundra ridges (the "Emerald Isle"), kelp beds, gravel
  beaches; cold deep-green/grey water, fog, snow-streaked summits; treeless rock toward the Barren Islands.
- Islands (Alutiiq names): Kodiak (Qik'rtaq) 57.60,-153.40 ~160km (city of Kodiak NE) · Afognak (Agw'aneq)
  58.25,-152.65 · Shuyak (Suyuraq) 58.55,-152.50 (state park) · Spruce 57.92,-152.41 (Ouzinkie) ·
  Whale 57.95,-152.75 (tidal pass) · Raspberry 58.05,-153.10 · Marmot 58.20,-151.85 (sea-lion rookery) ·
  Sitkalidak 57.13,-153.18 (Old Harbor) · Uganik 57.75,-153.55 · Barren Islands (Usuunaat) 58.90,-152.10
  (treeless, toward Kenai; Ushagat largest)
- Towns: Kodiak 57.79,-152.41 · Ouzinkie 57.92,-152.50 · Port Lions 57.87,-152.88 · Old Harbor 57.20,-153.30 ·
  Larsen Bay 57.54,-153.98
- Tour: Kodiak → Spruce → Whale → Afognak → Raspberry → Shuyak → Barren Islands → Marmot
- Weather: timeOfDay 7, windDirDeg 135, windStrength 18, waveHeight 2.2, atmosphere 0.8

---

## Next steps (the bake), per region

1. **Pull bathymetry/elevation** for each bbox (the existing `build/gen_worldmap.py` reads GEBCO;
   region tiles come from GEBCO + AWS Terrain Tiles as the Caribbean/Aegean did).
2. **Generate `data/<id>.js`** — project the bbox to world coords (compute `K`, `lon0`, `lat0` from
   the center + extent), extract `islandPolys` (named polys for the islands above), set `seaTint`/`foam`
   to match `resembles`.
3. **Register in `REGIONS`** with the `defaults` weather block above, `_BIOME[id]=biome`, the `tour`
   route (named islands), and `flora`/`palette` per biome (palms off for nord/temp; pine density up for
   nord; karst-grey rock for the thailand-style trop pair).
4. **Add to the globe** (`REGION_ART_COL[id]`, diorama placement at center lat/lon).
5. **Capture a demo scenario** per region once it loads.

Order suggestion (reuses existing art the most → least): el-nido-coron & halong-bay (thailand karst) →
solomon-gizo (hawaii volcanic) → faroe-islands & kodiak-archipelago (sweden nord) → aran-islands,
small-isles-skye, montauk-east-end (sweden temp). The 4 North-Atlantic regions are the case for a new
art style before polishing them.

**Built so far:** halong-bay ✅ and el-nido-coron ✅ are baked, registered, and playable.

---

# Batch 2 — coastal / peninsula regions

These are coast/peninsula-led rather than pure archipelagos; the bake features the islands + headlands
that make a good sailing loop. Two span widely separated sub-areas (flagged below).

| id | display | center (lat, lon) | biome | resembles | character |
|----|---------|-------------------|-------|-----------|-----------|
| st-johns-conception-bay | St. John's & Conception Bay (NL) | 47.62, -52.85 | nord | sweden | rust/grey sea-cliffs, fog, cold Atlantic |
| cape-cod-islands | Cape Cod & the Islands (MA) | 41.50, -70.20 | temp | japan | sandy moraine, dunes, barrier beaches |
| exe-estuary-south-devon | Exe Estuary & South Devon + Lundy (UK) | 50.58, -3.45 | temp | japan | red sandstone cliffs, estuary flats, granite Lundy |
| apo-dauin-siquijor | Apo I., Dauin & Siquijor (PH) | 9.18, 123.32 | trop | caribbean | volcanic isles, clear reef-fringed turquoise |

Notes: **Exe/South Devon** and **Apo/Dauin** each have an outlier — Lundy sits ~110 km NW of the Devon
coast in the Bristol Channel; Camiguin sits ~150 km SE of the Apo cluster (off N Mindanao) and is best
as its *own* future region, not in this bbox.

## st-johns-conception-bay — St. John's & Conception Bay (Newfoundland)
- center: 47.62, -52.85 · bbox [-53.05, 47.45, -52.60, 47.85]
- biome **nord** · resembles **sweden**
- Rust-and-grey sedimentary sea-cliffs (Bell Island iron beds) into cold slate-green swell; sparse boreal
  scrub on headlands, fog-prone, little beach — sea-cliff, stack and tickle.
- Islands/headlands: Bell I. (Wabana) 47.633,-52.957 ~9km · Little Bell I. 47.605,-52.945 · Kelly's I.
  47.575,-52.915 · Cape Spear 47.523,-52.620 (easternmost N. America) · Cape St. Francis 47.810,-52.785 ·
  Signal Hill / The Narrows 47.571,-52.681 · Fort Amherst Head 47.564,-52.683 · Bauline Head 47.715,-52.985 ·
  Topsail Head 47.530,-52.945 · Pouch Cove Head 47.762,-52.770
- Towns: St. John's 47.561,-52.712 · Wabana (Bell I.) 47.633,-52.948 · Portugal Cove 47.617,-52.852 ·
  Conception Bay South 47.525,-52.985 · Pouch Cove 47.758,-52.770
- Tour: The Narrows → Cape Spear → Fort Amherst Head → Kelly's I. → Little Bell I. → Bell I. (Wabana) → Bauline Head → Cape St. Francis → Signal Hill
- Weather: timeOfDay 7.5, windDirDeg 250, windStrength 18, waveHeight 2.2, atmosphere 0.7

## cape-cod-islands — Cape Cod & The Islands (Massachusetts)
- center: 41.50, -70.20 · bbox [-70.95, 41.20, -69.90, 42.10]
- biome **temp** · resembles **japan**
- Glacial-outwash sand: scrub-oak/pitch-pine moraine, grass-topped dunes, kettle ponds, long barrier
  beaches; cool slate-teal water, salt marsh, soft sea haze; clay bluffs (Aquinnah/Wellfleet), few true cliffs.
- Islands: Cape Cod peninsula 41.69,-70.20 ~100km (the "mainland" arm) · Martha's Vineyard 41.39,-70.62 ~30km
  (Aquinnah clay cliffs) · Nantucket 41.284,-70.099 ~24km · Naushon 41.483,-70.758 (Elizabeth Is.) · Nashawena
  41.429,-70.874 · Pasque 41.445,-70.835 · Cuttyhunk 41.425,-70.928 · Nonamesset 41.527,-70.685 · Monomoy
  41.550,-70.000 (barrier spit) · Muskeget 41.335,-70.304 · Penikese 41.452,-70.913
- Towns: Provincetown 42.051,-70.186 · Hyannis 41.653,-70.283 · Chatham 41.682,-69.960 · Woods Hole 41.524,-70.671 ·
  Edgartown 41.389,-70.513 · Nantucket Town 41.284,-70.099 · Cuttyhunk Village 41.425,-70.926
- Tour: Provincetown → Chatham → Monomoy → Nantucket → Muskeget → Martha's Vineyard → Cuttyhunk → Naushon → Woods Hole
- Weather: timeOfDay 9, windDirDeg 225, windStrength 14, waveHeight 1.2, atmosphere 0.45

## exe-estuary-south-devon — Exe Estuary & South Devon + Lundy (UK)
- center: 50.58, -3.45 · bbox [-4.75, 50.30, -3.40, 51.25] (spans the Devon coast AND Lundy ~110 km NW)
- biome **temp** · resembles **japan**
- Warm red Permian sandstone cliffs/stacks (Jurassic Coast W end) over a tidal sand/mudflat estuary with the
  Dawlish Warren dune spit; green farmland headlands, mild grey-green Channel water; Lundy is a stark grey-granite
  cliff-ringed plateau. (Exeter itself is inland → absent; the estuary mouth anchors it.)
- Islands/headlands: Lundy 51.180,-4.667 ~5km (marquee, Bristol Channel) · Dawlish Warren spit 50.610,-3.440 ·
  Orcombe Point 50.609,-3.378 (Jurassic Coast start) · Straight Point 50.607,-3.355 · The Parson & Clerk 50.555,-3.470
  (stack) · Hope's Nose 50.464,-3.490 · Berry Head 50.399,-3.485 · Thatcher Rock 50.448,-3.508 · The Ore Stone
  50.450,-3.500 · Pole Sands 50.615,-3.430 (tidal bank)
- Towns: Exmouth 50.620,-3.413 · Starcross 50.628,-3.444 · Topsham 50.683,-3.466 · Dawlish 50.581,-3.467 ·
  Teignmouth 50.546,-3.494 · Torquay 50.462,-3.525 · Brixham 50.396,-3.513
- Tour: Topsham → Starcross → Dawlish Warren → Orcombe Point → The Parson & Clerk → Teignmouth → Hope's Nose → Berry Head → Lundy
- Weather: timeOfDay 17, windDirDeg 235, windStrength 12, waveHeight 1.0, atmosphere 0.4

## apo-dauin-siquijor — Apo Island, Dauin & Siquijor (Philippines, Bohol Sea)
- center: 9.18, 123.32 · bbox [123.20, 9.00, 123.70, 9.45]
- biome **trop** · resembles **caribbean**
- Volcanic isles in warm clear turquoise Bohol Sea — fringing/sloping coral reefs, black-and-white volcanic
  sand, coconut-green slopes; small steep islets vs the long forested Negros coast.
- Islands/coast: Apo I. 9.075,123.270 ~1.5km (marine sanctuary, off Dauin) · Siquijor 9.213,123.516 ~24km ·
  Negros SE coast at Dauin 9.193,123.270 (muck-dive black sand) · Sumilon I. 9.428,123.391 (off SE Cebu, MPA) ·
  Maite/Masaplod reef 9.220,123.290 · Tambobo (Bonbonon) headland 9.108,123.150 · Larena coast (Siquijor N)
  9.247,123.589 · Salag Doong headland 9.188,123.655 · Paliton Point (Siquijor W) 9.207,123.470 · Zamboanguita
  coast 9.100,123.200
- Towns: Dauin 9.193,123.265 · Dumaguete 9.307,123.305 · Zamboanguita 9.100,123.190 · Apo I. village 9.075,123.270 ·
  Larena 9.250,123.589 · Siquijor town 9.214,123.515
- Tour: Dumaguete → Dauin → Apo I. → Zamboanguita → Tambobo Bay → Paliton Point → Siquijor town → Salag Doong → Sumilon I.
- Weather: timeOfDay 11, windDirDeg 70, windStrength 9, waveHeight 0.5, atmosphere 0.25

**Future / outliers:** Camiguin (volcanic island off N Mindanao, ~9.17°N 124.73°E) — its own tropical/hawaii-style region.
