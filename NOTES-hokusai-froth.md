# Hokusai wave froth / "frilly fingers" — what worked and what didn't

Retro on the attempt to reproduce *The Great Wave*'s curling white foam claws on the
real-time WebGPU ocean. Captured so we don't re-walk the same dead ends.

## The core obstacle (the thing to internalize)
The open-ocean surface is **gentle, low-amplitude, smooth swells**. There is no steep
breaking face. Foam needs a **sharp spatial gradient** to read as crisp claws; smooth
swells give broad, flat "crest" plateaus, so anything keyed to wave height spreads into
soft pools. Every open-water failure below traces back to this.

The tell: **the shoreline froth DID read as fingers.** It's keyed to a strong, well-defined
*shore-proximity* gradient (`sp`) with a travelling-sine "lap" and noise breakup. Strong
gradient → localized, crisp, finger-like froth. That's the model to copy for open water.

## What worked (keep)
- **Deep-blue palette driven by WAVE HEIGHT, not water depth.** Deep Prussian indigo
  `#102856` troughs → cobalt `#264f94` → pale `#A7C7E7` only at crest tips. Bias the
  height→ramp input dark (`smoothstep(-0.2, 2.6, wh)`) so ordinary water sits deep. This is
  the big win and reads as Hokusai's sea.
- **Flatten the glossy reflections under Hokusai** (`hkFlat` suppresses fresnel sky-sheen +
  sun glitter). Ukiyo-e is flat painted colour, not glossy water. Without this the deep blue
  washed pale toward the cream sky.
- **Warm cream sky + warm cream foam** (unbleached-paper tone), not cold blue-white.
- **Shoreline froth** (`shoreFoam`) — the one foam that looks right. Strong gradient + lap.

## What didn't work (don't repeat)
- **Wave-height threshold → white foam.** Broad soft pools. Smooth crests = broad fill.
- **Smooth-fbm contour / level-set "lines"** (`1 - smoothstep(0, w, abs(noise - level))`).
  Looks right in theory, but the noise gradient is shallow, so level sets are spatially fat
  → pools, not thin lines.
- **Ridged turbulence** (`1 - |2n - 1|`, octave-stacked) thresholded high. Still pooled at
  this wave scale; threshold values are guesswork without seeing the noise distribution.
- **Painted white foam with no edge.** White-on-white / white-on-pale is invisible. (User's
  key insight: the foam needs a *dark rim* to be legible — the print's keyblock outline.)
- **Shader "keyline"** (dark rim from a second offset threshold band). Never produced a
  visible rim — the rim width depended on the same shallow noise gradient.
- **Texture-stamped claws WITH mipmaps.** Mip-blur ate the thin dark keyline at distance →
  back to soft white blobs.
- **Texture-stamped claws, mipmaps OFF + thick keyline + bigger claws.** Still didn't read as
  outlined claws, and `minFilter=Linear` + `anisotropy 8` on a fullscreen water sample cost
  perf for no visible gain. (Revert this — re-enable mipmaps or drop the texture path.)

## THE BREAKTHROUGH (what finally worked)
Two diagnostic questions from the user cracked it: *"isn't it suspicious we can't see the
froth even rendered in dark ink?"* and *"is it rendering below the white surface?"*

Acting on that, we rendered the raw froth field **ungated in pure RED** — and the whole sea
lit up with rich, crisp, lacy red froth. So **the froth signal was reaching the screen the
whole time, in abundance.** Every prior failure was never the noise — it was **colour-on-
same-colour**:
- dark ink `#0b1c41` ≈ the deep-water indigo `#102856` → dark-on-dark, invisible.
- white foam ≈ the pale crest tops → white-on-white, invisible.
- plus the crest gate keyed on `n.y` (slope), which **barely fires on flat swells**, so foam
  never reached the high-contrast spots anyway.

The fix that worked:
1. **WHITE claw core + a slightly WIDER DARK-INDIGO rim.** Draw the wider dark mask first,
   then the narrower white core on top — the exposed dark ring *is* the woodblock keyline.
   `inkMask = smoothstep(0.40,0.47, froth)`, `whiteMask = smoothstep(0.50,0.57, froth)`.
2. **Gate by WAVE HEIGHT, not slope.** `smoothstep(-0.15,1.05, wh)` fires on flat water;
   `n.y` does not.
3. The froth field itself: warped fbm, `fbm2(xz*0.40 + domainWarp + drift)`, tight threshold.

Lesson to carry: **when an effect is "invisible," prove the signal first** (render it raw in
a contrasting debug colour) before tuning aesthetics. We burned ~12 iterations tuning colour
and thresholds when a 1-line red debug would have shown the field was fine on attempt #2.

## What to try next (ranked by promise)
1. **Copy the shoreline-froth recipe to open water.** Build a synthetic high-contrast
   "pseudo-shore" field for the crests — e.g. a sharp distance-field-like function of a
   warped noise, animated with a travelling lap — and gate froth on *that* gradient, not on
   wave height. The froth that already works proves this is the right lever.
2. **Real geometry, not paint.** Displace the crests with fine ridged noise so they actually
   break — but the water mesh is `PlaneGeometry(5600×4000, 540×380)` ≈ **10 units/quad**, far
   coarser than the ~2–4-unit claws. Needs a big tessellation bump (or a camera-local
   high-res patch / LOD) **plus** recomputed normals so lighting catches the relief. Biggest
   change, highest fidelity.
3. **SDF foam texture + fwidth AA.** Encode claws as a signed-distance field in the texture
   and reconstruct crisp, mip-stable edges with screen-space `fwidth`. Keeps edges sharp at
   any distance without the perf hit of mipmaps-off.
4. **Alpha-tested foam decals** stamped along crest lines (billboard/decal), art-authored
   with the keyline baked in — closest to the print, sidesteps the smooth-water problem.

## Perf note
Revert the foam texture's `generateMipmaps=false` / `minFilter=Linear` / `anisotropy=8` — it
regressed perf with no visible benefit. If we keep a foam texture, mipmap it and solve edge
crispness with an SDF (#3) instead.
