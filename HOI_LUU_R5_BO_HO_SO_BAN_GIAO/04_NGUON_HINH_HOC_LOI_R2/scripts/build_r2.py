"""HOI LUU R2: core/shaft reservation and reproducible preliminary traffic screen.
Run from package root. Requires numpy, scipy, shapely, matplotlib, markdown.
Geometry is a concept reservation, not manufacturer CAD or statutory compliance.
"""
from pathlib import Path
import json,csv,copy,hashlib,math,shutil
import numpy as np
from scipy.optimize import brentq
from shapely.geometry import Polygon,box,shape,mapping
from shapely.ops import unary_union
from shapely.affinity import translate
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source-r1'
for d in ['data','drawings','docs']: (ROOT/d).mkdir(exist_ok=True)
g=json.loads((SRC/'data/geometry.json').read_text()); r2=copy.deepcopy(g)
checks=[]
def check(name,value,detail=''):
    checks.append(dict(name=name,passed=bool(value),detail=detail))
def Acore(n):
    # Permanent central reservation plus successively terminating shuttle shafts.
    return box(-21,-18,21,18) if n<=33 else box(-21,-18,21,14) if n<=57 else box(-15,-14,21,14) if n<=81 else box(-15,-13,15,13)
def Dcore(n):return box(-16,-16,16,16) if n<=34 else box(-14,-10,14,10)
def core(t,n):return Acore(n) if t=='A' else Dcore(n)
def local(poly,t):return translate(poly,-g['towers'][t]['center'][0],-g['towers'][t]['center'][1])
def world(poly,t):return translate(poly,*g['towers'][t]['center'])
def solve(fn,target,a,b):return brentq(lambda x:fn(x)-target,a,b,xtol=1e-10)
def sample_rr(w,h,r,n=256):
    # Reuse only the exact pure geometry function, not the source build side effects.
    source=(SRC/'scripts/build_geometry.py').read_text()
    part=source[source.index('def rr('):source.index('def scallop(')]
    env={'math':math,'N':256};exec(part,env);return Polygon(env['rr'](w,h,r,n))
changes=[]
for f in r2['floors']:
    t,n=f['tower'],f['floor'];c=world(core(t,n),t);outer=Polygon(f['outer']);oldvoid=shape(f['void_geometry'])
    void=oldvoid
    if f['kind']=='podium' and void.intersection(c).area>1e-6:
        target=f['void_area'];zone=outer.difference(c.buffer(1))
        if t=='A':
            preferred=zone.intersection(box(g['towers'][t]['center'][0]+22,-100,400,300))
            if preferred.area>=target:zone=preferred
            threshold=solve(lambda x:zone.intersection(box(x,-100,400,300)).area,target,-100,400)
            void=zone.intersection(box(threshold,-100,400,300))
        else:
            threshold=solve(lambda x:zone.intersection(box(-100,-100,x,300)).area,target,-100,400)
            void=zone.intersection(box(-100,-100,threshold,300))
        changes.append({'tower':t,'floor':n,'change':'podium void relocated; same area','area':target})
    if t=='A' and n in [32,56,80]:
        y=18 if n==32 else 17;void=world(box(-8,y,8,y+6),t)
        changes.append({'tower':t,'floor':n,'change':'96 m2 east void moved north','local_bounds':[-8,y,8,y+6]})
    f['core_geometry']=mapping(c)
    xmin,ymin,xmax,ymax=core(t,n).bounds
    f['core_local']=[xmin,ymin,xmax-xmin,ymax-ymin]
    f['core_local_R2_bounds']=[xmin,ymin,xmax,ymax]
    if t=='A' and n in [32,56,80]:f['voids_local']=[[-8,y,16,6]]
    f['core_area_R2']=c.area;f['void_geometry']=mapping(void);f['void_area']=void.area
    f['slab_area']=outer.area-void.area
    check(f'{t}{n:02d}_core_in_outer',outer.covers(c))
    check(f'{t}{n:02d}_core_clear_void',void.intersection(c).area<1e-6)
    check(f'{t}{n:02d}_void_in_outer',void.is_empty or outer.buffer(1e-7).covers(void))
    check(f'{t}{n:02d}_area_unchanged',abs(f['slab_area']-next(x['slab_area'] for x in g['floors'] if x['tower']==t and x['floor']==n))<1e-5)
r2['revision']='R2';r2['date']='2026-09-30';r2['status']='Preliminary core and traffic reservation; external massing R1 retained'

