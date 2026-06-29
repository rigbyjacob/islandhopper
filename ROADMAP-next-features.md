# Island Hopper — next-features roadmap

Feasibility + priority for the seven ideas. Sizing is relative: **S** ≈ an afternoon,
**M** ≈ a focused session or two, **L** ≈ a multi-session subsystem. Risk = how likely
it loops on "looks wrong" tuning (the shadow/volcano tax).

---

## Priority order (recommended)

| # | Feature | Size | Risk | Why here |
|---|---------|------|------|----------|
| 1 | Vignette during dive | S | low | Quick, pure win, infra already exists |
| 2 | Fog + locale weather (snow) | S→M | low-med | Builds on storm/rain + `THREE.Fog` already in scene |
| 3 | Real textured moon | M (small) | low | Self-contained; reuses `drawMoonPhase` |
| 4 | Improved clouds & sky | M | med | Big payoff for sunset scenes, but subjective tuning |
| 5 | Audio (weather/ocean/vehicles) | L | low-med | High impact; large but self-contained |
| 6 | Terrain deformation (weapons) | L | high | Biggest scope + tone shift; prototype later |
| 7 | Realistic textures/buildings/roads/fauna | L+ | med-high | Open-ended; may clash with painterly styles |

---

## 1. Vignette during the dive — DO FIRST
**Now:** The dive already has staged progress values — `_diveZoom` (globe→surface, `k=t/dur`)
and `_descent` (establishing→follow cam), plus a `_diveFade` cloud overlay and a full-screen
`#overlay` DOM layer. So there's already a per-frame 0→1 "how deep into the dive are we" number.

**Needed:** One radial-gradient overlay (DOM div or a fullscreen quad) whose opacity tracks the
dive curve — ramp vignette **up** during the zoom-in, ease it **down** as you settle over the
region. ~30 lines, no shader risk.

**Payoff vs cost:** Highest ratio of the seven. Masks the exact transition seams you mentioned.

## 2. Fog + locale-specific weather (incl. snow) — QUICK WIN, THEN EXTEND
**Now:** Storm system is real (`stormFactor`, `localStormG`, world-space rain particles,
rain-on-lens overlay). A `THREE.Fog` object already exists. Several regions are *described* as
foggy (Faroe, Kodiak, Newfoundland) but don't render distinct fog. Region `defaults` already
carry weather params (wind, waves, storm), so there's a clean place to add per-region weather.

**Needed:**
- **Fog (S):** drive fog color/density from region + time + storm. Almost free, big mood gain.
- **Snow (M):** a second particle variant of the existing rain system — snow sprite, slower
  drift, no splash; gate by region/latitude. Reuses `buildRain`/particle plumbing.
- **Locale weather (S):** add a `weather` field to region defaults (e.g. `fog`, `snow`,
  `clear`) and wire it through.

**Risk:** Low — extends proven systems. Snow look needs a little tuning.

## 3. Real textured moon
**Now:** Moon is procedural in the sky shader — a disk + halo at `uMoonDir`, brightness
`uMoonInt`. The **phase slider only dims it** (`moonStr *= moonPhase`); it never changes shape.
There's already a `drawMoonPhase(cv, p)` canvas routine (drives the slider handle).

**Needed:** A camera-facing moon quad (or upgraded shader disk) with a moon texture + a phase
terminator. Two options:
- **Texture the existing slider art:** bake `drawMoonPhase` to a CanvasTexture — fastest, but
  the painted phase is fixed-lit.
- **Proper terminator (better):** sample a grey moon/crater texture and multiply by a phase mask
  computed from sun vs moon direction, so it tracks the slider *and* the sun. ~M, low risk.

**Payoff:** Strong night/sunset upgrade, cheap, isolated.

## 4. Improved clouds & sky (streaks, striations, sunset/sunrise)
**Now:** Sky is a shader dome (`buildSky`, gradient + sun/moon orbs, Van Gogh night mode).
Clouds are **billboard sprite puffs** (`buildClouds`, soft + cartoon textures), not volumetric.

**Needed:** Extend the sky shader with noise-driven horizontal cloud **streaks/cirrus bands** and
richer **sunset/sunrise color striations** tinted by sun elevation; optionally add stretched
cirrus sprites to the cloud field. Real payoff for the golden-hour scenarios.

**Risk:** Medium — this is the same "is it beautiful yet" subjective loop that the shadows hit.
Worth timeboxing and checking against your eye on-device.

## 5. Audio (weather, ocean, vehicles, weapons)
**Now:** Only background **music** (one `Audio` element). No SFX, no spatial audio.

**Needed:** A real audio layer. Recommended approach to stay single-file and avoid asset/licensing
loading: **synthesize with Tone.js** (loadable from CDN) rather than shipping sound files.
- Ambient beds cross-faded by weather/locale: waves, wind, rain, birds, rigging.
- Positional per-vehicle loops: ship engine, sub sonar pings, UFO tractor-beam hum, plane.
- One-shots synced to events you already fire: thunder↔lightning, cannon, splashes.
Hook points already exist (storm state, vehicle FX update, lightning).

**Risk:** Low-moderate, but it's **L** — many small pieces. Best as its own dedicated push.
First slice: ocean + wind ambient bed reacting to `stormFactor` (proves the pipeline).

## 6. Terrain deformation (bombs / tractor beam / missiles / cannons)
**Now:** Terrain height comes from a sampled field (`TF.H`) rendered via a GPU **clipmap**
(`updateClipmapTerrain`). The **volcano/lava** feature is the closest precedent — and it's
**disabled** after many failed look iterations (see `NOTES-volcano-lava.md`). No projectile/weapon
system exists yet.

**Needed:** Two hard halves — (a) projectile systems + impact detection per vehicle, and
(b) actual deformation: edit `TF.H` at impact and re-resample the clipmap, or crater decals.
Getting craters to look good on the painterly terrain is the risky part (cf. volcano).

**Risk:** High + biggest scope. Also a **tone shift** from serene sim toward action/game.
**Suggestion:** if you want this, prototype a single crater-on-impact (cannon → seabed dimple)
in isolation first to de-risk the look before building the whole arsenal.

## 7. Realistic surface textures / roads / buildings / flora / fauna
**Now:** Islands are colored terrain + instanced **palms/shrubs** (per-region `flora` config).
Cities are **labels only** — no building or road meshes. `Birds` toggle exists (fauna hook).
Everything is graded through the painterly `STYLES` (Gauguin, Hokusai, etc.).

**Needed:** Instanced buildings near city labels, roads as terrain decals/splines, region-specific
flora swaps, animated fauna instances. Large and per-region (17 regions), and "realistic" partly
fights the deliberate non-realistic art direction.

**Risk:** Medium-high, open-ended. **Scope down** to land it: e.g. start with simple instanced
low-poly buildings clustered at existing city points, styled to match the active palette — not a
full realism pass.

---

## Suggested sequencing
**Now:** 1 (vignette) → 2-fog. **Next:** 2-snow/locale → 3 (moon). **Then:** 4 (sky) and the first
slice of 5 (ambient audio). **Later / needs a direction call:** 6 (weapons) and 7 (realism) — both
shift the project's tone and scope; worth a quick prototype before committing.
