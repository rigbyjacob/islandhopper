# Volcano / Lava Eruption — DISABLED (2026-06-26)

The submarine-volcano eruption effect was shelved after a long day of iteration that never
reached an acceptable look. **All the code is kept, just disabled.** This documents what was
tried and why it didn't work, so a future attempt doesn't repeat the same dead ends.

## How it's disabled / how to re-enable

- Master flag: `const VOLC_ENABLED = false;` (just above the `VOLC` definition, ~line 468 of `index.html`).
- `buildVolcano()` and `updateVolcano()` early-return when it's false, so all the build/update
  code stays in the file but never runs.
- `seabedHeight()` returns the **pure real-GEBCO** seabed when disabled (the fabricated volcanic
  cone in `volcanoHeight()` is no longer max'd into the terrain).
- `START_AT_VOLCANO` is false and gated on `VOLC_ENABLED`, so the app starts at the normal boat tour.
- Leftover (harmless): the "🌋 Volcano" button and the `dev.erupt()/volcGo()/volcParticles()`
  hooks still exist; they just don't do anything visible while disabled.

To resume: set `VOLC_ENABLED = true`. Everything wires back up.

## What the feature was

A fixed dramatic seamount (`VOLC`, peak just under the surface) in the open water east of the
islands, baked into `seabedHeight`, topped with a glowing caldera and a triggerable eruption:
a raymarched volumetric fire column + ejecta particles + an ash/steam plume, with a
rumble→erupt→subside→idle state machine and auto-eruptions.

## Part A — Volumetric fire column (raymarched)

A camera-facing billboard quad whose fragment shader raymarches an animated 3D fbm density field
in a bounded column (`densAt` / `fireRay`, MeshBasicNodeMaterial). This part looked the *best* of
everything and is the reference quality the particles never matched.

Things done that worked:
- **Bottom-up height front** (`uFireRise`): density gated by a climbing `hN` cutoff so the column
  is supposed to grow from the vent instead of the whole height appearing at once.
- **Molten vs gaseous**: raised density contrast (`-0.12 ×4.2`) and front-to-back accumulation
  (`×0.34`) so it reads as an opaque molten body, not wispy gas.
- **Wind shear** (`uFireWind`): centreline bends downwind weighted by `hN^1.5` + an fbm gust
  wobble; AABB and billboard quad widened so the leaning crown isn't clipped.
- **Cooling to ash**: heat bleeds out with altitude (`cool`), crown goes to grey-brown cinder.

**UNRESOLVED (the blocker on the column):** despite `uFireRise`, it still "fades in at full
height" and shows a faint **ghost outline of the full column height all the time**. The *finish*
(fading down on subside) looks right; the *start* is wrong — it should erupt bottom-up. Suspect
the `alpha.mul(uVolcFire)` global term and/or the AABB/quad always being present means the volume
is always being marched; the rise front changes density but not the overall envelope/outline.
This was never fixed.

## Part B — Ejecta particles (the part that really sank it)

Many architectures tried, none satisfactory. In rough order:

1. **InstancedMesh 3D icosahedron blobs** (MeshStandardNodeMaterial, magma emissive, stretched
   along velocity). Real depth/shading/occlusion. Complaint: *"hard-edge blobs, not at all like
   the volumetric lava."*
2. **Softened the blob material** (unlit MeshBasicNodeMaterial, animated fbm cracks, fresnel +
   noise-eroded alpha). Complaint: still reads as hard ellipsoids — **you can't fuzz the edge of a
   solid mesh** (a surface has no volumetric falloff).
3. **Soft additive billboard sprites** (feathered radial "fireball" canvas texture, per-sprite
   heat color). Complaints: *overwhelmed the column / translucency mismatch*; then when switched
   to **normal blending** to show a dark cooled mass → *"barely visible"* (translucent sprites
   barely tint a bright sea; additive can't render anything *darker* than the background).
4. **Wind feel**: strong drag-toward-wind made them *"blow like paper"*; switched to a gentle
   drift so they keep a ballistic arc *"like molten rock."* (This part was right.)
5. **Cooling color**: bright spark → dark ember. Reported *"same color from start to finish,
   same size, no natural physics"* — largely because at high density everything overlapped into
   one uniform glow.
6. **Density sweep**: 700 → 2800 → 28000 sprites. High counts washed into a uniform blob;
   low/medium looked like a *"toy sparkler, not a thick stream of molten rock with sparks and ash."*
7. **Spawn geometry**: first version sprayed a **ring/curtain around** the column (wrong); changed
   to launch from the column **core** and arc **outward** (better, but never finished judging).
8. **Final rebuild (called off):** instanced 3D molten **chunks** (tumbling, cooling magma color,
   varied sizes) + a bright **spark** subset (streaked along velocity) + denser **visible ash** —
   intended to be the requested "mixture of solid molten chunks, bright spark streaks, and smoke
   that isn't practically invisible." **It failed to boot** (stuck on the "Still loading" overlay —
   a likely TSL/material or JS error introduced during the rebuild that was never diagnosed), and
   the feature was stopped at that point. This is the state preserved behind the flag, so if
   re-enabled it will currently need that boot error found first.

## Why it kept missing (lessons for next time)

- **Iterated blind for far too long.** The dev server (`localhost:8080`, live-reload via
  `reload.txt`) can be viewed directly with the Chrome tools / screenshots. Look at the actual
  render every change instead of reasoning from code. This was the single biggest time sink.
- **Particles vs. volume are different media.** Billboards = soft/fuzzy but can't be a dark solid
  mass and wash out in bulk; instanced meshes = solid chunks with real lighting but hard-edged.
  The desired "thick stream of molten rock + sparks + ash" probably needs **all three layers
  composited deliberately** (volume for the body, instanced chunks for the lava bombs, a small
  bright spark layer, and an opaque smoke plume), each tuned while *watching it*, not one system
  trying to be everything.
- **Additive can't show cooled/dark material; normal blend disappears over bright sea.** Pick the
  blend per layer with that in mind (hot sparks additive; cooled chunks opaque lit geometry; ash
  normal/opaque).
- **Fix the column's bottom-up start + ghost-outline first** — it's the hero element and the
  particles were being judged against a column that itself wasn't right.

## Key symbols (all still in `index.html`)

`VOLC`, `volcanoHeight`, `buildVolcano`, `updateVolcano`, `eruptVolcano`, `_spawnFount`,
`_spawnEjecta`, `_spawnAsh`, `_setSpin`, uniforms `uVolcFire / uFireBase / uFireRise / uFireWind`,
`makeFireballTexture`, `makeSmokeTexture`, and `dev.erupt / dev.volcGo / dev.volcParticles / dev.volcDbg`.
