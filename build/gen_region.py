#!/usr/bin/env python3
"""
gen_region.py — turn a GEBCO Esri-ASCII (.asc) tile into a PID Helmsman region blob.

A "region" is a self-contained map: equirectangular projection (x=(lon-lon0)*K,
z=-(lat-lat0)*K), the raw GEBCO bathymetry grid (Int16 metres, row0=NORTH), and
named island coastline polygons (the 0 m contour, in world coords).

Output: data/<id>.js  ->  window.<UPPER_ID> = { id,name,K,lon0,lat0,palette,
                                                 bathyMeta, bathyB64, islandPolys }

Usage:
  python3 build/gen_region.py --asc <file.asc> --id aegean --name "Aegean (Cyclades)" \
      --K 700 --lon0 25.5 --lat0 37.0

ELEV is intentionally NOT emitted: the app falls back to sampling land elevation
straight from the GEBCO grid when a region has no elevB64.
"""
import argparse, base64, json, numpy as np
from scipy import ndimage
from skimage import measure

# Known island centroids (lon,lat) for auto-naming. Add regions as needed.
KNOWN = {
  'aegean': {
    'Santorini': (25.43, 36.41), 'Thirasia': (25.33, 36.43), 'Mykonos': (25.33, 37.45),
    'Delos': (25.27, 37.39), 'Rinia': (25.22, 37.41), 'Naxos': (25.48, 37.07),
    'Paros': (25.15, 37.08), 'Antiparos': (25.03, 37.03), 'Ios': (25.28, 36.72),
    'Syros': (24.92, 37.44), 'Tinos': (25.16, 37.58), 'Sifnos': (24.67, 36.97),
    'Serifos': (24.50, 37.15), 'Folegandros': (24.92, 36.62), 'Sikinos': (25.10, 36.69),
    'Amorgos': (25.90, 36.85), 'Kimolos': (24.57, 36.80), 'Iraklia': (25.46, 36.84),
    'Schoinoussa': (25.52, 36.86), 'Koufonisia': (25.60, 36.94), 'Kea': (24.34, 37.62),
    'Andros': (24.90, 37.84), 'Donousa': (25.81, 37.10),
  },
  'japan': {
    'Izu Ōshima': (139.39, 34.74), 'Toshima': (139.28, 34.52), 'Enoshima': (139.48, 35.30),
    'Hatsushima': (139.17, 35.04), 'Jōgashima': (139.61, 35.13), 'Niijima': (139.27, 34.38),
  },
  'thailand': {
    'Phuket': (98.34, 7.92), 'Ko Yao Yai': (98.60, 8.12), 'Ko Yao Noi': (98.62, 8.21),
    'Ko Phi Phi': (98.77, 7.74), 'Ko Lanta': (99.05, 7.58), 'Ko Racha': (98.36, 7.61),
    'Ko Naka': (98.43, 8.03), 'James Bond I.': (98.50, 8.27),
  },
  'sweden': {   # Stockholm archipelago (Värmdö): the Djurö–Djurhamn–Stavsnäs run + neighbours
    'Djurö': (18.555, 59.300), 'Stavsnäs': (18.695, 59.285), 'Runmarö': (18.700, 59.300),
    'Nämdö': (18.680, 59.180), 'Vindö': (18.500, 59.340), 'Möja': (18.900, 59.400),
    'Sandön': (18.920, 59.290), 'Ingarö': (18.420, 59.270), 'Gällnö': (18.620, 59.370),
    'Fågelbrolandet': (18.660, 59.300),
  },
  'hawaii': {   # the main Hawaiian Islands
    "Hawaiʻi": (-155.50, 19.60), 'Maui': (-156.33, 20.80), "Oʻahu": (-157.97, 21.46),
    "Kauaʻi": (-159.50, 22.05), "Molokaʻi": (-157.02, 21.13), "Lānaʻi": (-156.92, 20.83),
    "Niʻihau": (-160.16, 21.90), "Kahoʻolawe": (-156.60, 20.55),
  },
  'halong': {   # Hạ Long Bay + Lan Ha + inner Bai Tu Long karst (lon,lat)
    'Cát Bà': (107.011, 20.795), 'Bồ Hòn': (107.100, 20.883), 'Ti Tốp': (107.056, 20.901),
    'Đầu Gỗ': (107.042, 20.908), 'Đầu Bê': (107.145, 20.795), 'Cát Dứa': (106.998, 20.777),
    'Trống Mái': (107.035, 20.910), 'Cống Đỏ': (107.210, 20.840), 'Ngọc Vừng': (107.400, 20.865),
  },
}

