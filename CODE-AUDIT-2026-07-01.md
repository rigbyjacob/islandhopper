# Island Hopper — Second-Opinion Code Audit (Fable, 2026-07-01)

Scope: `index.html` (8,485 lines), `build/` pipeline, `data/` region blobs, prior docs
(REGION-AUDIT.md, PERF-FRAMEWORK.md). Method: six parallel domain reviews (control/physics,
pathfinding, rendering/perf, GIS pipeline, region geography, audio/UI/graphs); every headline
finding independently re-verified against source before inclusion. Line numbers refer to
`index.html` unless noted.

**Overall verdict:** the core engineering is much better than typical for a project of this
shape — the PID/Kalman/pure-pursuit stack is the real algorithms correctly wired, the hex-grid
math is textbook-correct, the bathymetry encode/decode round-trip survives adversarial checking,
per-frame CPU is essentially allocation-free, and the QUALITY tier ladder is fully wired.
The defects that matter cluster into three themes: **(1) sign/convention bugs in exactly the
quantities the sim teaches** (cross-track gain, heading readout), **(2) staleness** (two regions
baked before the lonscale fix, a generator that no longer reproduces its own shipped data,
a Caribbean-only star dome), and **(3) GPU lifetime/fixed costs** the tier ladder doesn't touch
(region-swap leaks, a permanent second shadow pass, untiered vertex budgets).

---

## Priority fixes (ranked)

1. **Cross-track correction sign is inverted** — the one-character bug that matters most.
2. **HUD heading is 90° off the compass rose** — math angle printed as if it were a bearing.
3. **Region swap leaks VRAM by design; `_heightTex` subset is safely fixable** — demo-mode sessions grow without bound.
4. **Companion-sun shadow pass runs on every Earth scene** — a full extra scene render bought for nothing outside alien mode.
5. **Aegean & Japan data predate the lonscale fix** — the two flagship regions are E-W stretched 22–25%.
6. **Star dome hardcoded to 17.7°N** — the Faroes get a Caribbean sky.
7. **Audio init is one-shot; a failed CDN load or suspended iOS context is permanently silent.**
8. **Restored toggles render lit but never fire their side effects** — root cause of the known alien-toggle quirk, applies to every toggle.
9. **Unreachable A* goal → full-component flood, retried every 1 s.**
10. **`hawaii` missing from REGION_META** (only region absent).

---

## 1 · Control, physics, estimation

**[HIGH] XTE sign inverted (L1639, L1668, L1697).** `xteSigned = tx*(pos.z-a.z) - tz*(pos.x-a.x)`
is positive when the boat sits on the +angle side of the tangent; `course + clamp(P.xteGain*xteSigned, …)`
rotates the course *further* that way. Verified analytically (course `atan2` and the cross product
share the same (x,z) convention, so the correction must be subtracted) and numerically by the
domain reviewer (kinematic sim: gain ≥ ~0.04 at lookahead 26 parks the boat ~17 u off the line
forever; threshold scales ~1/lookahead). Pure pursuit dominates at the default 0.012, which is
why it sails anyway — but the slider labeled "snaps to line harder" (L328, L6863) weakens tracking,
and **every baked demo scenario ships `xteGain: 0.03`**, near the divergence threshold. Fix: negate.

**[MED] Integrator accumulates while Ki = 0 (L885–889).** Conditional-integration anti-windup is
textbook-correct, but with ki=0 the output never saturates, so `i` grows unboundedly under
persistent error; gain sliders don't reset PID state. Slide Ki to 0, sail, restore Ki → instant
rudder slam. Clamp `i` or reset on gain change.

**[MED] Assist episodes poison estimator + telemetry (L1722–1734, L4000, L1887).** `runAssist`
moves the boat kinematically but never updates `s.speedWater`, so the KF dead-reckons on a frozen
speed and absorbs the discrepancy into the current estimate; after handback, feed-forward crabs
against a fictitious current. Meanwhile telemetry plots live heading error against a frozen PID —
a flat rudder producing a perfect recovery. For a teaching sim: flag assist intervals on the chart
and either update `speedWater` or pause KF prediction during assist.

