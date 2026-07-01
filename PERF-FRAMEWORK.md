# Island Hopper — Performance Framework

The app runs great on an M2 Max but can crush weaker machines (freezing Chrome on
high‑DPI integrated‑GPU laptops). This framework makes the cost adjustable per
device **without degrading the high‑end experience**, and gives a fast loop to
prove an optimization didn't break the look.

Design rule: **`ULTRA` == the exact previous literals.** The default path is
byte‑identical to before. The probe only *recommends*; a tier is applied only by
the user (it persists + reloads), so the scene is always rebuilt consistently
from `Q` at init — no half‑applied live state, no partial‑mutation bugs.

---

## The five pieces

1. **Quality ladder** — one `QUALITY` preset table (`ULTRA / HIGH / MED / LOW /
   MOBILE`); every heavy lever reads from the active `Q`.
2. **Capability probe** — `runDiag()` reads the GPU + device class and runs a
   short micro‑bench on the heaviest scenes, then recommends a tier.
3. **Recommend‑only UI** — a toast + dev‑menu button. `applyQuality(tier)` is the
   *only* thing that changes quality (persists tier + reloads).
4. **Visual A/B** — `perfShots()` screenshots every scenario at the current tier;
   `perfContactSheet()` composites them across tiers next to the lever values, so
   a quality regression is visible in lockstep with the speed win.
5. **Mobile path** — same tools, run on‑device over Tailscale; `MOBILE` tier.

---

## Lever map

`ULTRA` values equal the old hardcoded literals. Cost is GPU unless noted.

| Lever (`Q.*`) | Controls | Cost class | Quality risk | ULTRA → HIGH → MED → LOW → MOBILE |
|---|---|---|---|---|
| `pixelCap` | render‑resolution cap (`setPixelRatio`) | **highest** — scales ~quadratically | low | 2.0 · 1.75 · 1.5 · 1.25 · 1.0 |
| `msaa` | MSAA antialiasing (constructor) | high on weak GPUs | low–med (edges) | on · on · off · off · off |
| `shadowSun` | primary sun shadow map px | high | med (frond crispness) | 4096 · 2048 · 2048 · 1024 · 1024 |
| `shadowSun2` | alien companion‑sun shadow px | med (alien skin only) | low | 2048 · 1024 · 1024 · 512 · 512 |
| `godrayTaps` | god‑ray radial samples | med (when sun visible) | low (decay auto‑derived) | 30 · 24 · 18 · 12 · 12 |
| `starCount` | Milky‑Way point density | low–med | low | 9000 · 6000 · 3500 · 1800 · 1500 |
| `floraMul` | instanced foliage pool size | med (CPU+GPU) | med (sparser islands) | 1.0 · 0.8 · 0.55 · 0.35 · 0.30 |
| `foamClaws` | Hokusai 3D curl‑claws **+ shore breakers** | high (Hokusai style only) | style‑specific | on · on · off · off · off |
| `globeSeg` | globe relief‑sphere tessellation (lon×lat) | high (globe view) | med (relief smoothness) | 360 · 288 · 220 · 160 · 128 |
| `globeShadow` | globe sun shadow map px | med (globe view) | low (terminator crispness) | 2048 · 2048 · 1024 · 1024 · 1024 |

Notes:
- **`pixelCap` is the single biggest win** and the safest — most "freezes Chrome"
  cases are a 4K/high‑DPI screen rendering at `dpr=2` with MSAA. Capping it alone
  often recovers a low‑end machine.
- **God‑ray decay is now derived from the tap count** (`w *= 1 − 1.71/N`). This
  reproduces the old constants exactly (0.943 @ 30 taps, 0.967 @ 52) and keeps the
  shaft look consistent at *any* tap count, so lowering taps doesn't change reach.
- **`foamClaws:false` also disables shore breakers** — they share the crest pass
  (`_clawCrests`). Both are Hokusai‑only, so this only affects that art style.
- Construction/build‑time levers (`msaa`, shadow sizes, `floraMul`, `starCount`,
  `foamClaws`, `globeSeg`, `globeShadow`) are exactly why "apply" reloads:
  everything is rebuilt from `Q`.

