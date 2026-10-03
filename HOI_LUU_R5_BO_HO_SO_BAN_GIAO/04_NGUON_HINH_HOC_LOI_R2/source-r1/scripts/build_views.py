"""Generate drawings and a neutral OBJ from the released geometry.json only."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import shape,Polygon,LineString,Point
R=Path(__file__).resolve().parents[1];G=json.loads((R/'data/geometry.json').read_text());F=G['floors']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.titleweight':'bold'})
COL={'A':'#5a8091','D':'#ae8960','B':'#a8b4b3','C':'#a8b4b3'}
def polygons(g):
    if g.is_empty:return []
    if g.geom_type=='Polygon':return [g]
    return [p for sub in getattr(g,'geoms',[]) for p in polygons(sub)]
def drawpoly(ax,g,color,alpha=1,lw=.7,hatch=None):
    for p in polygons(g):
        ax.add_patch(Patch(np.array(p.exterior.coords),facecolor=color,edgecolor='#354650',alpha=alpha,lw=lw,hatch=hatch))
        for h in p.interiors:ax.add_patch(Patch(np.array(h.coords),facecolor='white',edgecolor='#354650',lw=.4))
def save(fig,name):
    fig.savefig(R/'drawings'/f'{name}.svg',bbox_inches='tight')
    fig.savefig(R/'drawings'/f'{name}.png',dpi=155,bbox_inches='tight');plt.close(fig)
def sitebase(ax):
    drawpoly(ax,shape(G['site']),'#f5f4ef');
    b=shape(G['basement_envelope']);x,y=b.exterior.xy;ax.plot(x,y,'--',color='#89979b',lw=.8)
    ax.set_aspect('equal');ax.set_xlim(-5,300);ax.set_ylim(-5,160);ax.set_xlabel('X [m]');ax.set_ylabel('Y [m]');ax.grid(alpha=.1)

fig,ax=plt.subplots(figsize=(13,7.5));sitebase(ax)
drawpoly(ax,shape(G['private_buffers']),'#e3e9e0',.7,lw=.2)
drawpoly(ax,shape(G['plaza']),'#e6ca9d',1)
for k in ['A','D','B','C']:
    drawpoly(ax,shape(G['podium_footprints'][k]),COL[k],.5)
    pts=next(r['outer'] for r in F if r['tower']==k and r['kind']=='body') if k in ['A','D'] else G['towers'][k]['outline']
    drawpoly(ax,Polygon(pts),COL[k],.9)
    c=G['towers'][k]['center'];ax.text(*c,k,ha='center',va='center',fontsize=16,color='white',weight='bold')
for i,r in enumerate(G['ramp_reserves']):
    drawpoly(ax,shape(r),'#e2e3e7',hatch='///');c=shape(r).centroid;ax.text(c.x,c.y,'R'+str(i+1),ha='center')
ax.text(146,80,'PLAZA',ha='center',fontsize=9);ax.set_title('S01 · TỔNG MẶT BẰNG KIỂM SOÁT — TỌA ĐỘ MÉT',loc='left',pad=14)
fig.text(.12,.015,'X/Y là trục khu đất, chưa phải hướng địa lý. Vùng riêng B/C có đệm 6 m là lựa chọn thiết kế.',fontsize=9)
save(fig,'S01-site')

fig,ax=plt.subplots(figsize=(13,7.5));sitebase(ax)
drawpoly(ax,shape(G['parking_technical_B1']),'#dce2e5')
drawpoly(ax,shape(G['mall_B1']),'#e5c392')
for k in ['A','D','B','C']:
    p=shape(G['podium_footprints'][k]);ax.plot(*p.exterior.xy,'--',color='#50626c',lw=.8)
for r in G['ramp_reserves']:drawpoly(ax,shape(r),'#bdc8d2',hatch='///')
for i,r in enumerate(G['loading_reserves']):
    drawpoly(ax,shape(r),'#a8b79f');c=shape(r).centroid;ax.text(c.x,c.y,'BOH',ha='center',va='center',fontsize=8)
for k in ['B','C']:
    c=G['towers'][k]['center'];ax.text(*c,k+' · RIÊNG',ha='center',fontsize=10)
ax.text(52,76,'MALL A',ha='center');ax.text(233,82,'MALL D',ha='center');ax.text(148,80,'MALL B1',ha='center',fontsize=9)
ax.set_title('S02 · B1 — 14.000 m² MALL / 23.125 m² XE + KỸ THUẬT',loc='left',pad=14)
fig.text(.12,.015,'Đường nét đứt: đế trên mặt đất. Hai vùng BOH nằm trong mall. Khoảng trắng ở A/D: lõi riêng.',fontsize=9)
save(fig,'S02-basement')

for name,numbers in [('A',[7,31,55,79]),('D',[7,21,35,62])]:
    fig,axs=plt.subplots(2,2,figsize=(11,11))
    for ax,num in zip(axs.flat,numbers):
        row=next(r for r in F if r['tower']==name and r['floor']==num)
        c=row['center'];p=Polygon([[x-c[0],y-c[1]] for x,y in row['outer']]);drawpoly(ax,p,COL[name],.25)
        from shapely.affinity import translate
        drawpoly(ax,translate(shape(row['core_geometry']),-c[0],-c[1]),'#aab6bd',.85)
        drawpoly(ax,translate(shape(row['void_geometry']),-c[0],-c[1]),'white',hatch='///')
        if name=='D' and num==35:drawpoly(ax,p.buffer(-3),'#bfcdc8',.6)
        ax.text(0,0,'LÕI\nGIỮ CHỖ',ha='center',va='center',fontsize=9)
        ax.set_xlim(-40,40);ax.set_ylim(-38,38);ax.set_aspect('equal');ax.grid(alpha=.15)
        ax.set_title(f"{name}{num:02d} · +{row['z']:.2f} m\nSàn kiểm soát {row['slab_area']:,.2f} m²",fontsize=11)
        ax.set_xlabel('u [m]');ax.set_ylabel('v [m]')
    fig.suptitle(f'{name}01 · MẶT BẰNG ĐƯỜNG BAO VÀ LÕI — CÙNG TỶ LỆ',fontsize=15)
    fig.tight_layout(rect=[0,0,1,.94]);save(fig,f'{name}01-plans')

def point_angle(pts,c,theta):
    ray=LineString([c,[c[0]+200*math.cos(theta),c[1]+200*math.sin(theta)]])
    hit=Polygon(pts).boundary.intersection(ray)
    points=[hit] if hit.geom_type=='Point' else list(hit.geoms)
    p=max(points,key=lambda p:p.distance(Point(c)));return [p.x,p.y]
def bodyrings(name):
    rows=[r for r in F if r['tower']==name and r['kind']=='body'];t=G['towers'][name]
    return [(r['z'],r['outer']) for r in rows]+[(t['roof_z'],t['roof_outline'])]
def crownrings(name,n=256):
    t=G['towers'][name];c=t['center'];pts=t['roof_outline'];rings=[]
    for u in [0,.2,.4,.6,.8,1]:
        ring=[]
        for x,y in pts:
            theta=math.atan2(y-c[1],x-c[0]);top=(478.5+1.5*math.cos(4*theta)) if name=='A' else (281.5+3.5*math.cos(theta))
            shrink=1-(.12 if name=='A' else .035)*(u*u*(3-2*u))
            previous=bodyrings(name)[-2]; j=len(ring); dz=t['roof_z']-previous[0]
            dx=(x-previous[1][j][0])/dz;dy=(y-previous[1][j][1])/dz
            tangent=(u**3-2*u*u+u)*(top-t['roof_z'])
            ring.append([c[0]+(x-c[0])*shrink+tangent*dx,c[1]+(y-c[1])*shrink+tangent*dy,t['roof_z']+(top-t['roof_z'])*u])
        rings.append(ring)
    return rings

fig,axs=plt.subplots(1,2,figsize=(10,13),sharey=True,gridspec_kw={'width_ratios':[1,1]})
for ax,name in zip(axs,['A','D']):
    t=G['towers'][name];c=t['center'];rings=bodyrings(name)
    left=[(min(x for x,y in pts)-c[0],z) for z,pts in rings];right=[(max(x for x,y in pts)-c[0],z) for z,pts in rings]
    ax.add_patch(Patch(left+list(reversed(right)),facecolor=COL[name],alpha=.25,edgecolor='#354650',lw=1))
    for z,pts in rings:ax.plot([min(x for x,y in pts)-c[0],max(x for x,y in pts)-c[0]],[z,z],color='#72858e',lw=.35)
    for theta in [math.pi*9/8,math.pi*11/8,math.pi*13/8,math.pi*15/8]:
        line=[[*point_angle(pts,c,theta),z] for z,pts in rings]
        cr=crownrings(name);j=min(range(256),key=lambda i:abs(math.atan2(math.sin(math.atan2(cr[0][i][1]-c[1],cr[0][i][0]-c[0])-theta),math.cos(math.atan2(cr[0][i][1]-c[1],cr[0][i][0]-c[0])-theta))))
        line += [r[j] for r in cr[1:]]
        ax.plot([p[0]-c[0] for p in line],[p[2] for p in line],color='#3c5662',lw=1.2)
    cr=crownrings(name)
    ax.plot([p[0]-c[0] for p in cr[-1]+[cr[-1][0]]],[p[2] for p in cr[-1]+[cr[-1][0]]],color='#536873',lw=.8)
    for idx in range(0,256,8):ax.plot([r[idx][0]-c[0] for r in cr],[r[idx][2] for r in cr],color='#819098',lw=.4)
    for row in [r for r in F if r['tower']==name and r['kind']=='podium']:
        xs=[x-c[0] for x,y in row['outer']];ax.add_patch(Patch([(min(xs),row['z']),(max(xs),row['z']),(max(xs),row['top']),(min(xs),row['top'])],facecolor='#d3d3c8',edgecolor='#687779',lw=.5))
    if name=='D':ax.add_patch(Patch([[-28,t['hotel_start_z']],[28,t['hotel_start_z']],[28,t['hotel_start_z']+6],[-28,t['hotel_start_z']+6]],facecolor='#9eaf96',alpha=.7,edgecolor='none'))
    for z,label in [(t['roof_z'],'MÁI'),(t['crown_z'],'ĐỈNH')]:ax.annotate(f'{label} +{z:.2f}',xy=(24,z),xytext=(28,z+5),fontsize=9)
    ax.axhline(158.7,color='#aab1b3',ls='--',lw=.8);ax.text(-48,160.5,'B/C +158,70',fontsize=8)
    ax.set_xlim(-50,85);ax.set_ylim(-5,500);ax.set_aspect('equal');ax.set_xlabel('u [m]');ax.grid(axis='y',alpha=.13);ax.set_title(f'THÁP {name} · {t["floors"]} TẦNG',fontsize=12)
axs[0].set_ylabel('Cao độ Z [m]');fig.suptitle('E01 · MẶT ĐỨNG KIỂM SOÁT — KHÔNG PHÓNG ĐẠI CHIỀU CAO',fontsize=14)
save(fig,'E01-elevations')

# OBJ: body envelopes, podium envelopes, crown ribs, B/C reference blocks. No fake interior fit-out.
verts=[];faces=[];objects=[];lines=[]
def mesh_obj(name,v,f,mat):
    limit=480 if name.startswith('A_') else 285 if name.startswith('D_') else 10000
    v=[[x,y,min(z,limit)] for x,y,z in v]
    off=len(verts);verts.extend(v);objects.append({'name':name,'first':len(faces),'count':len(f),'material':mat});faces.extend([[off+i for i in face] for face in f])
def loft(name,rings,mat):
    n=len(rings[0]);v=[p for ring in rings for p in ring];f=[]
    for k in range(len(rings)-1):
        for i in range(n):j=(i+1)%n;f.append([k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i])
    mesh_obj(name,v,f,mat)
def tube(name,path,radius,mat='silver',segments=6):
    pp=np.array(path);rs=[]
    for i,p in enumerate(pp):
        tangent=pp[min(i+1,len(pp)-1)]-pp[max(i-1,0)];tangent=tangent/np.linalg.norm(tangent)
        ref=np.array([1,0,0]) if abs(tangent[0])<.9 else np.array([0,1,0]);u=np.cross(tangent,ref);u/=np.linalg.norm(u);v=np.cross(tangent,u)
        rs.append([(p+radius*(u*math.cos(j*2*math.pi/segments)+v*math.sin(j*2*math.pi/segments))).tolist() for j in range(segments)])
    loft(name,rs,mat)
for name in ['A','D']:
    t=G['towers'][name];c=t['center'];rings=bodyrings(name)
    three=[[[x,y,z] for x,y in pts] for z,pts in rings]
    if name=='D':
        # Six-metre-high recessed hotel sky lobby; outer fins and slab envelope remain continuous.
        start=t['hotel_start_z'];end=start+6;adjust=[]
        for z,pts in rings:
            if abs(z-start)<1e-5:adjust.append([[x,y,z] for x,y in pts])
            if start-1e-5<=z<=end+1e-5:
                inset=Polygon(pts).buffer(-3);ring=inset.exterior;ip=[[ring.interpolate(i*ring.length/256).x,ring.interpolate(i*ring.length/256).y] for i in range(256)]
                # Preserve the original angular ordering for a sound recess loft.
                ip=[point_angle(list(inset.exterior.coords),c,math.atan2(y-c[1],x-c[0])) for x,y in pts]
                adjust.append([[x,y,z] for x,y in ip])
                if abs(z-end)<1e-5:adjust.append([[x,y,z] for x,y in pts])
            else:adjust.append([[x,y,z] for x,y in pts])
        three=adjust
    loft(name+'_glass_envelope',three,'glass_'+name)
    cr=crownrings(name)
    for i in range(0,256,8):tube(f'{name}_crown_fin_{i}',[ring[i] for ring in cr],.12)
    tube(name+'_crown_rim',cr[-1]+[cr[-1][0]],.18)
    for j in range(8):
        theta=math.pi/8+j*math.pi/4
        path=[[*point_angle(pts,c,theta),z] for z,pts in rings]
        # Continue main ribs through podium as vertical alignment placeholders.
        path.insert(0,[path[0][0],path[0][1],0])
        i=min(range(256),key=lambda i:abs(math.atan2(math.sin(math.atan2(cr[0][i][1]-c[1],cr[0][i][0]-c[0])-theta),math.cos(math.atan2(cr[0][i][1]-c[1],cr[0][i][0]-c[0])-theta))))
        path += [ring[i] for ring in cr[1:]];tube(f'{name}_rib_{j+1}',path,.45 if name=='A' else .24)
    for row in [r for r in F if r['tower']==name and r['kind']=='podium']:
        loft(f'{name}_podium_{row["floor"]}',[[[x,y,z] for x,y in row['outer']] for z in [row['z'],row['top']]],'podium')
for name in ['B','C']:
    t=G['towers'][name];loft(name+'_REFERENCE_ONLY',[[[x,y,z] for x,y in t['outline']] for z in [26.4,154.2,158.7]],'residential')
    p=list(shape(G['podium_footprints'][name]).exterior.coords)[:-1];loft(name+'_podium_REFERENCE',[[[x,y,z] for x,y in p] for z in [0,26.4]],'podium')
obj_lines=['# metres, Z up; control massing, not construction BIM','mtllib hoi-luu-r1.mtl']
for v in verts:obj_lines.append('v '+' '.join(f'{x:.6f}' for x in v))
for ob in objects:
    obj_lines.extend(['o '+ob['name'],'usemtl '+ob['material']])
    for f in faces[ob['first']:ob['first']+ob['count']]:obj_lines.append('f '+' '.join(str(i+1) for i in f))
obj_lines.append('# END HOI LUU R1: '+str(len(objects))+' objects')
obj_text='\n'.join(obj_lines)+'\n'
(R/'model/hoi-luu-r1.obj').write_text(obj_text)
assert (R/'model/hoi-luu-r1.obj').read_text().count('\no ')==len(objects)
(R/'model/hoi-luu-r1.mtl').write_text('newmtl glass_A\nKd 0.38 0.54 0.63\nnewmtl glass_D\nKd 0.57 0.65 0.67\nnewmtl silver\nKd 0.78 0.80 0.79\nnewmtl podium\nKd 0.75 0.73 0.66\nnewmtl residential\nKd 0.61 0.66 0.65\n')
(R/'data/model-manifest.json').write_text(json.dumps({'vertices':len(verts),'faces':len(faces),'objects':objects,'crown_rules':{'A':'Z_top(theta)=478.5+1.5*cos(4*theta); 12% radial shrink plus Hermite initial slope from last body interval','D':'Z_top(theta)=281.5+3.5*cos(theta); 3.5% radial shrink plus Hermite initial slope from last body interval'},'D_sky_lobby_recess':{'from_z':G['towers']['D']['hotel_start_z'],'height':6,'glass_setback':3}},indent=2))

# Mathematically projected axonometric; reduced surface sampling affects only preview tessellation.
fig=plt.figure(figsize=(12,11));ax=fig.add_subplot(111,projection='3d')
for name in ['A','D','B','C']:
    t=G['towers'][name]
    if name in ['A','D']:rings=bodyrings(name)[::4]+[bodyrings(name)[-1]]
    else:rings=[(26.4,t['outline']),(158.7,t['outline'])]
    polys=[]
    for a,b in zip(rings,rings[1:]):
        pa=a[1][::8] if len(a[1])>8 else a[1];pb=b[1][::8] if len(b[1])>8 else b[1]
        for i in range(len(pa)):j=(i+1)%len(pa);polys.append([[*pa[i],a[0]],[*pa[j],a[0]],[*pb[j],b[0]],[*pb[i],b[0]]])
    ax.add_collection3d(Poly3DCollection(polys,facecolors=COL[name],edgecolors='#526673',linewidths=.13,alpha=.83))
    c=t['center'];ax.text(c[0],c[1],t['crown_z']+9,name,fontsize=14)
    if name in ['A','D']:
        cr=crownrings(name)
        rim=np.array(cr[-1]+[cr[-1][0]]);ax.plot(*rim.T,color='#536873',lw=.8)
        for j in range(8):
            theta=math.pi/8+j*math.pi/4; rib=np.array([[*point_angle(pts,c,theta),z] for z,pts in bodyrings(name)])
            ax.plot(*rib.T,color='#bbc3c7',lw=.7)
        for i in range(0,256,16):ax.plot(*np.array([ring[i] for ring in cr]).T,color='#6c777e',lw=.8)
        for row in [r for r in F if r['tower']==name and r['kind']=='podium']:
            pp=np.array(row['outer']+[row['outer'][0]]);ax.plot(pp[:,0],pp[:,1],row['top'],color='#857f6d',lw=.7)
    else:
        pp=np.array(list(shape(G['podium_footprints'][name]).exterior.coords));ax.plot(pp[:,0],pp[:,1],26.4,color='#857f6d')
ax.plot([0,295,295,0,0],[0,0,155,155,0],[0]*5,color='#4e5f67')
ax.set_xlim(0,295);ax.set_ylim(0,155);ax.set_zlim(0,495);ax.set_box_aspect([295,155,495]);ax.view_init(elev=18,azim=-67)
ax.set_xlabel('X [m]');ax.set_ylabel('Y [m]');ax.set_zlabel('Z [m]');ax.set_title('V01 · AXONOMETRIC TỪ DỮ LIỆU — B/C CHỈ HIỂN THỊ KHỐI THAM CHIẾU')
save(fig,'V01-axonometric')
print(json.dumps({'drawings':6,'obj_vertices':len(verts),'obj_faces':len(faces)}))
