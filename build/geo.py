# -*- coding: utf-8 -*-
"""裁剪 Natural Earth 为轻量离线 GeoJSON，供 Leaflet 在瓦片失败时作底图。"""
import json, os
from shapely.geometry import shape, box, mapping, LineString, Polygon, MultiPolygon, MultiLineString
NE = os.environ.get("NE_DIR", "/workspace/ne")
def _load(n):
    return json.load(open(os.path.join(NE, n + ".geojson")))
def _feats(src, B, simplify, minarea=0, kind="land", names=None, name_keys=("name","name_en")):
    out = []
    for f in src["features"]:
        if names is not None:
            pr = f.get("properties") or {}
            if not any((pr.get(k) or "") in names for k in name_keys):
                continue
        g = shape(f["geometry"])
        if not g.intersects(B): continue
        g = g.intersection(B)
        if simplify: g = g.simplify(simplify, preserve_topology=True)
        if g.is_empty: continue
        geoms = list(g.geoms) if hasattr(g, "geoms") else [g]
        for p in geoms:
            if p.geom_type in ("Polygon","MultiPolygon") and p.area < minarea: continue
            if p.geom_type in ("LineString","MultiLineString") and p.length < simplify * 2: continue
            out.append({"type":"Feature","properties":{"k":kind},"geometry":mapping(p)})
    return out
RIVERS = {"Jordan","Nile","Euphrates","Firat","Al Furat","Tigris","Dicle","Orontes","Rhine"}  # reused names
def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    specs = {
        "levant": dict(bbox=(33.4, 30.4, 37.4, 34.1), land="ne_10m_land", lake="ne_10m_lakes", riv="ne_10m_rivers_lake_centerlines", simp=.003, minarea=0.00002),
        "ane":    dict(bbox=(24.0, 12.0, 74.0, 44.5), land="ne_110m_land", lake="ne_50m_lakes", riv="ne_10m_rivers_lake_centerlines", simp=.08, minarea=0.04),
    }
    riv_ok = {"Jordan","Nile","Euphrates","Firat","Al Furat","Tigris","Dicle","Orontes","Rosetta Branch","Damietta Branch"}
    sizes = {}
    for k, s in specs.items():
        w,s0,e,n = s["bbox"]; B = box(w,s0,e,n)
        feats = []
        feats += _feats(_load(s["land"]), B, s["simp"], s["minarea"], "land")
        feats += _feats(_load(s["lake"]), B, s["simp"], s["minarea"]/4, "lake")
        feats += _feats(_load(s["riv"]), B, s["simp"]*0.6, 0, "river", names=riv_ok)
        path = os.path.join(outdir, k + ".json")
        json.dump({"type":"FeatureCollection","features":feats}, open(path,"w"), separators=(",",":"))
        sizes[k] = os.path.getsize(path)
    return sizes
if __name__ == "__main__":
    print(build("/workspace/OT-Historical-Books-GROKstudy/docs/assets/geo"))