def read_asc(path):
    hdr = {}
    with open(path) as fh:
        for _ in range(6):
            k, v = fh.readline().split(); hdr[k] = float(v)
        Z = np.loadtxt(fh)
    return hdr, Z  # Z[row,col], row0 = NORTH

def read_nc(path, N, S, W, E):
    """Slice a bbox straight out of a global GEBCO netCDF (e.g. GEBCO_2026.nc).
    netCDF4 index-slicing reads only the window's chunks, NOT the whole 7 GB file."""
    from netCDF4 import Dataset
    ds = Dataset(path)
    lat = ds.variables['lat'][:]; lon = ds.variables['lon'][:]
    cs = float(abs(lat[1] - lat[0]))
    li = np.where((lat >= S) & (lat <= N))[0]
    ci = np.where((lon >= W) & (lon <= E))[0]
    if not len(li) or not len(ci):
        raise SystemExit('bbox does not intersect the grid')
    la0, la1 = int(li[0]), int(li[-1]) + 1
    co0, co1 = int(ci[0]), int(ci[-1]) + 1
    Z = np.ma.filled(ds.variables['elevation'][la0:la1, co0:co1], -9999).astype('float64')
    Z = Z[::-1]                                   # GEBCO lat ascends S→N; flip so row0 = NORTH
    nrows, ncols = Z.shape
    hdr = {'ncols': ncols, 'nrows': nrows,
           'xllcorner': float(lon[co0]) - cs/2.0, 'yllcorner': float(lat[la0]) - cs/2.0,
           'cellsize': cs, 'NODATA_value': -32767}
    ds.close()
    return hdr, Z

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--asc', help='an Esri-ASCII .asc tile')
    ap.add_argument('--nc', help='a (global) GEBCO netCDF to slice from, e.g. GEBCO/GEBCO_2026/GEBCO_2026.nc')
    ap.add_argument('--bbox', nargs=4, type=float, metavar=('N','S','W','E'), help='lat/lon window when using --nc')
    ap.add_argument('--id', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--K', type=float, required=True)
    ap.add_argument('--lon0', type=float, required=True)
    ap.add_argument('--lat0', type=float, required=True)
    ap.add_argument('--lonscale', type=float, default=None,
                    help='east-west scale for longitude (default cos(lat0)). Corrects the 2x E-W stretch at high latitudes; pass 1.0 for the old uncompensated behaviour')
    ap.add_argument('--min-cells', type=int, default=4, help='drop land blobs smaller than this')
    ap.add_argument('--simplify', type=float, default=1.2, help='coastline simplify tolerance (px)')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()

    if a.nc:
        if not a.bbox: raise SystemExit('--nc requires --bbox N S W E')
        hdr, Z = read_nc(a.nc, *a.bbox)
    elif a.asc:
        hdr, Z = read_asc(a.asc)
    else:
        raise SystemExit('provide --asc <file> OR --nc <global.nc> --bbox N S W E')
    nrows, ncols = int(hdr['nrows']), int(hdr['ncols'])
    cs, x0c, y0c = hdr['cellsize'], hdr['xllcorner'], hdr['yllcorner']
    K, lon0, lat0 = a.K, a.lon0, a.lat0
    lonscale = a.lonscale if a.lonscale is not None else float(np.cos(np.radians(lat0)))  # cos(lat0): keep E-W:N-S isometric

    # index (row r from north, col c) -> lon/lat of the CELL CENTRE -> world (x,z)
    def lonlat(r, c):
        lon = x0c + (c + 0.5) * cs
        lat = y0c + (nrows - r - 0.5) * cs
        return lon, lat
    def world(r, c):
        lon, lat = lonlat(r, c)
        return (lon - lon0) * K * lonscale, -(lat - lat0) * K

    # ---- BATHY grid: Int16 metres, row0=north, row-major (matches decodeElev) ----
    Zi = np.clip(np.nan_to_num(Z, nan=-9999), -32767, 32767).astype('<i2')
    bathy_b64 = base64.b64encode(Zi.tobytes()).decode('ascii')
    x0, _ = world(0, 0);          x1, _ = world(0, ncols - 1)
    _, zN = world(0, 0);          _, zS = world(nrows - 1, 0)
    bathy_meta = {'w': ncols, 'h': nrows,
                  'x0': round(x0, 2), 'x1': round(x1, 2),
                  'zN': round(zN, 2), 'zS': round(zS, 2)}

    # ---- ISLAND_POLYS: 0 m coastline of each connected land blob, in world coords ----
    land = Z >= 0
    lbl, n = ndimage.label(land, structure=np.ones((3, 3)))  # 8-connectivity
    known = KNOWN.get(a.id, {})
    polys, named = [], {}
    for k in range(1, n + 1):
        comp = lbl == k
        if comp.sum() < a.min_cells:
            continue
        # pad so the coastline of edge-touching blobs still closes
        padded = np.pad(comp.astype(float), 1)
        contours = measure.find_contours(padded, 0.5)
        if not contours:
            continue
        contour = max(contours, key=len)  # outer ring (largest)
        contour = measure.approximate_polygon(contour, a.simplify)
        if len(contour) < 4:
            continue
        ring = [[round(v, 1) for v in world(rr - 1, ccc - 1)] for rr, ccc in contour]  # undo pad
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        cx = round(sum(p[0] for p in ring) / len(ring), 1)
        cz = round(sum(p[1] for p in ring) / len(ring), 1)
        peak_m = float(Z[comp].max())
        # centroid lon/lat for naming
        rr, ccx = ndimage.center_of_mass(comp)
        clon, clat = lonlat(rr, ccx)
        name = 'islet'
        best = 0.08  # deg threshold
        for nm, (klon, klat) in known.items():
            d = ((clon - klon) ** 2 + (clat - klat) ** 2) ** 0.5
            if d < best and nm not in named:
                best, name = d, nm
        if name != 'islet':
            named[name] = True
        polys.append({'n': name, 'h': round(peak_m / 50, 1), 'c': [cx, cz], 'r': ring})

    polys.sort(key=lambda p: -len(p['r']))
    region = {
        'id': a.id, 'name': a.name, 'K': K, 'lon0': lon0, 'lat0': lat0, 'lonscale': round(lonscale, 5),
        'bathyMeta': bathy_meta, 'islandPolys': polys, 'bathyB64': bathy_b64,
    }
    out = a.out or f'data/{a.id}.js'
    var = a.id.upper()
    body = json.dumps(region, separators=(',', ':'))
    with open(out, 'w') as fh:
        fh.write(f'window.{var}={body};\n')

    named_list = sorted([p['n'] for p in polys if p['n'] != 'islet'])
    print(f'[{a.id}] grid {ncols}x{nrows}  depth {Z.min():.0f}..{Z.max():.0f} m')
    print(f'  bathyMeta {bathy_meta}')
    print(f'  land blobs total {n}, kept {len(polys)} (>= {a.min_cells} cells)')
    print(f'  named islands ({len(named_list)}): ' + ', '.join(named_list))
    print(f'  wrote {out}  ({len(body)/1024:.0f} KB)')

if __name__ == '__main__':
    main()
