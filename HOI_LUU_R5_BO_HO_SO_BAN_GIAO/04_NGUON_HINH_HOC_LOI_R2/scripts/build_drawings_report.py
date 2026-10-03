"""Render exact R2 reservations and self-contained Vietnamese study report."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/hoi-luu-mpl')
import json,html,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Rectangle
from shapely.geometry import shape,Polygon,box
from shapely.affinity import translate
import markdown
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'data/r2-study.json').read_text());g=json.loads((ROOT/'data/geometry-r2.json').read_text());r1=json.loads((ROOT/'source-r1/data/geometry.json').read_text());st=s['stats']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','axes.titleweight':'bold'})
COL={'local':'#298d9f','shuttle':'#41559a','service':'#ac7652','stair':'#bf5763','office':'#298d9f','hotel':'#846eb0'}
def geom(ax,p,fc='none',ec='#263746',lw=1,alpha=1,ls='-'):
    if p.is_empty:return
    if p.geom_type=='Polygon':
        ax.add_patch(Patch(list(p.exterior.coords),fc=fc,ec=ec,lw=lw,alpha=alpha,ls=ls))
        for ring in p.interiors:ax.add_patch(Patch(list(ring.coords),fc='white',ec=ec,lw=lw))
    elif hasattr(p,'geoms'):
        for q in p.geoms:geom(ax,q,fc,ec,lw,alpha,ls)
def fl(t,n,data=g):return next(f for f in data['floors'] if f['tower']==t and f['floor']==n)
def local(p,t):return translate(p,-g['towers'][t]['center'][0],-g['towers'][t]['center'][1])
def active(t,n):
    a=[]
    for p in s['slots']:
        if p['tower']!=t:continue
        if t=='A' and ((p['id'].startswith('E2') and n>33) or (p['id'].startswith('E3') and n>57) or (p['id'].startswith('E4') and n>81) or (p['id'].startswith('K3') and n>=82)):continue
        if t=='D' and n>=35 and p['category']=='office':continue
        a.append(p)
    return a
def detail(ax,t,n):
    f=fl(t,n);geom(ax,local(shape(f['core_geometry']),t),'#eef1f4','#263746',1.8)
    old=local(shape(fl(t,n,r1)['core_geometry']),t);geom(ax,old,'none','#ca8f35',1.3,ls='--')
    for p in active(t,n):
        x,y,x2,y2=p['bounds'];ax.add_patch(Rectangle((x,y),x2-x,y2-y,fc=COL[p['category']],ec='white',lw=.8))
        ax.text((x+x2)/2,(y+y2)/2,p['id'],ha='center',va='center',color='white',size=6.3,weight='bold')
        edge={'N':((x+x2)/2,y2),'S':((x+x2)/2,y),'E':(x2,(y+y2)/2),'W':(x,(y+y2)/2)}[p['door']]
        dx,dy={'N':(0,.75),'S':(0,-.75),'E':(.75,0),'W':(-.75,0)}[p['door']]
        ax.plot([edge[0]-.45*(dy!=0),edge[0]+.45*(dy!=0)],[edge[1]-.45*(dx!=0),edge[1]+.45*(dx!=0)],color='white',lw=2)
        ax.annotate('',xy=(edge[0]+dx,edge[1]+dy),xytext=edge,arrowprops=dict(arrowstyle='-',color='#263746',lw=.7))
    ax.set_aspect('equal');ax.set_xlim(-26,26);ax.set_ylim(-23,23);ax.set_xticks(np.arange(-20,21,10));ax.set_yticks(np.arange(-20,21,10));ax.grid(alpha=.16);ax.set_axisbelow(True)
    ax.set_title(f'{t}{n:02d} · vùng lõi {f["core_area_R2"]:,.0f} m²',loc='left',fontsize=12)
    ax.set_xlabel('u local / m');ax.set_ylabel('v local / m')
def footer(fig,text):fig.text(.035,.018,text,fontsize=8,color='#526374')
def save(fig,name):
    fig.savefig(ROOT/'drawings'/f'{name}.svg',facecolor='white');fig.savefig(ROOT/'drawings'/f'{name}.png',dpi=140,facecolor='white');plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(15,13));fig.subplots_adjust(left=.07,right=.97,top=.91,bottom=.08,hspace=.27,wspace=.2)
for ax,n in zip(axs.flat,[8,34,58,82]):detail(ax,'A',n)
fig.suptitle('A · Lõi và các giếng thang lồng theo chiều cao',x=.07,ha='left',fontsize=19)
footer(fig,'A02 / R2   Xanh ngọc: thang local · Xanh đậm: shuttle · Nâu: phục vụ · Đỏ: thang bộ · Nét vàng: lõi R1. Kích thước là vùng giữ chỗ ngoài tường.')
save(fig,'A02-core-reservations')
fig,axs=plt.subplots(1,2,figsize=(15,8));fig.subplots_adjust(left=.07,right=.97,top=.87,bottom=.11,wspace=.15)
for ax,n in zip(axs,[7,35]):detail(ax,'D',n)
fig.suptitle('D · Thang khách sạn đi xuyên vùng văn phòng',x=.07,ha='left',fontsize=19)
footer(fig,'D02 / R2   DL/DH: hai nhóm văn phòng · H: bảy thang khách sạn trực tiếp · HS: hai thang phục vụ · DT: hai vùng thang bộ. Chưa xác nhận PCCC.')
save(fig,'D02-core-reservations')
fig,axs=plt.subplots(2,3,figsize=(16,11));fig.subplots_adjust(left=.04,right=.97,top=.9,bottom=.08,wspace=.2,hspace=.23)
for ax,(t,n) in zip(axs.flat,[('A',8),('A',56),('A',80),('D',7),('D',33),('D',49)]):
    f=fl(t,n);outer=local(Polygon(f['outer']),t);core=local(shape(f['core_geometry']),t);void=local(shape(f['void_geometry']),t)
    geom(ax,outer,'#f4f6f5','#263746',1.2);geom(ax,core,'#cdd5df','#41559a');geom(ax,void,'white','#c65a56',1.4)
    ax.text(0,0,f'{core.area:,.0f} m²\nlõi',ha='center',va='center',fontsize=10,color='#263746')
    ax.set_aspect('equal');ax.set_xlim(-37,37);ax.set_ylim(-36,36);ax.set_xticks([-30,0,30]);ax.set_yticks([-30,0,30]);ax.grid(alpha=.1);ax.set_title(f'{t}{n:02d} · GFA {f["slab_area"]:,.0f} m² · lõi {100*core.area/f["slab_area"]:.1f}%',fontsize=11,loc='left')
fig.suptitle('Kiểm tra lõi trong biên sàn thật · cùng tỷ lệ',x=.04,ha='left',fontsize=19)
footer(fig,'P02 / R2   Đường bao và cao độ lấy từ R1; vùng lõi và lỗ mở lấy từ geometry-r2.json. Phần ngoài lõi còn phải trừ cột, hành lang, vệ sinh và MEP.')
save(fig,'P02-floor-envelope')
fig,ax=plt.subplots(figsize=(17,9));fig.subplots_adjust(left=.04,right=.97,top=.91,bottom=.09)
geom(ax,shape(g['basement_envelope']),'#f2f2ee','#777',1);geom(ax,shape(g['mall_B1']),'#9ed8cb','#2c8274',1.4)
geom(ax,shape(r1['mall_B1']),'none','#b4813b',1.3,ls='--')
geom(ax,shape(g['private_buffers']),'#e7e9ee','#8390a1',.8)
for t in ['A','D']:
    c=shape(fl(t,1)['core_geometry']);geom(ax,c,'#41559a','white',1)
    ax.text(*c.centroid.coords[0],f'{t}\n{c.area:,.0f} m²',ha='center',va='center',color='white',weight='bold')
for t in ['B','C']:
    q=shape(g['podium_footprints'][t]);geom(ax,q,'#ced3dd','#627080');ax.text(*q.centroid.coords[0],f'{t} · riêng tư',ha='center',va='center')
for p in g['ramp_reserves']:geom(ax,shape(p),'#d4b38a','#ac7652')
line=shape(g['plaza_axis']);ax.plot(*line.xy,color='#24596a',ls=':',lw=1)
ax.text(151,79,'B1 mall · 14.000 m²',ha='center',fontsize=11,weight='bold',bbox=dict(fc='white',ec='none',alpha=.85))
ax.set_aspect('equal');ax.set_xlim(0,295);ax.set_ylim(0,155);ax.set_xticks(np.arange(0,296,25));ax.set_yticks(np.arange(0,156,25));ax.grid(alpha=.12);ax.set_xlabel('X / m');ax.set_ylabel('Y / m')
ax.set_title('B1 · Mở lại tuyến mall quanh lõi mới',loc='left',fontsize=19)
footer(fig,f'B02 / R2   Xanh: mall R2 · Nét vàng: mall R1 · Nâu: quỹ ram · Xám: vùng riêng tư B/C. Tham số bề rộng tuyến {st["mall_width_R1"]:.2f} → {st["mall_width_R2"]:.2f} m; không phải bề rộng thông thủy hành lang.')
save(fig,'B02-mall-core-adjustment')
fig,ax=plt.subplots(figsize=(15,11));fig.subplots_adjust(left=.09,right=.98,top=.91,bottom=.1)
zonecolors=['#298d9f','#4aa58e','#8da85b','#b99753'];xloc=[1,2.5,4]
for zi,(lo,hi,base) in enumerate([(8,30,0),(33,54,147.2),(57,78,256),(81,97,364.8)]):
    bs=[b for b in s['banks'] if b['id'].startswith(f'A-Z{zi+1}')]
    for bi,b in enumerate(bs):
        top=fl('A',b['served_floors'][-1])['z'];x=xloc[bi]
        ax.add_patch(Rectangle((x-.42,base),.84,top-base,fc=zonecolors[zi],alpha=.9))
        ax.text(x,(base+top)/2,f'5 xe\n{b["served_floors"][0]}–{b["served_floors"][-1]}',ha='center',va='center',fontsize=9,color='white',weight='bold')
        ax.plot([x-.42,x+.42],[top+5.5]*2,color=zonecolors[zi],lw=2)
for i,b in enumerate(s['shuttles']):
    x=6+i*1.5;ax.add_patch(Rectangle((x-.42,0),.84,b['terminal_z'],fc='#41559a',alpha=.87));ax.text(x,b['terminal_z']/2,f'E{i+2}\n6 xe',color='white',ha='center',va='center',weight='bold')
ax.add_patch(Rectangle((10.5,0),.65,445.6,fc='#ac7652'));ax.text(10.83,223,'4 vùng\nphục vụ',ha='center',va='center',color='white')
for n in [31,32,55,56,79,80,98]:
    f=fl('A',n);ax.axhspan(f['z'],f['top'],color='#bfc8d2',alpha=.25);ax.text(11.5,f['z']+1,f'A{n:02d}  +{f["z"]:.1f}',fontsize=8,va='bottom')
ax.set_ylim(-3,462);ax.set_xlim(0,14);ax.set_xticks([1,2.5,4,6,7.5,9,10.83]);ax.set_xticklabels(['K1','K2','K3','E2','E3','E4','AS']);ax.set_ylabel('Z / m');ax.grid(axis='y',alpha=.16);ax.set_title('A · Giếng local tái dùng theo các đoạn, shuttle chạy xuyên dưới',loc='left',fontsize=18)
footer(fig,'V02 / R2   37 giếng thang tại đế ≠ 77 xe trong toàn tháp: các bộ thang local độc lập xếp nối theo chiều cao. Biểu đồ không thể hiện đường thoát nạn.')
save(fig,'V02-vertical-zoning')
fig,ax=plt.subplots(figsize=(15,7));fig.subplots_adjust(left=.12,right=.96,top=.88,bottom=.22)
bs=s['banks']+s['shuttles'];y=np.arange(len(bs));ax.barh(y,[-b['demand_5min'] for b in bs],color='#b99753',label='Nhu cầu / 5 phút');ax.barh(y,[b['capacity_5min'] for b in bs],color='#298d9f',label='Công suất mô hình / 5 phút');ax.set_yticks(y);ax.set_yticklabels([b['id'] for b in bs]);ax.invert_yaxis();ax.axvline(0,color='#263746',lw=.8);ax.set_xlabel('Người / 5 phút · nhu cầu bên trái, công suất bên phải');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.17),ncol=2,frameon=False);ax.grid(axis='x',alpha=.13);ax.set_title('Sàng lọc công suất · mật độ văn phòng 12 m² net/người',loc='left',fontsize=18)
footer(fig,'T02 / R2   Công suất là xấp xỉ từ RTT; chưa có hàng đợi hay mô phỏng điều phối DCS. A-Z1-1 / A-Z1-2 có dự phòng thấp.')
save(fig,'T02-traffic-screen')

def num(v):return f'{v:,.0f}'.replace(',','.')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows)
coretable=table(['Tháp / đoạn','Vùng local u / v, m','R1 → R2, m²','Lý do'],[
['A01–A33','u −21..21; v −18..18','1.088 / 840 → 1.512','Giữ 15 local + 18 express + 4 phục vụ; đầu giếng E2'],
['A34–A57','u −21..21; v −18..14','840 / 728 → 1.344','E2 đã kết thúc; giữ E3/E4 và đầu giếng E3'],
['A58–A81','u −15..21; v −14..14','728 / 576 → 1.008','E3 đã kết thúc; E4 giữ tới hết A81'],
['A82–A98','u −15..15; v −13..13','576 → 780','10 local, 4 phục vụ, 3 vùng thang bộ và kỹ thuật'],
['D01–D34','u −16..16; v −16..16','624 → 1.024','14 văn phòng + 7 khách sạn + 2 phục vụ'],
['D35–D62','u −14..14; v −10..10','384 → 560','Thang khách sạn và phục vụ liên tục'],])
bt=table(['Nhóm','Tầng phục vụ','Xe','P / chuyến','RTT s','Interval s','HC / nhu cầu, người/5 phút'],[[b['id'],f"{b['served_floors'][0]}–{b['served_floors'][-1]}" if 'served_floors'in b else f"01 → {int(b['id'][-1])*24-16:02d}",b['cars'],b['P_effective'],f"{b['RTT_s']:.1f}",f"{b['interval_s']:.1f}",f"{b['capacity_5min']:.0f} / {b['demand_5min']:.0f}"] for b in bs])
# Correct shuttle terminals are explicit, not computed from zone index.
for zone,level in [(2,32),(3,56),(4,80)]:bt=bt.replace(f'| A-E{zone} | 01 → {zone*24-16:02d} |',f'| A-E{zone} | 01 → {level:02d} |')
ct=table(['Nhóm','P hiệu dụng','Diện tích cabin thông thủy tối thiểu ở 80% tải diện tích','Quỹ ngoài tường / giếng','Tải khởi điểm nghiên cứu'],[
['Local A','22 (nhóm cuối thấp 20)','5,78 m² (P20: 5,25)','3,40 × 4,00 m','~3.200 kg'],
['Shuttle A','33','8,67 m²','4,00 × 4,20 m','~5.000 kg; cần cabin cao tốc lớn'],
['Văn phòng D','26','6,83 m²','3,40 × 3,80 m','~4.000 kg'],
['Khách sạn D','16, có hành lý','6,00 m²','3,40 × 3,80 m','~3.200 kg'],])
nt=table(['Chỉ tiêu','R1','R2 hiện tại','Sai khác'],[
['Proxy net văn phòng A',num(st['A_office_net_R1_proxy']),num(st['A_office_net_R2_proxy']),f"−{num(st['A_office_net_R1_proxy']-st['A_office_net_R2_proxy'])} m²"],
['Proxy net văn phòng D',num(st['D_office_net_R1_proxy']),num(st['D_office_net_R2_proxy']),f"−{num(st['D_office_net_R1_proxy']-st['D_office_net_R2_proxy'])} m²"],
['Mall B1','14.000','14.000','0'],['Quỹ B1 còn lại','23.125','23.125','0; gồm lõi và kỹ thuật'],
['Tham số bề rộng tuyến mall',f"{st['mall_width_R1']:.2f} m",f"{st['mall_width_R2']:.2f} m",'Mở băng dưới đất; quảng trường mặt đất vẫn theo R1'],
['GFA kiểm soát toàn khu','631.690,24','631.690,24','0'],['Dự phòng FAR','8.459,76','8.459,76','0'],])
sections=[]
def sec(name,txt):sections.append((name,txt.strip()+'\n'))
sec('00-co-so',f'''
# HỘI LƯU · R2
## Kiểm tra lõi và giao thông đứng A/D
**Ngày phát hành 30/09/2026 (giờ Việt Nam) · Tiếp tục hồ sơ R1 · Đơn vị mét**

R2 đưa vùng giữ chỗ lõi thành một phương án giếng thang có tọa độ, các nhóm phục vụ và phép tính dân số. Phương án hiện tại giữ đường bao, số tầng và GFA của R1; thay đổi vùng lõi, một số lỗ mở và tuyến mall B1. Đây là phương án kiểm tra bằng thang một cabin, chưa phải cấu hình tối ưu để đặt mua.

**Kết luận chính:** bố trí hiện tại dùng lõi lớn hơn R1, làm giảm proxy diện tích văn phòng net khoảng 28.080 m² ở A và 9.360 m² ở D. Nó cho thấy giá phải trả để giữ vỏ tháp khi dùng cấu hình này, chứ chưa chứng minh các kích thước lõi là mức tối thiểu bắt buộc. Hai nhóm thang thấp A có dự phòng công suất rất nhỏ. Cần tối ưu điều phối/loại thang trước khi khóa lõi hoặc định giá cho thuê.

| Trạng thái | Thành phần |
| --- | --- |
| Giữ từ R1 | Đất 295×155 m; vị trí A/D/B/C; đế 6 tầng; A 98 tầng / 480 m; D 62 tầng / 285 m; ngân sách thân 300.000 / 120.000 m² |
| Đề xuất mới R2 | Lõi và giếng có tọa độ; A bốn vùng; D khách sạn trực tiếp; các lỗ mở được phối hợp lại; mall B1 vẫn 14.000 m² |
| Giả định để tính | 12 m² proxy net/người văn phòng; cao điểm 12%/5 phút; khách sạn 360 keys để thử tải; thông số động học và cabin sơ bộ |
| Chưa khóa | Nhà cung cấp, tiết diện tường chịu lực, mặt bằng phòng khách sạn, vận hành khách sạn hai chiều, PCCC, số thang mall/xe và tải phục vụ |

Nguồn: bản R1 đã lưu, mã Library `libfile_3b79feabef24819185e35ced52e4ae2b`. Thư mục `source-r1/` là bản tham chiếu. JSON R2 và bản vẽ R2 mới là nguồn cho những thay đổi tại lần này. OBJ bên trong nguồn R1 vẫn chứa lõi/lỗ mở cũ, chỉ dùng xem khối ngoài.
''')
sec('01-core',f'''
# 01 · Từ vùng giữ chỗ sang cấu trúc lõi
{coretable}
Tâm tháp vẫn A (53;49), D (238;104). Tọa độ trên là hệ local, không phải tọa độ đất. Các lõi trên A giảm lệch về phía có shuttle kết thúc, tránh cắt một giếng thang còn đang đi xuyên. Lõi thu ở A34/A58/A82, sau tầng sky lobby và khoảng đầu giếng; không thu ngay tại A31/A55/A79.

![A02](drawings/A02-core-reservations.svg)

Phần tô nhạt là toàn bộ quỹ lõi kiến trúc: tường, giếng, thang bộ, sảnh/circulation, MEP và vệ sinh còn phải phát triển. Các ô tô màu là module giữ chỗ **ngoài tường**, không phải kích thước cabin hoặc giếng thông thủy được hãng xác nhận. Ô AS là phục vụ; AT là thang bộ. A giữ ba vùng thang bộ, D hai vùng; số lượng và bề rộng thoát nạn chưa được xác nhận bởi phép tính dân số hay kiểm tra PCCC.

Các mũi cửa xác định phía mở sơ bộ. Lối local A đi qua hai sảnh giữa hàng K và các tuyến vòng ở hai bên. Các shuttle mở về phía ngoài lõi tại sảnh đế/sky lobby; ở tầng đi xuyên giếng đóng kín. Cần thiết kế sảnh mở ngoài lõi tại A01/A32/A56/A80 trong quỹ riêng/phụ trợ đã có. Phần nền nhạt chưa phải sơ đồ phân khoang, tường chịu lực hay hành lang chống khói.

Vùng lõi R2 nằm trong biên sàn thật của mọi tầng. Điều này kiểm tra được bằng polygon; việc có thể đặt cabin, counterweight, ray, cửa, hố pit và phòng máy thật trong từng module vẫn là bước riêng. Không có phép kiểm tra packing toàn cục chứng minh rằng một lõi nhỏ hơn không thể làm được.
''')
sec('02-A',f'''
# 02 · Tháp A: bốn vùng và ba tuyến shuttle

| Vùng | Tầng văn phòng | Tầng đón | Tổ chức local |
| --- | --- | --- | --- |
| Z1 | A08–A30 | Sảnh riêng A01 | 08–15 / 16–23 / 24–30, mỗi nhóm 5 xe |
| Z2 | A33–A54 | A32 +147,20 m | 33–40 / 41–47 / 48–54, mỗi nhóm 5 xe |
| Z3 | A57–A78 | A56 +256,00 m | 57–64 / 65–71 / 72–78, mỗi nhóm 5 xe |
| Z4 | A81–A97 | A80 +364,80 m | 81–89 / 90–97, mỗi nhóm 5 xe |

Khách Z1 đi từ sảnh A01 lên trực tiếp. Khách Z2/Z3/Z4 dùng ba nhóm E2/E3/E4 riêng, mỗi nhóm 6 xe express, lên đúng sky lobby rồi chuyển sang local. Không cho thang mall vận hành như một đoạn trong hành trình đi làm. A07 giữ phụ trợ/amenity theo R1; các lượt phát sinh ở đây chưa đưa vào mô hình cao điểm.

Tại đế có **37 giếng thang**: 15 local Z1, 18 shuttle và 4 phục vụ. Toàn tháp giữ chỗ **77 xe/bộ thang**: 55 local ở bốn đoạn, 18 shuttle, 4 phục vụ. Đây là 77 thiết bị riêng, không phải 77 giếng chạy suốt từ đất đến mái; cũng không phải tổng thang toàn dự án. Cấu hình có nhiều thiết bị vì chưa ghi nhận lợi ích DCS hoặc double-deck; mục đích hiện tại là bộc lộ quỹ không gian và chi phí vận hành của phương án một cabin.

![V02](drawings/V02-vertical-zoning.svg)

Local mỗi vùng dùng lại các vị trí K ở đoạn trên, với máy, cabin và pit độc lập. Nhóm thấp chỉ chạy tới tầng cuối của nhóm nó; bảng nối kiểm tra tầng cuối cao nhất từng vùng là trường hợp chặt nhất. Ba hàng K là vị trí, không phải ba tuyến thang xuyên suốt 98 tầng.

| Cụm nối | Landing cuối dưới | Đầu giếng dưới, +5,5 m | Đáy pit trên, −2,0 m | Khoảng còn lại |
| --- | --- | --- | --- | --- |
''' + ''.join(f'| A{x["last_floor"]}/A{x["first_floor"]} | +{x["last_landing"]:.2f} | +{x["overhead_top"]:.2f} | +{x["upper_pit_bottom"]:.2f} | {x["remaining_gap"]:.2f} m |\n' for x in s['transfers']) + '''
Các khoảng nối còn phải dành tối thiểu 0,40 m cho slab giả định, cộng dầm/máy/đường tiếp cận thật. Số +5,5 m và −2,0 m là yêu cầu quỹ đang thử; không phải catalogue hãng. Đầu giếng shuttle giữ 6,5 m qua tầng cuối: E2 đến +153,70; E3 +262,50; E4 +371,30 m. Bởi vậy lõi chỉ thu từ A34, A58, A82.

AS1–AS4 là bốn vị trí phục vụ/cứu hỏa dự kiến; chức năng từng xe, phạm vi tầng và tải hàng chưa khóa. Không được tự gọi một ô AS là thang chữa cháy đạt chuẩn. Các tuyến dài gần toàn chiều cao tháp cần xác nhận travel, ray và chuyển vị công trình cùng hãng và kết cấu.
''')
sec('03-D',f'''
# 03 · Tháp D: tách khách sạn và văn phòng
![D02](drawings/D02-core-reservations.svg)

Hai nhóm văn phòng DL/DH, mỗi nhóm 7 xe, từ sảnh văn phòng D01 lên D07–D19 hoặc D21–D33. D20/D34 là các tầng kỹ thuật/lánh nạn giữ chỗ; lượt phục vụ không được coi là một tầng văn phòng đông người.

Bảy thang khách sạn H đi **trực tiếp từ sảnh khách sạn D01** qua vùng văn phòng, dừng D35 và các tầng khách sạn được chọn. Khách không phải đổi cabin ở D35 để lên phòng. D35 vẫn giữ sky lobby, lounge và lớp kính lùi 3 m theo R1. Một số xe có thể được điều phối express lên lounge vào thời điểm cụ thể, nhưng không tính chúng thành nhóm express độc lập rồi cộng thêm xe lần nữa.

Hai HS đi từ BOH B1/đế lên vùng khách sạn, với cửa ở phía BOH; cần kiểm tra tách hàng sạch, hàng bẩn, rác và housekeeping. Bảy thang khách và hai thang phục vụ chạy xuyên lõi văn phòng. Thang văn phòng kết thúc D33; đầu giếng giả định +5,5 m đạt +152,70 m trong D34, trước khi thu lõi tại D35 +157,45 m.

**360 keys chỉ là tải thử**, gồm 20 tầng ×16 phòng và 4 tầng ×10 suite. D37–D47 + D49–D57 là 20 tầng thường, D58–D61 là bốn tầng suite. D36 dành phụ trợ/amenity để phối hợp lỗ thông với D35; D48/D62 giữ kỹ thuật. Đây chưa phải mặt bằng module phòng, không phải cam kết yield 360 phòng cao cấp.

Tải khách dùng 360×1,8+50 = 698 người để sàng lọc. Bảng RTT chỉ thử chiều từ sảnh lên; khách sạn có hai chiều, nhà hàng/lounges và thời điểm trả phòng, nên **chưa được xác nhận vận hành**. HS không góp vào công suất thang khách. D35/lounge và các sự kiện riêng cần thêm dân số và mô phỏng riêng.
''')
sec('04-calculation',f'''
# 04 · Cơ sở tính và giới hạn công suất
ISO 8100-32 đề cập việc lập kế hoạch, chọn thang cho văn phòng/khách sạn/nhà ở [1]. CIBSE Guide D 2025 phân biệt tính toán và mô phỏng [2–3]. R2 thực hiện phép sàng lọc bằng hành trình ngẫu nhiên, chưa thực hiện mô phỏng hàng đợi hoặc điều phối.

Proxy net từng tầng văn phòng = **0,90 × (GFA sàn − quỹ lõi)**. Sau khi trừ lõi, 10% tiếp theo dự trữ cho tổn thất sử dụng còn lại. Đây là proxy để tính dân số, không phải NLA chứng nhận: các cột, phòng MEP ngoài lõi, sảnh ngoài lõi và tỷ lệ phân chia khách thuê chưa có mặt bằng hoàn chỉnh. Không áp hệ số 90% lên GFA rồi trừ lõi thêm lần nữa.

Dân số = proxy net /12 m²; nhu cầu =12% dân số/5 phút. Mục tiêu nghiên cứu R2 là interval văn phòng ≤35 s, shuttle ≤30 s, khách sạn ≤40 s. **Các số này là giả định mục tiêu của dự án, không phải trích dẫn yêu cầu ISO/QCVN.** Nếu muốn mức 30 s cho mọi nhóm văn phòng, nhiều nhóm hiện tại cần tăng xe hoặc đổi điều phối.

Tổng dân số proxy: A **{num(st['A_population'])}**, văn phòng D **{num(st['D_office_population'])}**. Các tầng hỗ trợ/MEP không bị gán dân số văn phòng; tải phụ trợ có thật vẫn phải bổ sung khi công năng được khóa.

Mỗi nhóm lấy 12.000 chuyến, seed cố định 20260929. Một chuyến có P hành khách chọn tầng theo tỷ lệ dân số, dừng theo thứ tự tăng cao độ, rồi trở về terminal. Thời gian flight dùng profile gia tốc 1 m/s²: với d nhỏ hơn v²/a là 2√(d/a), còn lại d/v+v/a. Cộng 7 s mỗi điểm dừng/terminal cho cửa và leveling, cộng 2×P×1 s cho boarding/alighting. Khách sạn dùng 8 s và 1,2 s. Profile chưa mô tả jerk; các thông số phải thay bằng đường cong hãng.

HC = 300×số xe×P / RTT. Interval = RTT/số xe. **Interval không phải thời gian chờ đo được**; cũng không được cộng HC local và HC shuttle để tuyên bố công suất đường đi. Một hành trình A trên cao bị giới hạn bởi mắt xích yếu nhất.

{bt}
![T02](drawings/T02-traffic-screen.svg)

A-Z1-1 dự phòng khoảng {s['banks'][0]['capacity_margin_pct']:.1f}%, A-Z1-2 khoảng {s['banks'][1]['capacity_margin_pct']:.1f}%. Đây là mức rất mỏng, không nên khóa phương án như một hệ thống premium đã ổn định. Sai số lấy mẫu nhỏ không giải quyết được sai số giả định dân số, thời gian cửa hoặc lưu lượng người. Một ca thang ngừng hoạt động làm nhóm thấp A và một số tuyến shuttle thiếu công suất hoặc vượt interval.

Kịch bản 10 m² net/người làm ba nhóm local thấp A vượt HC; E2/E3 cũng thiếu công suất khi nâng dân số tương ứng. Mô hình cơ sở không được dùng cấp phép cho thuê mọi tầng ở mật độ 10 m²/người. Cần chạy cao điểm 15%, lunch/interfloor, mixed traffic, tải amenity và một xe ngừng hoạt động trong mô phỏng tiếp theo.
''')
sec('05-cabin',f'''
# 05 · Cabin cần được kiểm tra bằng diện tích
Bài trình bày CIBSE của Richard Peters chỉ rõ số người hiệu dụng phải kiểm tra bằng diện tích cabin, không thể chỉ lấy kg chia khối lượng người rồi nhân 80%; ví dụ diện tích mỗi người 0,21 m² cho văn phòng và 0,30 m² cho khách sạn/nhà ở [4]. R2 dùng các giá trị đó để đặt **yêu cầu diện tích cabin**, không giả định cabin lớn chỉ vì tải trọng ghi lớn.

Diện tích thông thủy yêu cầu = P × diện tích/người ÷0,80. Tải khởi điểm dưới đây là mục để trao đổi hãng; chưa chọn một sản phẩm đáp ứng đồng thời tải, diện tích, tốc độ và travel.

{ct}

Quỹ module bao gồm dự trữ tường và không được sử dụng như clear shaft. Các mức tải/cabin này khá lớn, nhất là shuttle A 10 m/s. Nếu hãng không cung cấp được cabin phù hợp trong module, phải đổi số xe, P, tốc độ hoặc lõi và chạy lại số học. Không được giữ P33 rồi âm thầm thay bằng cabin thông thường nhỏ hơn. Những phép kiểm tra polygon ở đây không chứng minh khả năng lắp thiết bị.

Khuyến nghị bước tối ưu: thử DCS trên dân số đã khóa; so cấu hình double-deck với single-deck; so 35 s và 30 s; dùng cabin area thật. Double-deck có thể giảm số giếng nhưng cần trả lại diện tích cho sảnh hai cao độ và lối chuyển. Các cặp A31/32, 55/56, 79/80 đều cách 6 m, phù hợp để nghiên cứu, nhưng tầng dưới đang giữ cho kỹ thuật/outrigger; cần tách luồng và kiểm tra pit local trước khi chọn.
''')
sec('06-geometry',f'''
# 06 · Điều chỉnh hình học và B1
![P02](drawings/P02-floor-envelope.svg)

Lỗ mở A32/A56/A80 đặt phía Đông trong R1 chồng lên tuyến E4 của bố trí mới. R2 chuyển chúng về phía +v (chưa phải Bắc địa lý), giữ mỗi lỗ **96 m²**: A32 u −8..8, v 18..24; A56/A80 u −8..8, v 17..23. A02 điều chỉnh hình lỗ/khuyết 1.950 m² để tránh lõi mới, giữ đúng diện tích khấu trừ và GFA tầng. Các thay đổi này có tọa độ trong JSON; OBJ R1 không phản ánh chúng.

![B02](drawings/B02-mall-core-adjustment.svg)

Lõi xuyên B1 tăng A 1.088→1.512, D 624→1.024 m². Nếu chỉ trừ lõi mới khỏi mall cũ, diện tích còn **13.176 m²**, thiếu 824 m². R2 mở băng nối dưới quảng trường bằng phép giải diện tích, giữ hai anchor, quỹ ram và vùng riêng tư B/C. Tham số tạo băng tăng 24,60→44,36 m; nó không phải một hành lang mall thông thủy rộng 44 m. Mall thật còn bao gồm anchor, cửa hàng, khu BOH, lối đi và các lỗ lõi.

Mall B1 vẫn là một polygon liên thông **14.000 m²**; không chạm đế hoặc buffer riêng tư 6 m của B/C, không chồng quỹ ram. B1 còn lại 23.125 m² gồm đỗ xe, kỹ thuật và lõi. Quỹ mall đế A 21.000 + D 17.000 và B1 14.000 =52.000 m² gross vẫn được giữ **ở cấp budget**. R2 chưa chia cửa hàng và chưa chứng minh sảnh riêng lớn hơn vẫn nằm gọn trong 7.000/5.000 m² private của đế A/D; đó là điểm phải kiểm tra trước khi chốt mặt bằng mall.

B2–B5 mỗi tầng 37.125 m² vẫn chỉ để xe/kỹ thuật. Tổng 185.625 m² hầm không thay đổi. Quỹ ram 18×60 m ở R1 vẫn là vùng giữ chỗ, chưa có độ dốc hay bán kính quay thật. Chưa đưa ra số ô xe vì chưa có lưới cột, phòng máy, bể, đường chạy, phân khoang và hình học ram. Thang xe/mall được bố trí ngoài core thân và phải được bổ sung tọa độ/tải; không tính vào 77/23 thiết bị phía trên.

{nt}
''')
sec('07-checkpoint',f'''
# 07 · Checkpoint và bước phát triển tiếp
**{len(s['checks'])}/{len(s['checks'])} điều kiện hình học/số học đạt** trong bản chạy này. Trong số đó có nhiều phép so chồng từng cặp module; số lượng lớn không có nghĩa hồ sơ đã gần thi công. Kiểm tra gồm lõi/lỗ mở trong biên từng tầng, bảo toàn GFA, module không chồng nhau, phần giếng còn hoạt động nằm trong lõi đúng đoạn, nối đầu giếng/pit theo giả định, B1 giữ diện tích/độ liên thông và 17 nhóm thang vượt phép sàng lọc cơ sở.

Không có kiểm tra: wall/core structural analysis, cabin CAD, fire/smoke compartment, travel-distance evacuation, manufacturer dispatch simulation, shaft clearances under drift, hotel room packing, detailed parking/ramp, operational resilience. Cụm “screen_pass” trong JSON chỉ chỉ điều kiện RTT/HC và interval của giả định tương ứng.

**Quyết định kiến trúc t đề xuất:** giữ vỏ R1 và dùng R2 này làm biên không gian để kiểm tra tiếp, chưa khóa lõi 1.512/1.024 m² như thiết kế tối ưu. Ưu tiên giải hai nhóm thấp A trước; song song lấy cabin/shaft/headroom từ hãng để so single-deck/DCS/double-deck. Chỉ sau đó khóa lõi, lập mặt bằng phòng D và phân chia mall. Mức net thất thoát hiện tại đủ lớn để yêu cầu tối ưu kỹ thuật trước khi phát triển nội thất hoặc phối cảnh.

| Gói việc tiếp | Sản phẩm cần ra |
| --- | --- |
| Tối ưu A | So số giếng, net floor, thời gian hành trình tổng và một xe hỏng; giải Z1 trước |
| Phối hợp hãng | Cabin area, tải, shaft clear, pit, overhead, machine space, travel từng nhóm |
| Lõi/kết cấu/PCCC | Tường và dầm thật, lobbies có bảo vệ, cầu thang/chiều rộng/lánh nạn phù hợp hồ sơ địa điểm |
| D phòng + vận hành | Module phòng trong biên thật; xác nhận keys, BOH, lounge, mixed hotel traffic |
| Hầm + đế | Lưới cột, ram thật, core/mall/parking lifts, private lobbies và cửa hàng trong gross budget |

## Tài liệu và cách dùng
`HOI_LUU_R2.html` chứa toàn bộ báo cáo/bản vẽ, đọc độc lập. `data/geometry-r2.json` là nguồn polygon/cao độ; `data/r2-study.json` chứa giả định, 17 nhóm, module và kiểm tra; hai CSV dùng trao đổi số liệu. Các SVG zoom không vỡ. `scripts/build_r2.py` và `build_drawings_report.py` tái tạo bộ này từ nguồn R1; không cần ảnh GenAI.

## Nguồn tham khảo kỹ thuật
1. [ISO 8100-32:2020 — phạm vi lập kế hoạch và chọn thang](https://www.iso.org/standard/73084.html). Chỉ sử dụng trang mô tả phạm vi; chưa tuyên bố tuân thủ toàn văn.
2. [CIBSE Guide D3 — Lift traffic design using calculation, 2025](https://www.cibse.org/knowledge-research/knowledge-portal/guide-d3-lift-traffic-design-using-calculation-2025/).
3. [CIBSE Guide D4 — Lift traffic design using simulation, 2025](https://www.cibse.org/knowledge-research/knowledge-portal/guide-d4-lift-traffic-design-using-simulation-2025/).
4. [Richard Peters / CIBSE — 80% Lift Traffic Design’s Most Misunderstood Number, 12/11/2025](https://www.cibse.org/media/x0sfnskv/80-lift-traffic-design-s-most-misunderstood-number-cibse.pdf). Tham chiếu điều kiện sức chứa theo diện tích cabin.
5. [KONE — Elevator planning handbook for architects](https://www.kone.com/en/Images/8559_Global_EN_Elevator_Planning_Handbook_tcm17-75237.pdf). Tham chiếu quy trình phối hợp early planning, shaft và overhead; không dùng để xác nhận sản phẩm cho R2.

Đây là nghiên cứu kiến trúc do trợ lý xây dựng theo hướng ưu tiên hình học/kết cấu; không phải tài liệu do SOM phát hành hoặc kiểm duyệt.
''')
combined='\n\n'.join(t for _,t in sections)
(ROOT/'HOI_LUU_R2.md').write_text(combined)
for name,txt in sections:(ROOT/'docs'/f'{name}.md').write_text(txt.replace('(drawings/','(../drawings/'))
body=markdown.markdown(combined,extensions=['tables','fenced_code'])
for p in (ROOT/'drawings').glob('*.svg'):
    svg=p.read_text();svg=svg[svg.index('<svg'):]
    body=body.replace(f'<img alt="{p.stem[:3]}" src="drawings/{p.name}" />',svg)
# General embedding replaces remaining image tags by exact referenced SVG.
import re
body=re.sub(r'<img alt="[^"]*" src="drawings/([^"]+\.svg)"\s*/>',lambda m:(ROOT/'drawings'/m.group(1)).read_text().split('<svg',1)[0]*0+'<svg'+(ROOT/'drawings'/m.group(1)).read_text().split('<svg',1)[1],body)
style='''body{font-family:system-ui,Arial,sans-serif;color:#253746;background:#f0f3f3;margin:0;line-height:1.65}main{max-width:1140px;margin:0 auto;background:white;padding:55px 60px}h1{font-size:30px;border-top:2px solid #287e87;padding-top:28px;margin-top:50px}h2{font-size:21px}p{max-width:1000px}table{border-collapse:collapse;width:100%;font-size:14px;margin:24px 0}th{background:#263d4c;color:white;text-align:left}td,th{padding:10px;border:1px solid #d4dde1;vertical-align:top}tr:nth-child(even){background:#f3f6f6}svg{width:100%;height:auto;display:block;margin:30px 0}code{font-size:13px;background:#edf2f3;padding:2px 4px}a{color:#227883}@media(max-width:700px){main{padding:25px 14px}table{font-size:11px}td,th{padding:5px}}@media print{body{background:white}main{padding:0}h1{break-before:page}svg,table{break-inside:avoid}a{color:inherit}}'''
(ROOT/'HOI_LUU_R2.html').write_text('<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HỘI LƯU R2 · Lõi và giao thông đứng</title><style>'+style+'</style><main>'+body+'</main></html>')
(ROOT/'README.md').write_text('''# HỘI LƯU R2\n\nMở HOI_LUU_R2.html để đọc hồ sơ và sáu bản vẽ vector.\n\nR2 là nghiên cứu lõi/giao thông đứng sơ bộ. Vỏ, cao độ, ngân sách GFA giữ R1. Lõi/lỗ mở/B1 đã cập nhật trong data/geometry-r2.json. Các kiểm tra không phải chứng nhận thi công hoặc vận hành.\n\nsource-r1/ là nguồn tham chiếu, có OBJ chứa lõi/lỗ mở cũ. Không dùng OBJ đó như mô hình nội bộ R2. Chưa phát hành BIM/OBJ nội bộ R2.\n\nTái tạo: python scripts/build_r2.py rồi python scripts/build_drawings_report.py. Python + numpy, scipy, shapely, matplotlib, markdown. Seed và giả định được giữ trong r2-study.json.\n''')
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and p.name!='manifest.json'}
(ROOT/'data/manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'drawings':6,'HTML_bytes':(ROOT/'HOI_LUU_R2.html').stat().st_size,'checks':len(s['checks']),'failed_checks':[c['name'] for c in s['checks'] if not c['passed']]}))
