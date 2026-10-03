"""HOI LUU R1 — deterministic concept geometry, metres. Python 3 + shapely.
Run from package root: python scripts/build_geometry.py
Not a structural analysis or code-compliance model.
"""
from pathlib import Path
import math,json,csv,re,hashlib
from shapely.geometry import Polygon,LineString,box,Point,mapping
from shapely.ops import unary_union
from shapely.affinity import translate

ROOT=Path(__file__).resolve().parents[1]
N=256
def area(pts): return Polygon(pts).area
def rr(w,h,r,n=N):
    # Analytic rounded rectangle sampled by perimeter length, CCW, start right midpoint.
    import numpy as np
    lens=[h/2-r,math.pi*r/2,w-2*r,math.pi*r/2,h-2*r,math.pi*r/2,w-2*r,math.pi*r/2,h/2-r]
    ends=np.cumsum(lens); ss=np.arange(n)*sum(lens)/n
    xy=np.zeros((n,2)); starts=np.r_[0,ends[:-1]]
    for k in range(9):
        mask=(ss>=starts[k])&(ss<ends[k]+1e-10); u=(ss[mask]-starts[k])/lens[k]
        if k==0: x=np.full_like(u,w/2);y=u*(h/2-r)
        elif k==1: t=u*math.pi/2;x=w/2-r+r*np.cos(t);y=h/2-r+r*np.sin(t)
        elif k==2: x=w/2-r-u*(w-2*r);y=np.full_like(u,h/2)
        elif k==3: t=math.pi/2+u*math.pi/2;x=-w/2+r+r*np.cos(t);y=h/2-r+r*np.sin(t)
        elif k==4: x=np.full_like(u,-w/2);y=h/2-r-u*(h-2*r)
        elif k==5: t=math.pi+u*math.pi/2;x=-w/2+r+r*np.cos(t);y=-h/2+r+r*np.sin(t)
        elif k==6: x=-w/2+r+u*(w-2*r);y=np.full_like(u,-h/2)
        elif k==7: t=3*math.pi/2+u*math.pi/2;x=w/2-r+r*np.cos(t);y=-h/2+r+r*np.sin(t)
        else:x=np.full_like(u,w/2);y=-h/2+r+u*(h/2-r)
        xy[mask,0]=x;xy[mask,1]=y
    return xy.tolist()
def scallop(pts,depth):
    out=[]
    for x,y in pts:
        theta=math.atan2(y,x)
        d=min(abs((theta-k*math.pi/2+math.pi)%(2*math.pi)-math.pi) for k in range(4))
        radius=math.hypot(x,y)
        f=1-depth*math.exp(-(d/.14)**2)/radius
        out.append([x*f,y*f])
    return out
def move(pts,c):return [[x+c[0],y+c[1]] for x,y in pts]
def solve(fn,target,lo=.08,hi=12):
    a,b=fn(lo),fn(hi)
    if not min(a,b)<=target<=max(a,b):raise ValueError((target,a,b))
    for _ in range(70):
        mid=(lo+hi)/2
        if (fn(mid)<target)==(a<b):lo=mid
        else:hi=mid
    return (lo+hi)/2
