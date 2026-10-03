"""Verify exported file completeness and height bounds, independently of renderer."""
from pathlib import Path
import json,csv,re,ast
R=Path(__file__).resolve().parents[1]
G=json.loads((R/'data/geometry.json').read_text());C=json.loads((R/'data/checks.json').read_text());M=json.loads((R/'data/model-manifest.json').read_text())
assert C['passed']==C['total']
with (R/'data/floor-schedule.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
assert len(rows)==160
for k,target in [('A',328000),('D',142000)]:assert abs(sum(float(r['slab_area']) for r in rows if r['tower']==k)-target)<.01
vertices=[];groups={};current=None;face_count=0
for line in (R/'model/hoi-luu-r1.obj').read_text().splitlines():
    p=line.split()
    if not p:continue
    if p[0]=='v':vertices.append(tuple(map(float,p[1:])))
    elif p[0]=='o':current=p[1];groups[current]=set()
    elif p[0]=='f':
        ids=[int(x)-1 for x in p[1:]];assert all(0<=i<len(vertices) for i in ids);groups[current].update(ids);face_count+=1
assert len(vertices)==M['vertices'] and face_count==M['faces']
assert set(groups)=={x['name'] for x in M['objects']}
heights={}
for k in ['A','D']:
    ids={i for name,index in groups.items() if name.startswith(k+'_') for i in index}
    heights[k]=max(vertices[i][2] for i in ids)
    assert abs(heights[k]-G['towers'][k]['crown_z'])<.001
for p in (R/'scripts').glob('*.py'):ast.parse(p.read_text())
report=(R/'HOI_LUU_R1.html').read_text()
assert report.count('data:image/svg+xml;base64,')==6
assert len(re.findall(r'<h1\b',report))==10
result={'geometry_checks':f"{C['passed']}/{C['total']}",'floor_rows':len(rows),'OBJ_objects':len(groups),'OBJ_vertices':len(vertices),'OBJ_faces':face_count,'OBJ_finished_heights':heights,'embedded_drawings':6,'chapters':10,'python_syntax':'pass','Blender_execution':'not performed'}
(R/'data/release-validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps(result,ensure_ascii=False))