# B1 mall: grow the connecting band only enough to retain the exact control area.
axis=shape(g['plaza_axis']);env=shape(g['basement_envelope']);private=shape(g['private_buffers'])
anchors=unary_union([translate(sample_rr(94,80,16),55,50),translate(sample_rr(84,80,16),237,103)])
coresB1=unary_union([world(Acore(1),'A'),world(Dcore(1),'D')])
ramps=unary_union([shape(x) for x in g['ramp_reserves']])
def mall(w):return unary_union([anchors,axis.buffer(w/2)]).intersection(env).difference(private).difference(coresB1).difference(ramps)
w=solve(lambda x:mall(x).area,14000,1,90);m=mall(w)
r2['mall_B1']=mapping(m);r2['mall_connector_generation_width']=w;r2['parking_technical_B1']=mapping(env.difference(m))
check('B1_mall_14000',abs(m.area-14000)<1e-5,m.area)
check('B1_connected',m.geom_type=='Polygon',m.geom_type)
check('B1_private_clear',m.intersection(private).area<1e-6)
check('B1_ramps_clear',m.intersection(ramps).area<1e-6)
check('B1_new_cores_clear',m.intersection(coresB1).area<1e-6)

# Architectural shaft modules: OUTER reservation including wall allowance, not clear hoistway.
slots=[]
def slot(t,id,x,y,ww,hh,cat,door):
    slots.append(dict(tower=t,id=id,bounds=[x,y,x+ww,y+hh],category=cat,door=door,area=ww*hh))
for row,y in enumerate([-10,-2.6,4.8]):
    for col in range(5):slot('A',f'K{row+1}.{col+1}',-8.5+3.4*col,y,3.4,4,'local','N' if row<2 else 'S')
for i,(x,y) in enumerate([(-14.5,-11.5),(-14.5,-7.1),(10.5,-5.6),(10.5,-1.2)]):slot('A',f'AS{i+1}',x,y,4,4,'service','E' if x<0 else 'W')
for i,(x,y) in enumerate([(-14.5,3),(10.5,3),(10.5,-12.5)]):slot('A',f'AT{i+1}',x,y,4,6.5,'stair','E' if x<0 else 'W')
for k in range(6):
    slot('A',f'E2.{k+1}',-12+4*k,13.3,4,4.2,'shuttle','N')
    slot('A',f'E3.{k+1}',-12+4*k,-17.5,4,4.2,'shuttle','S')
    slot('A',f'E4.{k+1}',15.3,-12+4*k,4.2,4,'shuttle','E')
for row,y in enumerate([-8.3,-1.9,4.5]):
    for col in range(3):
        idx=row*3+col+1;service=idx in [6,9]
        slot('D',f'HS{1 if idx==6 else 2}' if service else f'H{idx}',-5.1+3.4*col,y,3.4,3.8,'service' if service else 'hotel','E' if service else ('S' if row==2 else 'N'))
for i,x in enumerate([-13.5,9.5]):slot('D',f'DT{i+1}',x,-3.25,4,6.5,'stair','E' if x<0 else 'W')
for k in range(7):
    slot('D',f'DL.{k+1}',-11.9+3.4*k,-15.8,3.4,3.8,'office','N')
    slot('D',f'DH.{k+1}',-11.9+3.4*k,12,3.4,3.8,'office','S')
def active(t,n):
    out=[]
    for s in slots:
        if s['tower']!=t:continue
        if t=='A':
            if s['id'].startswith('E2') and n>33:continue
            if s['id'].startswith('E3') and n>57:continue
            if s['id'].startswith('E4') and n>81:continue
            if n>=82 and s['id'].startswith('K3'):continue
        elif n>=35 and s['category']=='office':continue
        out.append(s)
    return out
for t,n in [('A',8),('A',34),('A',58),('A',82),('D',7),('D',35)]:
    ac=active(t,n)
    for s in ac:check(f'{t}{n}_slot_{s["id"]}_contained',core(t,n).covers(box(*s['bounds'])))
    for i,a in enumerate(ac):
        for b in ac[i+1:]:
            overlap=box(*a['bounds']).intersection(box(*b['bounds'])).area
            check(f'{t}{n}_no_overlap_{a["id"]}_{b["id"]}',overlap<1e-7)

# Transparent stochastic trip sampling. Not a queue/dispatch simulation.
RNG=np.random.default_rng(20260929);TRIALS=12000
def flight(d,v,a=1):
    d=np.asarray(d,dtype=float);return np.where(d>=v*v/a,d/v+v/a,2*np.sqrt(d/a))