**Globe view** renders as its own scene (`globeScene`/`globeCam`) but shares the
renderer, so `pixelCap` and `msaa` already apply there. The globe‑specific cost is
the displacement relief sphere (`globeSeg`, the heaviest single globe object) and
the globe sun shadow (`globeShadow`); the globe's Milky‑Way arc rides `starCount`.
All three now scale with the tier, so a tier change covers the globe as well as
the in‑region view.

---

## How to run it

**On any device (URL flags):**
- `?diag` — probe on boot and show the recommendation toast.
- `?tier=LOW|MED|HIGH|ULTRA|MOBILE` — force a tier for this load (overrides saved).
- `?noopt` — the BASELINE build (4096 shadow every frame · 52 god‑ray taps ·
  per‑instance tree recompose) to A/B the optimizations themselves.
- `?perf` / `?perf=label` — auto‑run the full perf sweep once booted.

**Dev menu (Actions):**
- `🔬 Diagnose & recommend tier` — runs `runDiag()`; recommend‑only.
- `▶ Run perf sweep` — the existing CPU/GPU‑ms + fps sweep over all scenarios.
- `📸 Capture tier shots (<tier>)` — screenshot every scenario at the current tier.
- `🗂 Open tier contact sheet` — cross‑tier visual A/B grid.

**Console API** (also under `window.dev` when dev mode is on):
```js
await runDiag()            // recommend a tier (no change)
applyQuality('MED')        // persist + reload at MED
perfShots()                // capture shots for the current tier
perfContactSheet()         // open the cross-tier comparison
runPerfSweep({})           // full perf sweep → localStorage
perfDiff('baseline','optimized')   // compare two labeled runs
```

**Calibrating a quality lever in lockstep:**
1. `?tier=ULTRA` → `perfShots()` (+ `runPerfSweep`) → captures the reference.
2. `applyQuality('MED')` (reloads) → `perfShots()` (+ sweep) again.
3. `perfContactSheet()` → eyeball the two columns side by side; `perfDiff` for the
   numbers. If MED looks fine, the downgrade is safe; if a scene degrades, bump
   that one lever up in the `QUALITY` table and repeat.

---

## Mobile loop (Tailscale)

The on‑device path reuses the existing `just share` / `just tunnel` HTTPS loop and
the `/telemetry` beacon.

1. `just share` (or `just tunnel`) to expose the dev server over HTTPS.
2. On the phone open `…ts.net/?diag` — the probe runs on real mobile hardware and
   recommends (almost always `MOBILE`). Tap **Apply** to lock it in.
3. To sweep on‑device: open the dev menu → `▶ Run perf sweep`, or
   `…?tier=MOBILE&perf`. Keep the tab focused (RAF throttles in the background; the
   sweep flags `backgrounded` so you know fps is unreliable but CPU/GPU ms stay valid).
4. `📸 Capture tier shots` on the phone, then pull the contact sheet to compare the
   mobile look against desktop tiers.

---

## What's calibrated vs. what needs real‑device data

The `QUALITY` preset values and the `runDiag` GPU‑ms thresholds (≤6 → ULTRA, ≤10 →
HIGH, ≤16 → MED, else LOW) are sensible starting points, **not** measured truth.
The intended next step is to run `runDiag` + `runPerfSweep` on the actual machines
that struggle (the ones freezing Chrome) and on a mid‑range reference, then tighten:

- the **ms→tier thresholds** in `_recommendTier`, and
- the **per‑lever values** in the `QUALITY` table,

using `perfContactSheet` to make sure each downgrade is invisible enough. Because
the harness already captures real GPU timestamps where available, a few sweeps on
target hardware turn these estimates into calibrated numbers quickly.

> Heads‑up: WebGPU canvas screenshot capture (`perfShots`) depends on the browser
> allowing `drawImage` from the WebGPU canvas. If a device returns blank shots, the
> perf numbers are still valid — only the visual A/B image is unavailable there.
