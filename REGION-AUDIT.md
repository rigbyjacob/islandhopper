# Island Hopper — Per-Region Fidelity Audit

Comparing each in-sim region against its real-world counterpart. For each region: in-app screenshots (top-down + obliques) are assessed against researched reference imagery, noting differences in **terrain structure**, **land texture** (rock / sand / grass / forest / urban), **flora types**, and **color palette** (land / water / building / flora).

Method: in-app captures taken in Photorealistic style at midday. Real-world reference profiles gathered from public sources (linked per region). Verdicts: ✅ good match · 🟡 partial / stylized · 🔴 notable mismatch.

Regions audited (18): caribbean, aegean, japan, thailand, hawaii, halong, elnido, solomon, apo, aran, faroe, skye, montauk, kodiak, stjohns, capecod, exe, sweden.

---

## 1. Caribbean — Leeward Islands  🟡 good, slightly over-green
**Real:** Two-part arc — steep forested volcanic inner islands (Guadeloupe Basse-Terre, Montserrat, St Kitts/Nevis) + low, dry, tan-scrub coral islands (Antigua, Barbuda, St Barths, Grande-Terre). Turquoise reef shallows → cobalt. Pastel/red-roof colonial towns.

- **Terrain structure** ✅ Leeward arc layout is faithful: Puerto Rico anchors the west, Virgin Islands chain, down to Guadeloupe's twin-lobe "butterfly." Volcanic relief on inner islands reads well.
- **Land texture** 🟡 Nearly everything is rendered lush forest-green. The real flat coral islands (Antigua/Barbuda/St Barths) are arid tan scrub + pale limestone — the sim makes them too green/wet. Puerto Rico does show some tan lowland (good).
- **Flora** 🟡 Uniform tropical forest + palms; fine for volcanic islands, over-applied to the dry ones (should be cactus/acacia scrub + savanna).
- **Palette** — Water ✅ excellent (turquoise-over-reef → deep blue). Land 🟡 a touch too saturated/uniform green. Buildings: small clustered dots, not clearly pastel/red-roof at this scale.
- **Fix ideas:** give low/flat islands (small radius, low elevation) a drier tan/scrub palette + sparser flora; reserve lush green for the high volcanic ones.

## 2. Aegean — Cyclades  🟡 good dry palette, a few islands too green
**Real:** Scattered barren peaks of a submerged range; sun-bleached beige/grey/ochre rock, sparse olive/thyme scrub, largely treeless; intense azure water; iconic whitewashed cubic villages with cobalt domes.