def rect(x,y,w,h):return [[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
def geodict(g):return mapping(g)

site=box(0,0,295,155); basement=box(10,10,285,145)
Bpod=Polygon([(99,96),(150,96),(162,108),(162,144),(87,144),(87,108)])
Cpod=Polygon([(138,12),(205,12),(205,42),(185,62),(128,62),(128,22)])
Bpts=[[94+x,102+y] for x,y in [(0,0),(32,0),(32,6),(60,6),(60,36),(28,36),(28,30),(0,30)]]
Cpts=[[194-x,53-y] for x,y in [(0,0),(32,0),(32,6),(60,6),(60,36),(28,36),(28,30),(0,30)]]
centers={'A':[53,49],'D':[238,104],'B':[124,120],'C':[164,35]}
pod_h=[6,5.4,5.4,5.4,5.4,6.4]
poddefs={
 'A':dict(outer=[5800,5750,5500,5200,4900,4600], widths=[86,85.4,82,78,75,72], radii=[18,18,18,17,16.5,16], cx=[57,57,56,55,54,53], cy=49, deductions=[300,1950,500,400,300,300]),
 'D':dict(outer=[4500,4450,4250,3900,3450,3000], widths=[78,77.5,75,72,68,64], radii=[16,16,15,14,13,12], cx=[232,232,233,235,237,238], cy=104, deductions=[100,800,200,150,150,150])}
pods={}; floors=[]
for name,d in poddefs.items():
    z=0;rows=[]
    for i in range(6):
        w,r=d['widths'][i],d['radii'][i]
        h=solve(lambda h:area(rr(w,h,r)),d['outer'][i],2*r+.01,100)
        pts=move(rr(w,h,r),[d['cx'][i],d['cy']]); outer=Polygon(pts)
        # Explicit openings grouped on plaza-facing side; these are program reserves.
        # A L2 large subtraction is a double-height arrival hall + atrium reserve.
        core=box(centers[name][0]-(17 if name=='A' else 13),centers[name][1]-(16 if name=='A' else 12),centers[name][0]+(17 if name=='A' else 13),centers[name][1]+(16 if name=='A' else 12))
        if name=='A':
            zone=outer.difference(core.buffer(1)).intersection(box(centers[name][0]+18,-100,400,300))
            if zone.area<d['deductions'][i]:
                zone=outer.difference(core.buffer(1))
            # Cut a deterministic fraction by x; resulting polygon(s) are stored explicitly.
            threshold=solve(lambda x:zone.intersection(box(x,-100,400,300)).area,d['deductions'][i],-100,400)
            holes=zone.intersection(box(threshold,-100,400,300))
        else:
            zone=outer.difference(core.buffer(1))
            threshold=solve(lambda x:zone.intersection(box(-100,-100,x,300)).area,d['deductions'][i],-100,400)
            holes=zone.intersection(box(-100,-100,threshold,300))
        row={'tower':name,'floor':i+1,'kind':'podium','z':z,'height':pod_h[i],'top':z+pod_h[i],
             'w':w,'h':h,'r':r,'center':[d['cx'][i],d['cy']],'outer':pts,'void_geometry':geodict(holes),
             'envelope_area':outer.area,'void_area':holes.area,'slab_area':outer.area-holes.area,
             'program':'Mall + private arrival/support reserve','core_local':[-17,-16,34,32] if name=='A' else [-13,-12,26,24]}
        rows.append(row);floors.append(row);z+=pod_h[i]
    pods[name]=rows

A_special={7:6,31:6,32:6,55:6,56:6,79:6,80:6,98:6.8}
A=[];z=sum(pod_h)
for f in range(7,99):
    h=A_special.get(f,4.4)
    core=([-17,-16,34,32] if f<31 else [-15,-14,30,28] if f<55 else [-14,-13,28,26] if f<79 else [-12,-12,24,24])
    A.append({'tower':'A','floor':f,'kind':'body','z':z,'height':h,'top':z+h,'center':centers['A'],
              'voids_local':[rect(18,-8,6,16)] if f in [32,56,80] else [],'core_local':core,
              'program':'MEP/refuge/outrigger reservation' if f in [31,55,79,98] else 'Sky lobby/support' if f in [7,32,56,80] else 'Office'})
    z+=h
Aroof=z
def aprofile(t,p):
    t=max(0,min(1,t));q=t**p;w=70*(1-.28*q);h=66*(1-.34*q);r=16*(1-.30*q)
    depth=(1.2+.4*math.sin(math.pi*t))*(1-.30*q)
    return scallop(rr(w,h,r),depth),[w,h,r,depth]
def asum(p):return sum(area(aprofile((r['z']-34)/(Aroof-34),p)[0])-sum(area(v) for v in r['voids_local']) for r in A)
ap=solve(asum,300000)
for row in A:
    pts,dims=aprofile((row['z']-34)/(Aroof-34),ap)
    row.update(dict(w=dims[0],h=dims[1],r=dims[2],channel_depth=dims[3],outer=move(pts,centers['A']),
                    envelope_area=area(pts),void_area=sum(area(v) for v in row['voids_local'])))
    row['slab_area']=row['envelope_area']-row['void_area']
floors+=A

D=[];z=34
for f in range(7,63):
    hotel=f>=35;h=(3.8 if hotel else 4.25)
    h={7:5.6,20:5.6,34:6,35:6,48:5.2,62:5.8}.get(f,h)
    D.append({'tower':'D','floor':f,'kind':'body','z':z,'height':h,'top':z+h,'center':centers['D'],
              'voids_local':[rect(18,-6,5,12)] if f==21 else [rect(16,-8,5,16)] if f==36 else [],
              'core_local':[-12,-8,24,16] if hotel else [-13,-12,26,24],
              'program':'Hotel sky lobby' if f==35 else 'MEP/refuge reservation' if f in [20,34,48,62] else 'Hotel' if hotel else 'Office',
              'package':'hotel' if hotel else 'office'})
    z+=h
Droof=z;Dsplit=next(r['z'] for r in D if r['floor']==35)
def dprofile(t,p,hotel):
    t=max(0,min(1,t));q=t**p
    if hotel:w,h,r=56-6*q,36-2*q,10-q
    else:w,h,r=60-4*q,48-12*q,12-2*q
    return rr(w,h,r),[w,h,r]
def dsum(p,hotel):
    rows=[r for r in D if (r['package']=='hotel')==hotel];a,b=(Dsplit,Droof) if hotel else (34,Dsplit)
    return sum(area(dprofile((r['z']-a)/(b-a),p,hotel)[0])-sum(area(v) for v in r['voids_local']) for r in rows)
dp_off=solve(lambda p:dsum(p,False),70000);dp_hot=solve(lambda p:dsum(p,True),50000)
for row in D:
    hotel=row['package']=='hotel';a,b=(Dsplit,Droof) if hotel else (34,Dsplit)
    pts,dims=dprofile((row['z']-a)/(b-a),dp_hot if hotel else dp_off,hotel)
    row.update(dict(w=dims[0],h=dims[1],r=dims[2],outer=move(pts,centers['D']),envelope_area=area(pts),void_area=sum(area(v) for v in row['voids_local'])))
    row['slab_area']=row['envelope_area']-row['void_area']
floors+=D
floors.sort(key=lambda row:(row['tower'],row['floor']))

podpoly={k:Polygon(v[0]['outer']) for k,v in pods.items()};podpoly.update(B=Bpod,C=Cpod)
axis=LineString([(80,70),(112,79),(167,78),(208,82),(229,93)])
private=unary_union([Bpod.buffer(6),Cpod.buffer(6)])
plaza=axis.buffer(12,cap_style='round',join_style='round').difference(unary_union(list(podpoly.values()))).difference(private)
coreB1=unary_union([box(36,33,70,65),box(225,92,251,116)])
anchorA=Polygon(move(rr(94,80,16),[55,50]));anchorD=Polygon(move(rr(84,80,16),[237,103]))
ramps=[box(12,84,30,144),box(263,11,281,71)]
def mallpoly(w):return unary_union([anchorA,anchorD,axis.buffer(w/2)]).intersection(basement).difference(private).difference(coreB1).difference(unary_union(ramps))
mallwidth=solve(lambda w:mallpoly(w).area,14000,1,90)
mall=mallpoly(mallwidth)
parking=basement.difference(mall)
ramps=[box(12,84,30,144),box(263,11,281,71)]
loading=[box(22,15,42,27),box(253,119,270,131)]
basements=[{'name':f'B{i}','z':(-6 if i==1 else -6-3.6*(i-1)), 'height':6 if i==1 else 3.6,
            'envelope_area':37125,'mall_control_area':14000 if i==1 else 0,'parking_technical_control_area':23125 if i==1 else 37125} for i in range(1,6)]

def profile_at(name,z):
    if name=='A':return aprofile((z-34)/(Aroof-34),ap)[0]
    if z<Dsplit:return dprofile((z-34)/(Dsplit-34),dp_off,False)[0]
    return dprofile((z-Dsplit)/(Droof-Dsplit),dp_hot,True)[0]

# Store original B/C input unchanged as source and reference massing.
bcpath=ROOT/'data'/'bc-source-r1.json'
if not bcpath.exists():
    html=(ROOT.parent/'duplex-bc-r1.html').read_text()
    bc=json.loads(re.search(r'<script[^>]*id="geometry-data"[^>]*>(.*?)</script>',html,re.S).group(1))
    bcpath.write_text(json.dumps(bc,ensure_ascii=False,indent=2))
else:bc=json.loads(bcpath.read_text())

for row in floors:
    if row['kind']=='body':row['void_geometry']=geodict(unary_union([Polygon(move(v,row['center'])) for v in row['voids_local']]))
    x,y,w,h=row['core_local'];row['core_geometry']=geodict(box(x+centers[row['tower']][0],y+centers[row['tower']][1],x+w+centers[row['tower']][0],y+h+centers[row['tower']][1]))

towers={'A':{'center':centers['A'],'rotation_deg':0,'floors':98,'body_floor_count':92,'roof_z':Aroof,'crown_z':480,'profile_exponent':ap,'body_budget':300000,'podium_budget':28000,'roof_outline':move(profile_at('A',Aroof),centers['A'])},
        'D':{'center':centers['D'],'rotation_deg':0,'floors':62,'body_floor_count':56,'roof_z':Droof,'crown_low_z':278,'crown_z':285,'hotel_start_z':Dsplit,'office_profile_exponent':dp_off,'hotel_profile_exponent':dp_hot,'body_budget':120000,'podium_budget':22000,'roof_outline':move(profile_at('D',Droof),centers['D'])},
        'B':{'center':centers['B'],'floors':40,'roof_z':154.2,'crown_z':158.7,'outline':Bpts,'source':'bc-source-r1.json','status':'reference only; interior preserved in source'},
        'C':{'center':centers['C'],'floors':40,'roof_z':154.2,'crown_z':158.7,'outline':Cpts,'source':'bc-source-r1.json','status':'reference only; interior preserved in source'}}

checks=[]
def check(code,ok,details):checks.append({'id':code,'pass':bool(ok),'details':details})
for row in floors:
    p=Polygon(row['outer']);from shapely.geometry import shape
    v=shape(row['void_geometry']);core=shape(row['core_geometry'])
    check(f"{row['tower']}{row['floor']:03d}_geometry",p.is_valid and p.area>0 and (v.is_empty or p.buffer(1e-7).covers(v)),{'area':p.area,'void':v.area})
    check(f"{row['tower']}{row['floor']:03d}_core",p.covers(core) and core.intersection(v).area<1e-6,{'core_area':core.area,'overlap_void':core.intersection(v).area})
for k in ['A','D']:
    body=[r for r in floors if r['tower']==k and r['kind']=='body'];pod=pods[k]
    check(k+'_GFA',abs(sum(r['slab_area'] for r in body)-towers[k]['body_budget'])<.01, sum(r['slab_area'] for r in body))
    check(k+'_pod_GFA',abs(sum(r['slab_area'] for r in pod)-towers[k]['podium_budget'])<.01,sum(r['slab_area'] for r in pod))
    check(k+'_podium_contains_body',all(Polygon(r['outer']).buffer(.001).covers(Polygon(body[0]['outer'])) for r in pod), 'Outer envelopes only: reserved atria must be framed; no large unsupported tower overhang')
    check(k+'_projection_within_ground',all(Polygon(pod[0]['outer']).buffer(.001).covers(Polygon(r['outer'])) for r in pod+body),'All floor projections inside ground envelope')
    check(k+'_vertical_continuity',all(abs(rows[i]['top']-rows[i+1]['z'])<1e-7 for rows in [pod+body] for i in range(len(rows)-1)),towers[k]['roof_z'])
for k,p in podpoly.items():check(k+'_in_site',site.covers(p),p.bounds)
for i,k in enumerate(podpoly):
    for l in list(podpoly)[i+1:]:check('pod_gap_'+k+l,podpoly[k].intersection(podpoly[l]).area<1e-8,{'clear_distance_m':podpoly[k].distance(podpoly[l])})
towerpolys={k:Polygon(next(r['outer'] for r in floors if r['tower']==k and r['kind']=='body')) for k in ['A','D']};towerpolys.update(B=Polygon(Bpts),C=Polygon(Cpts))
distances={k+l:towerpolys[k].distance(towerpolys[l]) for i,k in enumerate(towerpolys) for l in list(towerpolys)[i+1:]}
check('mall_area',abs(mall.area-14000)<.01,mall.area)
check('mall_disconnected_BC',mall.intersection(unary_union([Bpod,Cpod])).area<1e-8,'BC footprint exclusion plus 6 m plan buffer')
check('mall_connected',mall.geom_type=='Polygon',mall.geom_type)
for i,r in enumerate(ramps):check(f'ramp_reserve_{i}',basement.covers(r) and r.intersection(mall).area<.001,{'area':r.area,'mall_overlap':r.intersection(mall).area})
for i,l in enumerate(loading):check(f'loading_in_mall_{i}',mall.covers(l),l.area)
density=sum(p.area for p in podpoly.values())+400
check('density',density<=18290,{'footprint_including_400_allowance':density,'ratio':density/45725})
total=sum(r['slab_area'] for r in floors)+119690.24+28000+14000
check('FAR_budget',total<=640150,{'control_area':total,'FAR_control':total/45725,'headroom':640150-total})
check('BC_source',bc['totals']['units_both_towers']==184 and bc['totals']['crown_top']==158.7,bc['totals'])

model={'project':'HOI LUU','revision':'R1','date':'2026-09-30','units':'metres','status':'Architectural geometry control; not construction documents',
       'coordinates':{'origin':'site corner (0,0); Z=0 entry datum; no geographic north assigned','X':'along 295 m edge','Y':'along 155 m edge','Z':'up'},
       'site':geodict(site),'basement_envelope':geodict(basement),'towers':towers,'floors':floors,
       'podium_footprints':{k:geodict(p) for k,p in podpoly.items()},'mall_B1':geodict(mall),'mall_connector_generation_width':mallwidth,
       'parking_technical_B1':geodict(parking),'private_buffers':geodict(private),'plaza':geodict(plaza),'plaza_axis':geodict(axis),
       'ramp_reserves':[geodict(r) for r in ramps],'loading_reserves':[geodict(r) for r in loading],
       'basements':basements,'tower_distances':distances,'control_area_total':total,'density_area':density,
       'area_convention':'Envelope minus explicit architectural voids; conservatively retains MEP/refuge/support. Not final statutory FAR. Core/shaft areas retained in envelope convention; detailed opening accounting pending.'}
(ROOT/'data'/'geometry.json').write_text(json.dumps(model,ensure_ascii=False,indent=2))
(ROOT/'data'/'checks.json').write_text(json.dumps({'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks},ensure_ascii=False,indent=2))
with (ROOT/'data'/'floor-schedule.csv').open('w',newline='',encoding='utf-8-sig') as f:
    cols=['tower','floor','kind','z','height','top','w','h','r','envelope_area','void_area','slab_area','program']
    wr=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');wr.writeheader();wr.writerows(floors)
with (ROOT/'data'/'outline-vertices.csv').open('w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['tower','floor','vertex','X_m','Y_m','Z_m'])
    for row in floors:
        for i,(x,y) in enumerate(row['outer']):wr.writerow([row['tower'],row['floor'],i,f'{x:.6f}',f'{y:.6f}',f"{row['z']:.6f}"])
print(json.dumps({'A_roof':Aroof,'D_roof':Droof,'D_hotel_start':Dsplit,'parameters':[ap,dp_off,dp_hot],'GFA':total,'density':density,'mall_width':mallwidth,'failed':[c for c in checks if not c['pass']],'tower_gaps':distances},ensure_ascii=False,indent=2))

if any(not c["pass"] for c in checks):
    raise SystemExit("Unresolved geometry checks")
