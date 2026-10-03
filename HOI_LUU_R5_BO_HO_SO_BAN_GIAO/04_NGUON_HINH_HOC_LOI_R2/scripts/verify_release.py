from pathlib import Path
import hashlib,json,csv,re
R=Path(__file__).resolve().parents[1]
s=json.loads((R/'data/r2-study.json').read_text());g=json.loads((R/'data/geometry-r2.json').read_text());h=(R/'HOI_LUU_R2.html').read_text()
assert all(c['passed'] for c in s['checks'])
assert len(s['banks'])+len(s['shuttles'])==17
assert h.count('<svg')==6 and '<img' not in h
assert len(g['floors'])==160
assert len(list(csv.DictReader((R/'data/core-floor-schedule.csv').open())))==160
assert len(list(csv.DictReader((R/'data/traffic-banks.csv').open())))==17
for t,budget in [('A',300000),('D',120000)]:
    assert abs(sum(f['slab_area'] for f in g['floors'] if f['tower']==t and f['kind']=='body')-budget)<1e-5
for rel,digest in json.loads((R/'data/manifest.json').read_text()).items():assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==digest,rel
for level in [32,56,80]:assert f'01 → {level:02d}' in h
result={'passed':True,'geometry_arithmetic_checks':len(s['checks']),'traffic_groups':17,'floor_rows':160,'embedded_vector_drawings':6,'scope':'concept geometry and preliminary traffic screen only; no legal/structural/vendor validation'}
(R/'data/release-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
