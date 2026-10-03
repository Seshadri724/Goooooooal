"""Rig haru.blend (built by build_haru.py, which also makes the expression shape keys): UVs, armature + weights, GLB export.
    bash run_blender.sh rig_haru.py ../haru.blend
Saves ../haru.blend in place and writes ../haru.glb. Re-run build_haru.py first: this step is not idempotent.
"""
import bpy, math, os, traceback
from math import radians
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOG = os.path.join(HERE, "rig_haru.log")
log = open(LOG, "w")
def say(*a): print(*a, file=log, flush=True)

def select_only(objs, active):
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = active

def uv_unwrap(meshes):
    for o in meshes:
        select_only([o], o)
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=radians(66), island_margin=0.003)
        bpy.ops.object.mode_set(mode='OBJECT')

def build_armature():
    arm_data = bpy.data.armatures.new("HaruRig"); arm = bpy.data.objects.new("HaruRig", arm_data)
    bpy.data.collections["Haru"].objects.link(arm)
    arm_data.display_type = 'STICK'; arm.show_in_front = True
    select_only([arm], arm); bpy.ops.object.mode_set(mode='EDIT')
    eb = arm_data.edit_bones
    def bone(name, head, tail, parent=None, connect=False, deform=True):
        b = eb.new(name); b.head = head; b.tail = tail; b.use_deform = deform
        if parent: b.parent = eb[parent]; b.use_connect = connect
        return b
    # joint positions mirror build_haru.py (same skin skeleton)
    bone("root", (0, 0, 0), (0, 0, 0.12), deform=False)
    bone("hips", (0, 0, 0.5), (0, 0, 0.62), "root")
    bone("spine", (0, 0, 0.62), (0.005, 0, 0.76), "hips", True)
    bone("chest", (0.005, 0, 0.76), (0, 0, 0.9), "spine", True)
    bone("neck", (0, 0, 0.9), (0.005, 0, 1.0), "chest", True)
    bone("head", (0.005, 0, 1.0), (0.005, 0, 1.33), "neck", True)
    for s, sfx in ((1, ".L"), (-1, ".R")):
        sh = Vector((0, 0.125 * s, 0.865)); d1 = Vector((0.0, 0.375 * s, -0.927)).normalized(); d2 = Vector((0.06, 0.33 * s, -0.94)).normalized()
        el = sh + d1 * 0.195; wr = el + d2 * 0.18
        bone("shoulder" + sfx, (0, 0.03 * s, 0.87), sh, "chest")
        bone("upper_arm" + sfx, sh, el, "shoulder" + sfx, True)
        bone("forearm" + sfx, el, wr, "upper_arm" + sfx, True)
        bone("hand" + sfx, wr, wr + d2 * 0.085, "forearm" + sfx, True)
        bone("thigh" + sfx, (0, 0.066 * s, 0.5), (0.006, 0.068 * s, 0.29), "hips")
        bone("shin" + sfx, (0.006, 0.068 * s, 0.29), (0, 0.068 * s, 0.085), "thigh" + sfx, True)
        bone("foot" + sfx, (0, 0.068 * s, 0.085), (0.14, 0.068 * s, 0.03), "shin" + sfx, True)
    bpy.ops.object.mode_set(mode='OBJECT')
    return arm

def skin(arm, deforming, rigid):
    select_only(deforming + [arm], arm)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    segs = [(b.name, b.head_local, b.tail_local) for b in arm.data.bones if b.use_deform]
    def nearest_bone(p):
        def dist(h, t):
            d = t - h; u = max(0.0, min(1.0, (p - h).dot(d) / d.length_squared)); return (h + d * u - p).length
        return min(segs, key=lambda s: dist(s[1], s[2]))[0]
    for o in deforming:   # heat weighting can silently fail on overlapping shells: patch the gaps with the nearest bone
        bare = [v.index for v in o.data.vertices if not any(g.weight > 0.001 for g in v.groups)]
        for i in bare:
            b = nearest_bone(o.data.vertices[i].co)
            (o.vertex_groups.get(b) or o.vertex_groups.new(name=b)).add([i], 1.0, 'REPLACE')
        say(f"weights {o.name}: {len(o.vertex_groups)} groups, {len(bare)}/{len(o.data.vertices)} were unweighted -> nearest bone")
    # heat weighting gives a small detached island the nearest bone it diffuses to: the chest badge followed the arm
    shirt = next(o for o in deforming if o.name == "Shirt")
    badge = [v.index for v in shirt.data.vertices if v.co.x > 0.1 and (v.co - Vector((0.11, 0.05, 0.795))).length < 0.03]  # build_haru.py badge
    for g in shirt.vertex_groups: g.remove(badge)
    shirt.vertex_groups["chest"].add(badge, 1.0, 'REPLACE')
    say("badge verts pinned to chest:", len(badge))
    for o, b in rigid:    # rigid parts: one full-weight group + armature modifier (exports cleanly as skinning)
        vg = o.vertex_groups.new(name=b); vg.add(range(len(o.data.vertices)), 1.0, 'REPLACE')
        m = o.modifiers.new("Armature", 'ARMATURE'); m.object = arm
        o.parent = arm

try:
    objs = {o.name: o for o in bpy.data.collections["Haru"].objects}
    meshes = [o for o in objs.values() if o.type == 'MESH']
    try: uv_unwrap(meshes); say("uv: smart project on", len(meshes), "meshes")
    except Exception as e: say("uv unwrap skipped:", e)
    arm = build_armature()
    deforming = [objs[n] for n in ("Body", "Shirt", "Shorts", "Socks")]
    rigid = [(objs[n], "head") for n in ("Head", "Eyes", "Face", "Ears", "Hair", "HairCap")] + [(objs["Shoe_L"], "foot.L"), (objs["Shoe_R"], "foot.R"), (objs["Hand_L"], "hand.L"), (objs["Hand_R"], "hand.R")]
    skin(arm, deforming, rigid)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "haru.blend"))
    select_only([arm] + meshes, arm)
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, "haru.glb"), export_format='GLB', use_selection=True,
                              export_skins=True, export_morph=True, export_yup=True)
    say("exported", os.path.join(ROOT, "haru.glb"), os.path.getsize(os.path.join(ROOT, "haru.glb")) // 1024, "KB")
    say("DONE")
except Exception:
    say(traceback.format_exc()); say("FAILED")
log.close()
