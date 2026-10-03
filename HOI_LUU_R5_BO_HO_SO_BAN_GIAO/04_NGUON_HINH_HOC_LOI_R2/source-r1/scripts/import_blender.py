"""Run in Blender's Text Editor. No addons required. Does not delete existing objects.
The imported object is an architectural control surface, not structural BIM.
"""
from pathlib import Path
import json, math
import bpy
from mathutils import Vector

try:
    PACKAGE = Path(__file__).resolve().parents[1]
except NameError:
    PACKAGE = Path('/CHANGE/TO/hoi-luu-r1')
if not (PACKAGE/'model/hoi-luu-r1.obj').is_file():
    raise RuntimeError('Set PACKAGE to the extracted hoi-luu-r1 folder.')

collection=bpy.data.collections.new('HOI_LUU_R1')
bpy.context.scene.collection.children.link(collection)
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=1.0
colors={'glass_A':(.38,.54,.63,1),'glass_D':(.57,.65,.67,1),'silver':(.78,.80,.79,1),
        'podium':(.75,.73,.66,1),'residential':(.61,.66,.65,1),'site':(.88,.87,.83,1)}
materials={}
for name,col in colors.items():
    m=bpy.data.materials.new('HL_R1_'+name);m.diffuse_color=col;m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=col;bsdf.inputs['Roughness'].default_value=.28 if name.startswith('glass') else .5
    materials[name]=m

vertices=[];groups=[];current=None
for line in (PACKAGE/'model/hoi-luu-r1.obj').read_text().splitlines():
    parts=line.split()
    if not parts:continue
    if parts[0]=='v':vertices.append(tuple(map(float,parts[1:4])))
    elif parts[0]=='o':
        current={'name':parts[1],'faces':[],'material':'podium'};groups.append(current)
    elif parts[0]=='usemtl' and current is not None:current['material']=parts[1]
    elif parts[0]=='f':current['faces'].append([int(i.split('/')[0])-1 for i in parts[1:]])
for group in groups:
    used=sorted({i for f in group['faces'] for i in f});mapping={idx:i for i,idx in enumerate(used)}
    mesh=bpy.data.meshes.new(group['name']);mesh.from_pydata([vertices[i] for i in used],[],[[mapping[i] for i in f] for f in group['faces']]);mesh.update()
    ob=bpy.data.objects.new(group['name'],mesh);collection.objects.link(ob)
    ob.data.materials.append(materials[group['material']])
    for poly in ob.data.polygons:poly.use_smooth=('glass' in group['material'] or 'rib' in group['name'])
    ob['revision']='R1';ob['units']='metres';ob['status']='Architectural control surface; not structural BIM'

def outline(name,pts,z,material='site',radius=.15):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.bevel_depth=radius;curve.bevel_resolution=1
    spl=curve.splines.new('POLY');spl.points.add(len(pts)-1)
    for p,(x,y) in zip(spl.points,pts):p.co=(x,y,z,1)
    spl.use_cyclic_u=True
    ob=bpy.data.objects.new(name,curve);collection.objects.link(ob);ob.data.materials.append(materials[material])
G=json.loads((PACKAGE/'data/geometry.json').read_text())
outline('SITE_295x155',[(0,0),(295,0),(295,155),(0,155)],0,'silver',.2)
for b in G['basements']:
    outline('BASEMENT_'+b['name'],[(10,10),(285,10),(285,145),(10,145)],b['z'],'silver',.1)

cam_data=bpy.data.cameras.new('HL_R1_camera');cam=bpy.data.objects.new('HL_R1_camera',cam_data);collection.objects.link(cam)
cam.location=(630,-770,470);target=Vector((145,77,225));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
cam_data.type='ORTHO';cam_data.ortho_scale=610;bpy.context.scene.camera=cam
light_data=bpy.data.lights.new('HL_R1_sun','SUN');light_data.energy=2
light=bpy.data.objects.new('HL_R1_sun',light_data);collection.objects.link(light);light.rotation_euler=(math.radians(25),math.radians(-20),math.radians(-25))
bpy.context.scene.render.resolution_x=1600;bpy.context.scene.render.resolution_y=1200;bpy.context.scene.render.resolution_percentage=100
print('Imported HOI LUU R1:',len(groups),'surface objects; source data in',PACKAGE)
