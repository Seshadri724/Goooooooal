"""Add a second hairstyle, HairSwept (side-swept fringe + three long back locks), to the rigged haru.blend and re-export haru.glb.
    bash run_blender.sh swept_hair.py ../haru.blend
The game shows Hair (spiky) or HairSwept (+ the shared HairCap) per fighter (`spiky` on a character) and recolours it.
Not idempotent: it removes an existing HairSwept first, so re-running is fine; the rest of the file is untouched.
"""
import bpy, bmesh, math, os, random, traceback
from math import radians, sin, cos, pi
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
log = open(os.path.join(HERE, "swept_hair.log"), "w")
def say(*a): print(*a, file=log, flush=True)

HC, HA, HB, HZ = Vector((0.006, 0, 1.12)), 0.13, 0.132, 0.135   # head centre + radii (build_haru.py)
def lin(h):
    h = h.lstrip('#'); f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(f(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)) + (1,)
mix = lambda a, b, t: tuple(x + (y - x) * t for x, y in zip(a, b))
H_ROOT, H_MID, H_TIP = lin('#8e0a1c'), lin('#dc1020'), lin('#ff2e36')   # the game re-derives a root->tip ramp from the brightness

def bezier(p0, p1, p2, n):
    return [(p0 * (1 - t) ** 2 + p1 * 2 * t * (1 - t) + p2 * t * t) for t in (i / (n - 1) for i in range(n))]

def tube(bm, cl, pts, radii, ref, seg=10):
    """Tapered tube along pts into bm; radii[i] = (across, along) and a last 0 closes it to a point; vertex colour root->tip."""
    n, rings = len(pts), []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        u = ref if abs(t.dot(ref.normalized())) < 0.97 else Vector((1, 0, 0))
        nn = t.cross(u).normalized(); bb = t.cross(nn).normalized()
        col = mix(H_ROOT, H_MID, min(1, i / (n - 1) / 0.45)) if i / (n - 1) < 0.45 else mix(H_MID, H_TIP, (i / (n - 1) - 0.45) / 0.55)
        r = radii[i]
        if r == 0:
            v = bm.verts.new(p); v[cl] = col; rings.append(v); continue
        ring = []
        for j in range(seg):
            a = 2 * pi * j / seg; v = bm.verts.new(p + nn * (r[0] * cos(a)) + bb * (r[1] * sin(a))); v[cl] = col; ring.append(v)
        rings.append(ring)
    for k in range(n - 1):
        a, b = rings[k], rings[k + 1]
        for j in range(seg):
            bm.faces.new((a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j]) if isinstance(b, list) else (a[j], a[(j + 1) % seg], b))
    c = bm.verts.new(sum((v.co for v in rings[0]), Vector()) / seg); c[cl] = rings[0][0][cl]   # root cap
    for j in range(seg): bm.faces.new((c, rings[0][(j + 1) % seg], rings[0][j]))

def dirn(phi, theta):
    ph, th = radians(phi), radians(theta)
    return Vector((sin(ph) * cos(th), sin(ph) * sin(th), cos(ph)))
def on_head(d, k=1.0): return HC + Vector((d.x * HA, d.y * HB, d.z * HZ)) * k

try:
    random.seed(4)
    old = bpy.data.objects.get("HairSwept")
    if old: bpy.data.objects.remove(old, do_unlink=True)
    hair_mat = next(m for m in bpy.data.materials if m.name == "Haru_Hair")
    bm = bmesh.new(); cl = bm.verts.layers.float_color.new("Col")

    # fringe: seven petals hanging from the front of the crown, all swept toward -y (the character's right) and uneven in length
    SWEEP = -26
    for th, z, w in ((-62, 0.075, 0.03), (-42, 0.082, 0.032), (-22, 0.07, 0.034), (0, 0.05, 0.036), (20, 0.058, 0.034), (40, 0.082, 0.03), (60, 0.09, 0.027)):
        th_tip, tip_z = th + SWEEP * (1 - abs(th) / 100), HC.z + z
        ph_tip = math.degrees(math.acos(max(-1.0, min(1.0, (tip_z - HC.z) / HZ))))
        pts = []
        for i in range(7):
            u = i / 6; d = dirn(24 + (ph_tip - 24) * u, th * 0.75 + (th_tip - th * 0.75) * u)
            pts.append(on_head(d) + d * (0.012 + 0.024 * sin(pi * min(1.0, u * 1.15)) + 0.01 * (1 - u)))
        prof = (0.6, 0.88, 1.0, 1.0, 0.85, 0.5)
        tube(bm, cl, pts, [(w * k, w * k * 0.6) for k in prof] + [0], (pts[0] - HC).normalized())
    for sd in (1, -1):    # temple locks in front of the ears
        a, b = dirn(70, 62 * sd), dirn(92, 80 * sd)
        tube(bm, cl, [on_head(a.lerp(b, i / 6).normalized()) + a.lerp(b, i / 6).normalized() * 0.014 for i in range(7)],
             [(0.03 * k, 0.018 * k) for k in (0.6, 0.88, 1.0, 1.0, 0.85, 0.5)] + [0], a)

    # three long locks from the crown, swept back and down past the nape (3 swept locks, the non-spiky style)
    for th, length, drop in ((150, 0.27, 0.2), (180, 0.31, 0.24), (212, 0.26, 0.19)):
        d = dirn(34, th); root = on_head(d, 0.92)
        back = Vector((-1, 0.18 * sin(radians(th)) * 3, 0)).normalized()
        end = root + back * length * 0.75 + Vector((0, 0, -drop))
        mid = root + back * length * 0.55 + Vector((0, 0, 0.05))
        pts = bezier(root, mid, end, 9)
        prof = (0.7, 1.0, 1.0, 0.92, 0.78, 0.6, 0.38, 0.18)
        tube(bm, cl, pts, [(0.05 * k, 0.034 * k) for k in prof] + [0], d, seg=10)

    me = bpy.data.meshes.new("HairSwept"); bm.to_mesh(me); bm.free()
    me.materials.append(hair_mat); me.shade_smooth() if hasattr(me, "shade_smooth") else None
    bmesh_n = bmesh.new(); bmesh_n.from_mesh(me); bmesh.ops.recalc_face_normals(bmesh_n, faces=bmesh_n.faces); bmesh_n.to_mesh(me); bmesh_n.free()
    o = bpy.data.objects.new("HairSwept", me); bpy.data.collections["Haru"].objects.link(o)
    arm = bpy.data.objects["HaruRig"]
    vg = o.vertex_groups.new(name="head"); vg.add(range(len(me.vertices)), 1.0, 'REPLACE')
    m = o.modifiers.new("Armature", 'ARMATURE'); m.object = arm
    o.parent = arm
    say("HairSwept:", len(me.vertices), "verts,", len(me.polygons), "faces")

    meshes = [x for x in bpy.data.collections["Haru"].objects if x.type == 'MESH']
    for x in bpy.context.view_layer.objects: x.select_set(False)
    for x in meshes + [arm]: x.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "haru.blend"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, "haru.glb"), export_format='GLB', use_selection=True,
                              export_skins=True, export_morph=True, export_yup=True)
    say("exported", os.path.getsize(os.path.join(ROOT, "haru.glb")) // 1024, "KB")
    say("DONE")
except Exception:
    say(traceback.format_exc()); say("FAILED")
log.close()
