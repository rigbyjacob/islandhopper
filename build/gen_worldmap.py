#!/usr/bin/env python3
"""Bake a VIBRANT shaded-relief Earth COLOR texture + a DISPLACEMENT (height) texture
from the global GEBCO netCDF, for the world-map globe.
Outputs:
  data/worldmap.js       -> window.WORLDMAP      (color, jpeg data-uri)
  data/worldmap_disp.js  -> window.WORLDMAP_DISP (grayscale height, jpeg data-uri)
"""
import base64, io, numpy as np
from netCDF4 import Dataset
from PIL import Image
from scipy.ndimage import uniform_filter, gaussian_filter

STEP = 60   # 1440 x 720 — plenty for a globe
ds = Dataset('GEBCO/GEBCO_2026/GEBCO_2026.nc')
Zraw = np.asarray(ds.variables['elevation'][::STEP, ::STEP]).astype('float32')   # lat S->N
ds.close()
H, W = Zraw.shape
# Pre-smooth the elevation: at STEP=60 the bare GEBCO sampling reads as speckle / "GIS noise". A light
# gaussian blur of the SOURCE field gives a more polished, recognisable Earth for both colour & height.
Z = gaussian_filter(Zraw, sigma=0.5, mode='nearest')   # light source smooth (keeps the colour/coastlines crisp; the displacement gets its own smoothing below)
land = Z >= 0

# ---- COLOR (gentler relief shading + a final de-speckle blur for a cleaner, less noisy look) ----
d = np.clip(-Z, 0, 6000) / 6000.0                                  # ocean depth 0..1
shallow = np.array([46, 150, 176], np.float32); deep = np.array([12, 40, 104], np.float32)
ocean = shallow * (1 - d)[..., None] + deep * d[..., None]
e = np.clip(Z, 0, 4000) / 4000.0                                   # land elevation 0..1
low = np.array([78, 146, 70], np.float32); tan = np.array([190, 166, 102], np.float32)
high = np.array([146, 122, 92], np.float32); snow = np.array([240, 242, 246], np.float32)
t1 = np.clip(e / 0.35, 0, 1)[..., None]; t2 = np.clip((e - 0.35) / 0.45, 0, 1)[..., None]; t3 = np.clip((e - 0.82) / 0.18, 0, 1)[..., None]
landc = low * (1 - t1) + tan * t1
landc = landc * (1 - t2) + high * t2
landc = landc * (1 - t3) + snow * t3
img = np.where(land[..., None], landc, ocean)
# east-west hillshade for relief readability — gentler (less speckle)
gx = np.zeros_like(Z); gx[:, 1:] = Z[:, 1:] - Z[:, :-1]
shade = np.clip(1 + np.tanh(gx / 450.0) * 0.14, 0.86, 1.16)
img = img * shade[..., None]
# ambient occlusion (cavity): softer, so valleys/shelves don't read as grain
Zs = uniform_filter(Z, size=11, mode='nearest')
ao = np.clip(1 + (Z - Zs) / 220.0 * 0.32, 0.74, 1.06)
img = img * ao[..., None]
# mild saturation pop, then a light blur to polish out residual speckle
gray = img.mean(-1, keepdims=True)
img = np.clip(gray + (img - gray) * 1.10, 0, 255)
img = gaussian_filter(img, sigma=(0.25, 0.25, 0), mode='nearest')   # light de-speckle only (was 0.7 — too blurry)
img = np.clip(img, 0, 255).astype(np.uint8)[::-1]                  # flip so top = north

# ---- DISPLACEMENT (sea level = mid-grey 0.5; COMPRESSED so the globe reads as Earth, not a knobbly potato) ----
# land range compressed (÷5500 + 0.8 power → highs pulled down); ocean barely sunk; then smoothed.
land_h = np.clip(Z / 5500.0, 0, 1) ** 0.8
sea_h  = np.clip(-Z / 8000.0, 0, 1) ** 0.9
disp = np.where(land, 0.5 + 0.42 * land_h, 0.5 - 0.30 * sea_h)
disp = gaussian_filter(disp, sigma=1.5, mode='nearest')           # smooth the height field (no spiky relief)
disp = np.clip(disp * 255, 0, 255).astype(np.uint8)[::-1]

def datauri(arr, mode, q):
    im = Image.fromarray(arr, mode); buf = io.BytesIO(); im.save(buf, format='JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')

cj = datauri(img, 'RGB', 88); dj = datauri(disp, 'L', 90)
open('data/worldmap.js', 'w').write('window.WORLDMAP="' + cj + '";\n')
open('data/worldmap_disp.js', 'w').write('window.WORLDMAP_DISP="' + dj + '";\n')
print(f'worldmap {W}x{H}  land {land.mean()*100:.1f}%  color {len(cj)/1024:.0f}KB  disp {len(dj)/1024:.0f}KB')