def trips(fs,weights,P,v,base,door=7,tp=1):
    zs=np.array([f['z'] for f in fs]);weights=np.array(weights,dtype=float);weights/=weights.sum()
    counts=RNG.multinomial(P,weights,size=TRIALS);rt=[];stop=[]
    for c in counts:
        z=zs[c>0];travel=float(flight(np.diff(np.r_[base,z]),v).sum()+flight(z[-1]-base,v))
        rt.append(travel+door*(len(z)+1)+2*P*tp);stop.append(len(z))
    return dict(RTT_s=float(np.mean(rt)),trip_p95_s=float(np.percentile(rt,95)),mean_stops=float(np.mean(stop)),sampling_SE_s=float(np.std(rt,ddof=1)/np.sqrt(TRIALS)))
def bank(id,t,lo,hi,base,cars,P,v,target=35,hotel=False):
    fs=[f for f in r2['floors'] if f['tower']==t and lo<=f['floor']<=hi and (not hotel or (37<=f['floor']<=47 or 49<=f['floor']<=61))]
    if hotel:
        weights=[16 if f['floor']<=57 else 10 for f in fs];population=sum(weights)*1.8+50
    else:
        weights=[(f['slab_area']-f['core_area_R2'])*.9 for f in fs];population=sum(weights)/12
    ans=trips(fs,weights,P,v,base,8 if hotel else 7,1.2 if hotel else 1)
    candidate_kg=3200 if hotel or t=='A' else 4000
    ans.update(id=id,tower=t,served_floors=[f['floor'] for f in fs],base_z=base,cars=cars,P_effective=P,speed_mps=v,population=population,target_interval_s=target,candidate_kg=candidate_kg,rated_mass_status='not fixed; cabin area and shaft CAD must be verified',minimum_clear_cabin_area_m2=P*(.3 if hotel else .21)/.8)
    ans['capacity_5min']=300*cars*P/ans['RTT_s'];ans['interval_s']=ans['RTT_s']/cars
    ans['demand_5min']=.12*population;ans['capacity_margin_pct']=100*(ans['capacity_5min']/ans['demand_5min']-1)
    ans['screen_pass']=ans['interval_s']<=target and ans['capacity_5min']>=ans['demand_5min']
    ans['density_sensitivity']={str(d):dict(population=population*12/d,demand=.12*population*12/d,capacity_pass=ans['capacity_5min']>=.12*population*12/d) for d in [10,12,14]} if not hotel else {}
    ans['one_car_out']={'capacity_5min':300*(cars-1)*P/ans['RTT_s'],'interval_s':ans['RTT_s']/(cars-1)}
    return ans
banks=[]
zones=[(8,30,0),(33,54,147.2),(57,78,256),(81,97,364.8)]
for zi,(lo,hi,base) in enumerate(zones):
    for bi,seq in enumerate(np.array_split(np.arange(lo,hi+1),3 if zi<3 else 2)):
        P=20 if zi==0 and bi==2 else 22
        banks.append(bank(f'A-Z{zi+1}-{bi+1}','A',int(seq[0]),int(seq[-1]),base,5,P,6))
for lo,hi,id in [(7,19,'D-LOW'),(21,33,'D-HIGH')]:banks.append(bank(id,'D',lo,hi,0,7,26,6))
banks.append(bank('D-HOTEL','D',37,61,0,7,16,8,40,True))
shuttles=[]
for zi in [1,2,3]:
    pop=sum(x['population'] for x in banks if x['id'].startswith(f'A-Z{zi+1}'))
    z=zones[zi][2];P=33;cars=6;v=10
    rt=float(2*flight(z,v)+14+2*P)
    ans=dict(id=f'A-E{zi+1}',population=pop,base_z=0,terminal_z=z,P_effective=P,cars=cars,speed_mps=v,candidate_kg=5000,rated_mass_status='not fixed; large high-speed cabin requires supplier validation',minimum_clear_cabin_area_m2=P*.21/.8,RTT_s=rt,interval_s=rt/cars,capacity_5min=300*cars*P/rt,demand_5min=.12*pop,target_interval_s=30)
    ans['screen_pass']=ans['interval_s']<=30 and ans['capacity_5min']>=ans['demand_5min']
    ans['one_car_out']={'capacity_5min':300*(cars-1)*P/rt,'interval_s':rt/(cars-1)}
    shuttles.append(ans)