- **Terrain structure** ✅ Many scattered low-to-mid rocky islands in plausible Cyclades layout (Syros, Paros, Naxos, Amorgos, Santorini labelled). Faithful archipelago feel.
- **Land texture** ✅→🟡 Base is correctly dry tan/khaki rock — a clear, correct departure from the Caribbean green. But several islands (Naxos/Paros centres) carry too much dark forest-green; real Cyclades are more uniformly barren scrub.
- **Flora** 🟡 Should be sparse low scrub + occasional olive/cypress; sim adds lusher forest patches that read too vegetated.
- **Palette** — Land ✅ beige/ochre good; Water ✅ azure/turquoise good. Missing the signature **whitewashed + blue-dome village** look (towns are dots/labels only).
- **Fix ideas:** push these islands further toward barren (cap forest tint, more bare-rock/scrub); consider white-cube town motifs (the code already has an Aegean town style — verify it's showing).

## 3. Japan — Sagami Bay  ✅ good (missing urban + Fuji)
**Real:** Semicircular bay flanked by Izu/Miura peninsulas, forested hills behind the shore, Izu Ōshima volcanic island offshore, dense coastal cities (Kamakura/Zushi), cooler steel-blue water, Mt Fuji backdrop.

- **Terrain structure** ✅ Bay + flanking forested peninsulas + **Izu Ōshima** present as a volcanic islet. Relief good.
- **Land texture** ✅ Forest green with bare brown rock ridges — appropriate temperate cover. 🟡 Lacks the dense built-up coastal strip (real shore is heavily urbanized).
- **Flora** ✅ Temperate conifer/broadleaf green (reads as pine/cedar). Good.
- **Palette** ✅ Water correctly cooler/steel-blue (not tropical turquoise except shallows); land green/brown good.
- **Fix ideas:** add coastal urban density near city labels; optional Mt Fuji on the skybox for the money shot.

## 4. Thailand — Phang Nga Bay / Andaman  ✅ strong match
**Real:** Calm bay studded with vertical jungle-clad limestone karst towers (incl. James Bond Island/Ko Tapu); milky jade-green water; mangroves; Phuket hilly.

- **Terrain structure** ✅ Phang Nga Bay with scattered karst islets (James Bond I., Ko Yao Noi/Yai, Ko Lanta labelled) + larger hilly mainland/Phuket. Steep tower relief reads.
- **Land texture** ✅ Grey-tan limestone rock draped in dense green jungle — correct karst look.
- **Flora** ✅ Saturated tropical jungle on the rock. Good.
- **Palette** ✅ Water nails the milky **jade-green/turquoise** signature; land grey-rock + green. Among the best regions.
- **Fix ideas:** minor — could add mangrove fringe tone at islet bases; otherwise faithful.

## 5. Hawaii — the Islands  🟡 layout perfect, too uniformly green
**Real:** Volcanic chain; strong wet/dry split — lush windward rainforest vs arid brown leeward + black lava fields (Big Island), red soil, multi-colored beaches; deep Pacific blue (narrow reefs).

- **Terrain structure** ✅ Excellent — Niʻihau, Kauaʻi, Oʻahu, Molokaʻi, Lānaʻi, Maui, Kahoʻolawe + Big Island all correctly placed and shaped, with volcanic relief.
- **Land texture** 🟡 Every island is uniform lush dark green. Missing Hawaii's defining contrast: arid brown/ochre leeward slopes, black basalt lava fields, red soil.
- **Flora** 🟡 All rainforest; should include dry grassland/shrub leeward and near-barren young lava.
- **Palette** ✅ Water correctly deep Pacific blue (not reef-turquoise). 🟡 Land too monochrome green — add brown/black/red.
- **Fix ideas:** add a leeward-dry + lava palette variant (e.g. drive aridity by a per-island or directional mask; black-rock zones on Big Island).

## 6. Hạ Long Bay  ✅ good match
**Real:** ~1,600 vertical limestone karst towers in calm emerald/jade water; grey rock capped with green forest; almost no beaches.
- **Terrain structure** ✅ Dense field of karst islets in a sheltered bay (Tì Tóp, Bồ Hòn, Cống Đỏ labelled). Captures the "many towers" character.
- **Land texture** ✅ Grey limestone + green forest drape. 🟡 Towers read a touch more rounded/forested than the real near-vertical spikes.
- **Flora** ✅ Jungle green on rock.
- **Palette** ✅ Water emerald/jade — correct; land grey+green.
- **Fix ideas:** steeper/sharper tower silhouettes would push realism; minor.

## 7. El Nido & Coron  ✅ good match
**Real:** Jagged grey-to-blackened limestone karst + sheer cliffs over turquoise Bacuit Bay; white/golden beaches; small El Nido town.
- **Terrain structure** ✅ Scattered karst islands + larger island (Culion) in plausible layout.
- **Land texture** ✅ Limestone + forest; white-sand rings present. 🟡 Rock renders tan-ish; real Coron limestone is darker/blacker-weathered.
- **Flora** ✅ Tropical forest + coastal palms.
- **Palette** ✅ Water turquoise/emerald excellent; beaches white. 🟡 darken/weather the rock for Coron's signature.
- **Fix ideas:** darker, more vertical limestone for Coron's cliffs.

## 8. Solomon Islands — Gizo & Kolombangara  🟡 too much bare rock
**Real:** Kolombangara = near-perfect rainforested volcanic cone (Mt Veve), unbroken dense jungle shore-to-summit; Gizo smaller/lower; reef-fringed.
- **Terrain structure** ✅ Kolombangara renders as a large near-circular volcanic island; Gizo + smaller islands + reefs around. Good shapes.
- **Land texture** 🔴 Too much exposed brown/tan rock on the slopes. Real Solomons are unbroken dark rainforest with almost no bare rock — sim's slope/elevation rock ramp over-exposes.
- **Flora** 🟡 Should be denser, darker, continuous jungle.
- **Palette** ✅ Water turquoise/blue good; 🟡 land needs to be much greener, less brown.
- **Fix ideas:** for wet-tropical regions, raise the rock/cliff elevation+slope thresholds so jungle climbs higher before bare rock shows (see systemic note).

## 9. Apo, Dauin & Siquijor  🟡 generic tropical
**Real:** Small volcanic Apo + black-sand Dauin coast + raised-coral Siquijor (green over pale, white beaches); vibrant reef.
- **Terrain structure** ✅ Larger islands + small islet (Sumilon/Apo) + reef shallows — plausible Bohol Sea layout.
- **Land texture** 🟡 Generic green-forest + brown-rock; doesn't capture Dauin's black volcanic sand or Siquijor's pale-coral character.
- **Flora** ✅ Tropical forest/palms.
- **Palette** ✅ Water turquoise; land generic green/brown. Reads as "a tropical island," not specifically these places.
- **Fix ideas:** add black-sand beach tone for the Dauin/volcanic side; otherwise acceptable.

## 10. Aran Islands  🔴 too dark; water too tropical
**Real:** Three FLAT pale-grey limestone-pavement islands (Inishmore/Inishmaan/Inisheer) gridded with white dry-stone walls + small green fields; treeless; cool steely-grey Atlantic water.
- **Terrain structure** ✅ Three flat islands correctly named & positioned, low relief — faithful.
- **Land texture** 🔴 Rendered dark near-black; should be PALE grey limestone pavement + small green field patches. Big tonal miss.
- **Flora** 🟡 Treeless (correct) but surface doesn't read as grass/limestone.
- **Palette** 🔴 Land far too dark; Water 🔴 turquoise (should be cold steely Atlantic blue-grey). Missing dry-stone-wall grid signature.
- **Fix ideas:** pale-grey limestone palette + lighter green fields; cold-water tint (see systemic note).

## 11. Faroe Islands  🔴 too grey/rocky; missing emerald turf
**Real:** Steep basalt islands almost entirely carpeted in VIVID EMERALD GRASS over dark cliffs; misty; brightly painted + turf-roof villages; deep moody blue-grey water.
- **Terrain structure** ✅ Many steep high-relief islands correctly named (Streymoy, Eysturoy, Vágar, Suðuroy…). Mist suits the locale. Good shapes.
- **Land texture** 🔴 Dominantly bare grey rock; real Faroe is green grass to the cliff edges. Slope/elevation rock ramp over-exposes rock here.
- **Flora** 🔴 Should be continuous green turf; sim shows little.
- **Palette** 🔴 Land too grey (needs emerald green). Fog ✅ (maybe slightly heavy). Water washed by fog.
- **Fix ideas:** let grass dominate up steep slopes (raise rock threshold) and use a vivid green for Faroe; optional turf-roof/painted village motifs.

## 12. Small Isles & Skye  🟡 a bit brown; water too tropical
**Real:** Mountainous (jagged dark Cuillin) + green-brown heather moorland; Small Isles (Rùm, Eigg, Canna); steely grey-blue lochs; Portree pastel harbour row.
- **Terrain structure** ✅ Skye + Rùm/Eigg/Canna/Raasay/Scalpay/Soay correctly named & placed; Cuillin relief present. Good.
- **Land texture** 🟡 Brown rock + dark green — plausibly moorland but a little too bare-brown; could use more grass-green + purple heather.
- **Flora** 🟡 Moor/heath ok; no purple-heather accent.
- **Palette** 🟡 Land ok-ish; Water 🔴 too turquoise (should be steely loch grey-blue).
- **Fix ideas:** more green/heather on the moor; cold-water tint.

## 13. Kodiak Archipelago  🟡 great structure, too grey/foggy
**Real:** "Emerald Isle" — saturated deep-green Sitka spruce + tundra over glacier-carved, deeply fjord-indented mountains; cold blue-grey/teal water.
- **Terrain structure** ✅ Excellent — Afognak/Raspberry/Shuyak/Barren Islands with the signature deeply fingered fjord coastline. Best structural match of the cool regions.
- **Land texture** 🟡 Reads dark grey-green; should be saturated emerald spruce. Heavy regional fog mutes it a lot.
- **Flora** 🟡 Should read as dense green conifer; muted.
- **Palette** 🟡 Land needs more green; fog ✅ appropriate but heavy; water washed.
- **Fix ideas:** lift land greenness; consider dialing the Kodiak fog down a notch so the Emerald-Isle colour reads.

## 14. St. John's & Conception Bay  🟡 fog-muddy; missing the colour
**Real:** Rugged grey-rock Avalon coast, deep narrow harbour (the Narrows) under Signal Hill, spruce + heath barrens; iconic "Jellybean Row" rainbow houses; cold navy/steel Atlantic, often foggy.
- **Terrain structure** 🟡 Large coastal landmass + islet present; the iconic Narrows/Signal Hill aren't clearly readable from above. Coastline plausible.
- **Land texture** 🟡 Dark grey-green under heavy fog — plausibly rock+spruce barrens but muddy.
- **Flora** 🟡 Dark, reads spruce-ish.
- **Palette** 🟡 Heavy fog; land dark; Water 🔴 turquoise (should be cold navy/steel). Missing the Jellybean-Row colour signature.
- **Fix ideas:** ease fog; cold-water tint; (stretch) colourful harbour-row town motif.

## 15. Cape Cod & the Islands  🔴 structure great, far too green (should be sand)
**Real:** Glacial SAND peninsula — the hooked "arm," pale tan/buff beaches & dunes, sage-green dune grass + pitch-pine/scrub-oak; grey-shingle / white-clapboard villages; blue-green nearshore.
- **Terrain structure** ✅ Excellent — the hooked Cape peninsula + Martha's Vineyard + Nantucket/Muskeget + Elizabeth Islands (Cuttyhunk, Naushon…) all present and correctly shaped; flat.
- **Land texture** 🔴 Rendered dark-green forest. Cape Cod's whole identity is SAND (it's a sandbar) — pale tan dunes/beaches + sage scrub. Biggest texture miss of the set.
- **Flora** 🟡 Should be dune grass + sparse pitch-pine/scrub-oak (sage-green), not lush forest.
- **Palette** 🔴 Land needs to flip to pale-sand + sage; Water 🟡 slightly tropical-turquoise.
- **Fix ideas:** sand-dominant palette for low glacial-sand regions (high sand band, sage grass, sparse pine); grey-shingle village tone.

