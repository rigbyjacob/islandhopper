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
from scipy.ndimage import uniform_filter

STEP = 60   # 1440 x 720 — plenty for a globe
ds = Dataset('GEBCO/GEBCO_2026/GEBCO_2026.nc')
Z = np.asarray(ds.variables['elevation'][::STEP, ::STEP]).astype('float32')   # lat S->N
ds.close()
H, W = Z.shape
land = Z >= 0

# ---- vibrant COLOR ----
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
# east-west hillshade for relief readability
gx = np.zeros_like(Z); gx[:, 1:] = Z[:, 1:] - Z[:, :-1]
shade = np.clip(1 + np.tanh(gx / 350.0) * 0.22, 0.78, 1.25)
img = img * shade[..., None]
# ambient occlusion (cavity): darken where ground sits below its neighbourhood (valleys, shelves, trenches)
Zs = uniform_filter(Z, size=11, mode='nearest')
ao = np.clip(1 + (Z - Zs) / 170.0 * 0.5, 0.6, 1.08)
img = img * ao[..., None]
# moderate saturation pop (between grim and neon)
gray = img.mean(-1, keepdims=True)
img = np.clip(gray + (img - gray) * 1.18, 0, 255)
img = np.clip(img * 1.0, 0, 255).astype(np.uint8)[::-1]            # flip so top = north

# ---- DISPLACEMENT (sea level = mid-grey; land up 0.5..1.0, ocean sunk 0.5..0.0 with real bathymetry) ----
disp = np.where(land, 0.5 + 0.5 * np.clip(Z / 4000.0, 0, 1), 0.5 - 0.5 * np.clip(-Z / 6000.0, 0, 1))
disp = np.clip(disp * 255, 0, 255).astype(np.uint8)[::-1]

def datauri(arr, mode, q):
    im = Image.fromarray(arr, mode); buf = io.BytesIO(); im.save(buf, format='JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')

cj = datauri(img, 'RGB', 88); dj = datauri(disp, 'L', 90)
open('data/worldmap.js', 'w').write('window.WORLDMAP="' + cj + '";\n')
open('data/worldmap_disp.js', 'w').write('window.WORLDMAP_DISP="' + dj + '";\n')
print(f'worldmap {W}x{H}  land {land.mean()*100:.1f}%  color {len(cj)/1024:.0f}KB  disp {len(dj)/1024:.0f}KB')