**[LOW]** 3-DOF model omits `u̇+=v·r / v̇−=u·r` coupling (corners on rails; flatters the PID) ·
KF process noise scales dt² per step → frame-rate-dependent tuning (L1395) · naive `P=(I−KH)P`
update, no symmetrization (L1403) · A* current-penalty uses ground-truth current, not the KF
estimate, and ignores the tide wobble (L1133) · `gpsAccum = 0` instead of `-= 1/3` drops
fractional remainder (L4003).

**Verified clean:** heading error shortest-path-wrapped everywhere incl. the derivative path
(L879–889, L1858); derivative-on-measurement with stable LPF; semi-implicit Euler + dt cap 0.04;
KF F/Q/R/H mutually consistent, injected noise exactly matches R; current observable; feed-forward
math correct; assist and PID are mutually exclusive with hysteresis and reset on handback.

## 2 · Pathfinding

**[HIGH] Planner is blind to 1 u of draft (L948 vs L329/L1474).** Grid blocks water shallower than
1.6 u; hull grounds at 2.6 u (`P.draft`). The comment says this is deliberate ("channels stay
open"), but the consequence is that the planner routes through 1.6–2.6 u shoals and the confessed
cheat controller (L1715) hides the resulting groundings — the planner causes the very events the
assist papers over. Consider draft-aware blocking with the inflation radius doing the
channel-keeping instead.

**[HIGH] Unreachable goal → full-component flood every second (L1135–1146, L1620–1624).**
`nearestFree` can snap a goal into a different connected component (strait sealed by inflation);
A* exhausts the start's component (~150–350k cells) before failing, and `maybeReplan` retries at
1 Hz (sub: 2.5 s). One flood-fill component labeling at grid build would memoize reachability.

**[MED]** Coarse hierarchical heuristic inadmissible — up to >5× overestimate across coarse
boundaries (L990–998, L1126); mitigated by hierNav defaulting off, except `dev.navBench()`
**permanently flips `P.hierNav = true` as a side effect (L5909)** — and baked scenarios ship
`hierNav: true` too, so this path is live in demos · sub planner swaps BLOCKED but reuses the
ship's coarse field + cache (L2534–2541) — wrong obstacle set under hierNav · `relaxPath` checks
vertices only; `uncrossPath` commits its detour point even when repair failed (L1091–1095) and
`simplifyPath` decimates by 4 without LOS on the fallback chord (L1108) — land-crossing segments
can survive to pursuit · sub grid rebuild is a synchronous ~1M-sample mid-frame hitch (L2486–2507)
· tour loop rebuilds per 0.1 tick of the current sliders because `tourKey` embeds them (L1601) ·
per-frame path-ribbon fill is O(dashes × path length), ~10⁶ iterations/frame on long tour paths
(L4089–4133) · ship grid samples one point per cell (sub grid ring-samples 7 for exactly this
reason) and the 2-ring inflation scales with map extent — can seal straits on big regions
(L941–967).

**[LOW]** `planThrough` ignores per-leg `found` → discontinuous splices (L1170) · zero-length
segment in `clearLOSseg` → `BLOCKED[NaN]` vacuously clear (L1103) · dead code: `catmull`/
`smoothPath` unreferenced (L1019–1041).

**Verified clean:** odd-r hex neighbor tables both parities, axial conversion + cube rounding
round-trips exactly; binary heap + lazy deletion + reused typed-array buffers; current penalty
only ever *adds* cost, so the Euclidean heuristic stays admissible in flat mode; `goalOpen`
semantics; try/finally grid swap for the sub.

## 3 · Rendering & performance

**[HIGH] Region-swap VRAM leak (L7736–7745).** Detach-only teardown is a documented trade
(disposing textures sampled by live materials → WebGPU weak-map crash), but the blast radius is
big: ~30–60 MB/swap (410k-tri ocean, 7×321² clipmap rings, 900×800 bathy DataTexture, label
CanvasTextures, flora InstancedMeshes), and demo mode swaps per scenario. Start with the safe
subset: **`_heightTex` is nulled without dispose (L7745) yet only region-owned materials sample
it — and `setTerrainLOD()` already disposes it safely (L5522)**. Clipmap/ocean geometries are
likewise region-owned. Dispose those; keep the shared-material textures leaked if needed.

**[HIGH] Permanent second shadow pass (L2307–2311).** `sun2Light.castShadow = true` forever
(WebGPU null-depthTexture workaround); three.js renders shadow maps for castShadow lights
regardless of intensity, so every Earth scene pays a 2048² full-scene pass every shadow frame
for a light at intensity 0. `Q.shadowSun2` shrinks it on low tiers but never to zero. Options:
keep the map allocated but toggle `shadow.autoUpdate`/light layers on Earth scenes, or gate the
scene's shadow-caster set.

**[MED]** Terrain/ocean vertex budget untiered: `CLIP_N = 320` × 7 rings ≈ 1.2M tris,
`frustumCulled = false`, `castShadow = true` → fully drawn into the 4096² map every shadow frame
+ main pass; ocean is 206k verts × 11-wave Gerstner in the vertex stage; `pixelCap` only scales
fragment work, so LOW/MOBILE still pay ULTRA vertex cost (L5527, L4865) · atmosphere post-chain
(godray march + full-res mip bloom + grade) is the default path; only tap count is tiered
(L1945, L6553) · Hokusai claws: ≤2600 finger placements × 4 iterative Gerstner calls + 333 KB/frame
instance upload, boolean tier lever only — but correctly style-gated (L4671–4744) ·
`updateReadouts` rebuilds `innerHTML` every frame (L8365, called at L1964).

**[LOW]** Dev beacons (telemetry POST @350 ms, reload poll @1 s) active on LAN/ts.net/cloudflare
hosts — the phone-demo path (L1783, L8462) · compass face fully re-stroked per frame (L8421) ·
debugNav rewrites both nav lines + bounding spheres per frame (L1364) · minor per-frame allocs
in descent/globe/claw paths (L1919, L4713, L7413).

**Verified clean:** scratch-object discipline keeps steady state allocation-free; boids bounded
(≤96 fish + 28 birds, within-school pair tests only); TEL/wake/FX pools all capped; no readbacks,
recompiles, or logs in the loop; all 10 `Q.*` levers verified wired; shadows half-rate; clipmap
displaces from baked texture with zero per-frame resample. PERF-FRAMEWORK's "ULTRA == old
literals" contract holds.

## 4 · GIS pipeline & data

**[HIGH] Stale bakes: `aegean.js`, `japan.js` have no `lonscale` key** (thailand too — harmless
at 8°N). All newer regions carry cos(lat0) to 5 decimals; Japan's perfectly square bathyMeta for
a 2°×2° tile proves lonscale=1 at 34.9°N (should be 0.82). Aegean ~25%, Japan ~22% E-W stretch;
distances and bearings anisotropic. Hardcoded Caribbean also uncorrected (~4.5% at 17°N).
Runtime is self-consistent (`REGION.lonscale ?? 1`, L738), so this is a regen, not a code fix.

**[HIGH] Star dome observer hardcoded: `OBS_LAT = 17.7°N, OBS_LON = -62°` (L4291)** for all 17
regions — Faroe (62°N) shows the Southern Cross with Polaris at 18°. The equatorial→horizontal
rotation itself is correct; wire it to `REGION.lat0/lon0`.

**[MED]** `gen_region.py:200` keeps one ring per land blob by max vertex count: interior lakes
are filled solid, and a convoluted lake shoreline can *replace* the outer coast; runtime even-odd
fill already supports holes — the generator doesn't emit them · shipped data not reproducible:
`sweden.js` contains "Ljusterö" but `KNOWN['sweden']` lacks it — naming table drifted since the
bake; a rerun renames islands · `dist/index.html` isn't self-contained: three.js importmap
(L263) and Tone.js (L3712) load from CDN at runtime — offline kiosk breaks · `pack.js:27` regex
silently skips script tags with extra attributes.

**[LOW]** "GEBCO 2024" comment vs 2026 grids; "0..60 units" comment vs `80*(1-exp)` actual ·
NODATA: -9999 decodes as 9999 m depth (`read_nc`); `read_asc` parses NODATA and never applies it ·
edge-of-tile: boundary vertices land half a cell outside the grid → sample the -4000 abyss
fallback → flattened rim (Japan's clipped islet) · `peak` array written, never read · `'c'` is
vertex-mean, not area centroid.

**Verified clean:** Int16 LE round-trip exact both sides; row0=NORTH consistent end-to-end;
grid-centre→corner registration exact; batch-2 extents match spec to within a cell; Float32
precision fine at ≤±1400 u; even-odd scanline fill winding-agnostic.

## 5 · Region review (names, palettes, geography)

Diacritics are remarkably good across all regions — Hawaiian ʻokina/kahakō, Vietnamese,
Faroese ð/ø, Swedish, Japanese macrons all correct. Pin lat/lons: all 18 verified plausible.

**[HIGH]** `hawaii` missing from REGION_META (L6972–6990; all 17 others present) — globe falls
back to bare `r.name`. (Softener: `.blurb` is dead data — written, never read.)

**[MED]** Aegean `windDirDeg: 115` contradicts its own "meltemi" comment — meltemi is N–NNE;
sibling trade-wind regions use 45–60 for NE, so ~0–30 fits the code's convention · Montauk:
"Ram Island" polygon is actually the Long Beach Point/Orient spit; real Ram Island is at
41.078N 72.305W · Apo: "Sumilon" label sits on an unnamed islet 6 km west of the real Sumilon,
which exists in the data unnamed at exactly (123.39, 9.43) — swap the labels · Exe region fuses
Lundy (Bristol Channel, north coast) with the Exe estuary (south coast): in-sim they connect
across what is really land, and Lundy is granite under a red-sandstone palette (the registry
comment admits it) · namesake islands unnamed `'islet'` polys: **Skye**, **Kodiak Island**,
**Siquijor** — the region titles promise them.

**[LOW]** "Stavsnäs" is a harbour village, not an island (→ Fågelbrolandet) · "Rinia" → Rineia ·
"James Bond I." → Ko Khao Phing Kan (nickname is fine for tourists, note the real name) ·
Solomon: Mbabanga plotted north of Ghizo, real one is SE lagoon; Kennedy I. ~3 km off · Aegean
includes tiny Kimolos but crops out adjacent, far larger Milos · Japan blurb promises Mt. Fuji;
none exists in-sim.

**REGION-AUDIT.md status:** fixed & verified — cold-water seaTints, per-region rock thresholds,
Aran limestone, Cape Cod sand+sage, Faroe emerald, Kodiak spruce, eased fog, Hạ Long steeper
towers, Aegean dry-gold + whitewash/blue-dome motifs. Partial — Hawaii black lava done,
windward/leeward split absent. Still open — Caribbean dry-island (Antigua/Barbuda) palette,
Sweden Falu-red / St. John's Jellybean Row / Cape Cod grey-shingle town colors, Skye heather,
Dauin black sand, darker Coron limestone.

## 6 · Audio, UI, telemetry graphs

**[HIGH] Heading conventions disagree in the UI (L8372).** The compass rose is a correct map
(needle, wind/current/setpoint arrows all verified in one consistent world→screen frame), but
the HUD prints raw math angle: a boat the compass shows pointing **N** reads **"hdg 270°"**;
0° = East. Same frame leaks into "Wind bearing" readout and `desiredHeadingDeg`. For a control
sim, the fix is one line where displayed: `bearing = (deg + 90 + 360) % 360` (and inverse on
input), or relabel honestly as math-frame.

**[HIGH] Audio init is unrecoverable (L3710–3716, L6241).** `_audioInit = true` is set *before*
the CDN import; gesture listeners self-remove on first gesture; nothing ever retries or calls
`ctx.resume()`. A failed Tone load (offline dist!) or iOS-suspended context = permanently silent
SFX while HTMLAudio music plays — easy to miss. Reset the flag on failure; resume on later
gestures.

**[HIGH] Restored toggles don't apply (L8348–8352).** `addToggle` only fires `onChange` on click,
so persisted "on" states render lit but inert after reload — this is precisely the known
alien-toggle quirk, and it applies to every toggle with a side effect. Invoke setters once after
`loadSettings()`.

**[MED]** Keyboard shortcuts ignore modifiers (Cmd/Ctrl+V triggers view switch, L6233) and
`typing()` whitelists only INPUT/TEXTAREA while the panel builds `<select>`s — arrows steer the
boat while a select is focused (L6220) · first click of a double-click fires `eruptVolcano()`,
which lacks the `VOLC_ENABLED` guard and latches the state machine in 'rumble' forever
(L6211–6218, L5315 vs L853) · `setPixelRatio` never refreshed on monitor change (L1801 vs L6141)
· recordings are silent — no `createMediaStreamDestination()` mix-in (L6369) · mid-recording
resize stretches footage (fixed recCanvas vs `drawImage` scale, L6363) · no-timeslice
`MediaRecorder` buffers ~120 MB/min at 16 Mbps (L6383) · `captureStream()` no-arg comment
describes `captureStream(0)` semantics; Safari path degrades to "Empty — no frames" (L6367).

**[LOW]** Graph x-axis is frame index, not time — window spans 2.7 s @120 Hz vs 5.3 s @60 Hz
(L8415) · one NaN poisons a polyline silently (L8413) · heading-error clamp ±90° flatlines at
the rail (L8395) · desired-heading arrow points East before guidance runs (L8450) · HUD canvases
have no DPR scaling — blurry on retina (L194, L8386) · muted synths run forever behind
`setMasterVolume(0)` · iOS ignores `HTMLMediaElement.volume` → ducking/fades are no-ops there ·
mixed localStorage namespaces + raw `Object.assign(P, parsed)` with no migration (L6587/L1763) ·
`saveSettings()` (full stringify) on every slider input tick (L8301) · no pointer capture on
look-drag (L6325) · tilt/fullscreen touch targets ~38–40 px vs 44 px guideline.

**Verified clean:** wrap-around heading plots draw no 359°→1° spike (error wrapped before
recording); P/I/D/out traces share one honest scale; labels are in-scene sprites so the
behind-camera HTML-projection bug class doesn't apply; listener synced to active camera;
region-bus audio fade; recorder mime ladder/4K cap/empty-blob guard all sound.

---

## Suggested fix order

**Afternoon 1 — correctness of the lesson (all small):** negate XTE (3 call sites share one
formula) · heading/bearing conversion at display+input · reset/clamp integrator on gain change ·
flag assist intervals in telemetry · apply toggle side effects after settings restore ·
add `hawaii` to REGION_META · meltemi wind bearing.

**Afternoon 2 — data regen:** re-bake aegean/japan (+ caribbean constant) with lonscale ·
reconcile `KNOWN` naming tables before regen (Ljusterö) · wire star dome to `REGION.lat0/lon0` ·
fix Ram Island/Sumilon label assignments; name Skye/Kodiak/Siquijor polys.

**Perf pass (biggest wins first):** dispose region-owned resources on swap (`_heightTex`,
clipmap + ocean geometries) · stop paying the companion-sun shadow pass on Earth scenes · put
CLIP_N / ocean grid / bloom chain on the QUALITY ladder · component-label the nav grid to
memoize unreachable goals · move sub-grid rebuild off the frame (amortize or idle-slice) ·
drop `tourKey`'s current-slider terms (or debounce) · incremental cursor for the path-ribbon
`at(s)` scan · `updateReadouts` only on value change.

**Housekeeping:** `dev.navBench()` restore `hierNav` · gate dev beacons to localhost · vendor
three.js + Tone into dist if "single portable file" is a real requirement · emit holes from
`gen_region.py` (runtime already supports even-odd) · fix doc drift (GEBCO year, compressM range).

---

## Addendum — fixes applied & validated (2026-07-01, same day)

Applied to `index.html` (uncommitted; `just pack` re-run → dist/ + docs/ updated): XTE sign
(both call sites) · HUD hdg → compass bearing; wind/current sliders display bearings (storage
unchanged) · Ki=0 integrator zeroing · assist honesty (speedWater to KF + amber telemetry bands)
· NaN-safe plot · meltemi 115→90 (default + 2 baked scenarios) · REGION_META.hawaii · star
observer follows REGION.lat0/lon0 · navBench hierNav restore · beacon/live-reload failure caps ·
audio init retry + context resume on gesture · modifier keys + `<select>` excluded from ship
controls · eruptVolcano VOLC_ENABLED guard · pixelRatio on resize · pointer capture on look-drag
· debounced saveSettings (cancelled in Reset-all) · teardown disposes safe subset (label
textures/materials, clipmap geometries, `_heightTex`) · companion-sun shadow pass skipped on
Earth via per-light `shadow.autoUpdate` · updateReadouts throttled ~7 Hz.

Validation: all inline scripts parse; 16/16 Node unit tests on the extracted PID/pursuit code
(old XTE sign parks 22u off-track at gain 0.04, 50u at lookahead 60; fix converges ~0 in all
cases; no Ki-restore slam; anti-windup intact; bearing table exact) · three r180 WebGPU
`ShadowNode.updateBefore` confirmed to gate on `needsUpdate||autoUpdate` · live in Chrome:
clean boot, compass↔hdg agreement checked at 110°/296°/266°, 5 region swaps (japan→hawaii→faroe→
aegean→caribbean) crash-free with disposal active at 84 fps after, alien mode works and now
restores correctly after reload (the old quirk was likely the demo-boot settings path), globe
shows the Hawaiʻi · The Islands pin, telemetry beacon verified against the running devserver.

NOT done in this pass (needs the data re-bake session): aegean/japan lonscale regen, lake holes,
Ram Island/Sumilon/namesake label fixes, CLIP_N/ocean/bloom tiering, A* component labeling,
recording audio track.

## Addendum 2 — data session (2026-07-01, evening)

Done and validated live: aegean + japan re-baked from GEBCO_2026.nc with lonscale (all names
reproduce; japan's KNOWN drift fixed — Kōzushima/Miyakejima/Shikinejima restored; Milos + Kea
now named on aegean); gen_region.py gained interior-lake detection (constant-elevation patches
in a depression, sealed lip vs the sea) emitting `hl` hole rings + area-based outer-ring pick +
size-scaled naming threshold (edge-clipped mainlands excluded); runtime scanline fill is even-odd
across outer+hole rings — Sørvágsvatn is carved on Vágar with its cliff lip intact; label fixes:
Sumilon→real islet, Siquijor/Skye/Kodiak named, montauk 'Ram Island'→'Orient Point' (tour updated
— GEBCO resolves no Ram Island blob). Remaining open: perf tiering (CLIP_N/ocean/bloom), A*
component labeling, recording audio, CDN-vendoring for dist.