for b in banks+shuttles:check('screen_'+b['id'],b['screen_pass'],{'capacity':b['capacity_5min'],'demand':b['demand_5min'],'interval':b['interval_s']})

# Machine/pit separation for local stacks and express termination.
transfers=[]
for last,first in [(30,32),(54,56),(78,80)]:
    low=next(f for f in r2['floors'] if f['tower']=='A' and f['floor']==last);high=next(f for f in r2['floors'] if f['tower']=='A' and f['floor']==first)
    clear=(high['z']-2)-(low['z']+5.5)
    transfers.append(dict(last_floor=last,first_floor=first,last_landing=low['z'],overhead_top=low['z']+5.5,upper_pit_bottom=high['z']-2,gross_gap=high['z']-low['z'],remaining_gap=clear,structural_slab_allowance=.4))
    check(f'A_local_stack_{last}_{first}',clear>=.4,clear)
for last,nextn in [(32,34),(56,58),(80,82)]:
    a=next(f for f in r2['floors'] if f['tower']=='A' and f['floor']==last);b=next(f for f in r2['floors'] if f['tower']=='A' and f['floor']==nextn)
    check(f'A_express_headroom_{last}',a['z']+6.5<=b['z'],{'head_top':a['z']+6.5,'reclaim_z':b['z']})
def office_net(data,t):return sum((f['slab_area']-shape(f['core_geometry']).area)*.9 for f in data['floors'] if f['tower']==t and f['program']=='Office')
stats=dict(A_population=sum(x['population'] for x in banks if x['tower']=='A'),D_office_population=sum(x['population'] for x in banks if x['id'] in ['D-LOW','D-HIGH']),hotel_keys_traffic_assumption=360,hotel_population=next(x['population'] for x in banks if x['id']=='D-HOTEL'),A_installed_traffic_cars=55+18+4,A_base_vertical_shafts=15+18+4,D_installed_traffic_cars=14+7+2,A_office_net_R1_proxy=office_net(g,'A'),A_office_net_R2_proxy=office_net(r2,'A'),D_office_net_R1_proxy=office_net(g,'D'),D_office_net_R2_proxy=office_net(r2,'D'),mall_width_R1=g['mall_connector_generation_width'],mall_width_R2=w,mall_area_without_repair=shape(g['mall_B1']).difference(coresB1).area,core_B1_A=1512,core_B1_D=1024)
check('FAR_unchanged',abs(r2['control_area_total']-g['control_area_total'])<1e-8)
check('density_unchanged',abs(r2['density_area']-g['density_area'])<1e-8)
out=dict(project='HOI LUU',revision='R2',date='2026-09-30',timezone='Asia/Ho_Chi_Minh',assumptions={'office_density_net_m2_per_person':12,'post_core_net_factor':.9,'office_peak_fraction_5min':.12,'office_interval_project_target_s':35,'shuttle_interval_target_s':30,'hotel_interval_target_s':40,'acceleration_mps2':1,'flight_profile':'ideal triangular/trapezoidal; no jerk','door_and_levelling_s':7,'passenger_transfer_s':1,'samples_per_bank':TRIALS,'hotel_keys':'360 for traffic testing; not approved room yield','hotel_population':'360*1.8+50; full occupancy plus guest visitors','hotel_screen':'up-peak only; mixed-direction hotel traffic not validated','car_count_status':'working reservation; not procurement schedule'},banks=banks,shuttles=shuttles,slots=slots,transfers=transfers,geometry_changes=changes,stats=stats,checks=checks)
for name,data in [('r2-study.json',out),('geometry-r2.json',r2)]: (ROOT/'data'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
with (ROOT/'data/traffic-banks.csv').open('w',newline='') as fp:
    fields=['id','tower','cars','P_effective','speed_mps','population','RTT_s','interval_s','capacity_5min','demand_5min','target_interval_s','screen_pass'];wr=csv.DictWriter(fp,fields,extrasaction='ignore');wr.writeheader();wr.writerows(banks+shuttles)
with (ROOT/'data/core-floor-schedule.csv').open('w',newline='') as fp:
    fields=['tower','floor','z','height','slab_area','core_area_R2','program'];wr=csv.DictWriter(fp,fields,extrasaction='ignore');wr.writeheader();wr.writerows(r2['floors'])
print(json.dumps({'stats':stats,'failed':[x for x in checks if not x['passed']],'banks':[{k:b[k] for k in ['id','RTT_s','interval_s','capacity_5min','demand_5min']} for b in banks+shuttles]},ensure_ascii=False,indent=2))