## 16. Montauk & East-End Long Island  🟡 structure faithful, a bit too forested
**Real:** Forked glacial East End (twin forks), sandy beaches + tall ochre/tan ocean bluffs, maritime grassland/scrub + some woods; blue-green to deep blue.
- **Terrain structure** ✅ Excellent — the twin-forked East End, Plum Island, Gardiners all faithful.
- **Land texture** 🟡 Dark-green forest dominant; Long Island is fairly wooded so less wrong than Cape Cod, but missing sandy beaches + the signature ochre eroding bluffs.
- **Flora** 🟡 Forest ok; add dune grass/scrub.
- **Palette** 🟡 Land a touch dark-green; Water turquoise (bays ok, ocean side should be deeper blue). Montauk bluffs (tan/ochre) not represented.
- **Fix ideas:** sandy beach/bluff tone on the ocean side; lighten interior toward grassland.

## 17. Stockholm Archipelago  ✅ good (missing bare granite + cold water)
**Real:** ~30,000 low islands/skerries; smooth grey-pink rounded granite + pine forest; Falu-red cottages; cool steely Baltic, calm/enclosed.
- **Terrain structure** ✅ Excellent — fragmented low archipelago of many islands/skerries (Ljusterö, Möja, Sandön, Ingarö, Gällnö), low relief. Very faithful.
- **Land texture** ✅→🟡 Dark-green pine forest is right; but missing the **smooth grey-pink exposed granite** that's the archipelago's signature texture (sim is mostly forest).
- **Flora** ✅ Pine/conifer green — correct.
- **Palette** 🟡 Land green good; add pink-grey granite; Water 🔴 too turquoise (should be cool steely Baltic). Falu-red cottages not visible.
- **Fix ideas:** expose smooth bare-granite on low rounded rock; cold-water tint; optional Falu-red boathouse motif.

---

## Cross-cutting (systemic) findings & priority fixes

These patterns recur across many regions; fixing them lifts the whole set at once:

1. **Water is tropical-turquoise everywhere** 🔴 (highest impact). The reef-shallow bathymetry tint is applied globally, so cold regions (Aran, Faroe, Skye, Kodiak, Newfoundland, Stockholm) look Caribbean. **Fix:** a per-region "sea coolness/temperature" factor that shifts shallow-water hue from turquoise → steely grey-blue for cold-latitude regions.
2. **Steep cool islands over-expose bare rock** 🔴 (Faroe, Solomon, partly Skye/Kodiak). The slope/elevation rock+cliff ramp shows brown/grey rock where the real place is continuous green (emerald turf / rainforest). **Fix:** per-region rock thresholds — let grass/forest climb higher before bare rock appears on "green" regions.
3. **Everything skews lush green** 🟡 (Caribbean dry isles, Hawaii leeward/lava, Cape Cod sand, Aegean barren). The land ramp defaults green; arid/sandy/barren locales need their own palettes. **Fix:** per-region palette presets — dry-tan-scrub, sand-dune, barren-rock, lava-black — selected by region, not one global green ramp.
4. **Terrain STRUCTURE is consistently excellent.** Island shapes/layouts and named features are faithful in nearly every region (Hawaii chain, Cape hook, LI forks, Kodiak fjords, Cyclades scatter, Guadeloupe butterfly). The gaps are almost entirely **texture/palette**, not geometry.
5. **Town/building identity is absent** 🟡 — pastel Caribbean, white-blue Cyclades, Jellybean-Row Newfoundland, Falu-red Sweden, grey-shingle Cape are all signatures that don't read (towns are dots/labels). Lower priority; town-motif system already exists for some.
6. **Region fog is good but heavy** on Kodiak/Faroe/Newfoundland — appropriate mood, but dial down ~20% so the land colour reads.

**Best matches:** Thailand (Phang Nga), Hạ Long, El Nido, Hawaii & Cape Cod & Montauk (structure), Japan, Stockholm.
**Most-wanted fixes:** cold-water tint (#1) and per-region land palettes for Cape Cod (sand), Faroe (emerald), Aran (pale limestone), Solomon (jungle), Hawaii (lava/arid).


