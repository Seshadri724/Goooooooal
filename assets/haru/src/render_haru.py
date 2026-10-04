"""Model-sheet renders of haru.blend: turnarounds, head, expressions, then every part on its own (hair, face parts,
head topology, torso, arms, hands, legs, shorts, shoes), each shaded + wireframe, plus a UV dump for the UV panels.
    bash run_blender.sh render_haru.py ../haru.blend
Writes ../renders/*.png and ../renders/uv.json (compose_sheet.py lays them out). Changes the open file but does not save it.
"""
import bpy, bmesh, json, math, os, traceback
from math import radians
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "renders")
LOG = os.path.join(HERE, "render_haru.log")
log = None   # opened by __main__; poses_haru.py imports these helpers and sets its own
def say(*a): print(*a, file=log, flush=True)

# name, azimuth (0 = in front, he faces +X), elevation, distance, look-at height, lens
VIEWS = [("front", 0, 4, 4.0, 0.68, 50), ("side", 90, 4, 4.0, 0.68, 50), ("back", 180, 6, 4.0, 0.68, 50), ("three_quarter", -38, 6, 4.0, 0.68, 50),
         ("head_front", 0, 2, 1.25, 1.17, 70), ("head_side", 90, 2, 1.25, 1.17, 70), ("head_back", 180, 2, 1.25, 1.17, 70), ("head_top", 0, 89, 1.25, 1.17, 70),
         ("face", -12, 2, 0.95, 1.13, 70), ("hair", -140, 28, 1.1, 1.2, 60), ("shoe", -55, 18, 0.75, 0.06, 60), ("shoe_side", 90, 8, 0.7, 0.06, 60)]
WIRE = ["front", "side", "back", "three_quarter", "head_front", "head_side", "head_back", "head_top", "shoe", "shoe_side"]  # sheet: every view also as wireframe
ONLY = os.environ.get("HARU_VIEWS")  # e.g. "front,p_eye"

def studio():
    sc = bpy.context.scene
    col = bpy.data.collections.new("Studio"); sc.collection.children.link(col)
    def light(name, loc, energy, color, size):
        ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
        o = bpy.data.objects.new(name, ld); col.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, 0.8)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    light("Key", (2.4, -1.8, 2.8), 300, (1.0, 0.96, 0.92), 2.0)
    light("Fill", (2.0, 2.4, 1.3), 110, (0.8, 0.88, 1.0), 3.0)
    light("Rim", (-2.2, -0.6, 2.4), 260, (1.0, 0.85, 0.8), 1.5)
    light("Rim2", (-2.0, 1.6, 1.8), 160, (0.8, 0.88, 1.0), 1.5)
    light("Under", (0.6, -0.4, -2.2), 90, (0.9, 0.92, 1.0), 2.5)   # lifts the sole view
    w = sc.world or bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.045, 0.05, 0.065, 1); bg.inputs[1].default_value = 0.8
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); col.objects.link(cam); sc.camera = cam
    for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
        try: sc.render.engine = eng; break
        except TypeError: pass
    sc.render.resolution_x, sc.render.resolution_y = 900, 1200
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'; sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'   # AgX desaturates the kit reds; the sheet is punchy
    try: sc.eevee.use_shadows = True
    except AttributeError: pass
    return cam

def meshes():
    return [o for c in ("Haru", "Parts") if c in bpy.data.collections for o in bpy.data.collections[c].objects if o.type == 'MESH']

ORIG, WIRE_MAT = {}, []
def set_wire(on):
    """Swap every character material for clay grey + dark wireframe lines (the sheet's WIRE panels), or back."""
    if not WIRE_MAT:
        m = bpy.data.materials.new("Wire"); m.use_nodes = True; nt = m.node_tree
        b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs["Roughness"].default_value = 0.7
        w = nt.nodes.new("ShaderNodeWireframe"); w.use_pixel_size = True; w.inputs[0].default_value = 1.4
        mx = nt.nodes.new("ShaderNodeMixRGB"); mx.inputs[1].default_value = (0.22, 0.23, 0.25, 1); mx.inputs[2].default_value = (0.01, 0.01, 0.012, 1)
        nt.links.new(w.outputs[0], mx.inputs[0]); nt.links.new(mx.outputs[0], b.inputs["Base Color"]); WIRE_MAT.append(m)
    for o in meshes():
        for i, sl in enumerate(o.material_slots):
            ORIG.setdefault((o.name, i), sl.material)
            sl.material = WIRE_MAT[0] if on else ORIG[(o.name, i)]

def show(objs):
    keep = set(o.name for o in objs)
    for c in ("Haru", "Parts"):
        if c in bpy.data.collections:
            for o in bpy.data.collections[c].objects: o.hide_render = o.name not in keep

def set_expression(name):
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.data.shape_keys:
            for kb in o.data.shape_keys.key_blocks[1:]: kb.value = 1.0 if kb.name == name else 0.0

def aim(arm, bone, direction):
    """Rotate a pose bone (armature at the origin) so it points along `direction`, keeping its head."""
    bpy.context.view_layer.update()
    pb = arm.pose.bones[bone]; m = pb.matrix.copy()
    cur = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
    q = cur.rotation_difference(Vector(direction).normalized())
    pb.matrix = Matrix.Translation(m.translation) @ (q.to_matrix() @ m.to_3x3()).to_4x4()

def pose_wave(arm):
    for b, d in (("upper_arm.L", (0.05, 0.92, 0.38)), ("forearm.L", (0.12, 0.3, 0.95)), ("hand.L", (0.1, 0.15, 1.0)),
                 ("upper_arm.R", (0.06, -0.22, -0.97)), ("forearm.R", (0.2, -0.15, -0.97)),
                 ("head", (-0.02, 0.12, 1.0)), ("thigh.R", (0.02, -0.12, -0.99)), ("shin.R", (0.0, -0.1, -0.99))):
        aim(arm, b, d)

# expression close-ups and the posed shot (rig must exist: run rig_haru.py first)
VIEWS += [("expr_" + e, 0, 2, 1.2, 1.17, 70) for e in ("Neutral", "Happy", "Surprised", "Angry", "Sad", "Wink")]
VIEWS += [("pose_wave", -30, 6, 4.0, 0.7, 50)]

def shots():
    for v in VIEWS: yield v + (False,)
    for v in VIEWS:
        if v[0] in WIRE: yield ("wire_" + v[0],) + v[1:] + (True,)

# ------------------------------------------------------------------ parts
def cut(src, name, keep=None, mats=None, side=0, island=None, islands=None):
    """Copy of src reduced to one part: keep(v, dominant_bone) per vertex, faces of the named materials, his left (+1) or
    right (-1) half, the connected island holding island(bm)'s vertex, and/or every island whose centroid passes islands(c).
    Lives in the Parts collection."""
    o = src.copy(); o.data = src.data.copy(); o.name = name; bpy.data.collections["Parts"].objects.link(o)
    if o.data.shape_keys: o.shape_key_clear()
    bm = bmesh.new(); bm.from_mesh(o.data); dl = bm.verts.layers.deform.active
    gname = {g.index: g.name for g in src.vertex_groups}
    def dom(v):
        d = v[dl] if dl else None
        return gname.get(max(d.items(), key=lambda kv: kv[1])[0]) if d and len(d) else None
    if keep or side:
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if (keep and not keep(v, dom(v))) or (side and v.co.y * side < 0)], context='VERTS')
    if mats is not None:
        idx = {i for i, m in enumerate(o.data.materials) if m and m.name in mats}
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index not in idx], context='FACES')
    if island:
        seen, stack = set(), [island(bm)]
        while stack:
            v = stack.pop()
            if v in seen: continue
            seen.add(v); stack.extend(e.other_vert(v) for e in v.link_edges)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v not in seen], context='VERTS')
    if islands:
        left, dead = set(bm.verts), []
        while left:
            seen, stack = set(), [left.pop()]
            while stack:
                v = stack.pop()
                if v in seen: continue
                seen.add(v); stack.extend(e.other_vert(v) for e in v.link_edges)
            left -= seen
            if not islands(sum((v.co for v in seen), Vector()) / len(seen)): dead += seen
        bmesh.ops.delete(bm, geom=dead, context='VERTS')
    bm.to_mesh(o.data); bm.free(); o.hide_render = True
    return o

def bb(objs):
    pts = [o.matrix_world @ v.co for o in objs if o.type == 'MESH' for v in o.data.vertices]
    return Vector([min(p[i] for p in pts) for i in range(3)]), Vector([max(p[i] for p in pts) for i in range(3)])

def ring(name, pts, hexc):
    """A glowing polyline loop (head topology overlay). Emission so its colour reads exactly over the wireframe."""
    if len(pts) < 3: say('ring missed the surface:', name); return None
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0022; cu.bevel_resolution = 2
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1); sp.use_cyclic_u = True
    for q, p in zip(sp.points, pts): q.co = (*p, 1)
    m = bpy.data.materials.new("Ring_" + name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission"); h = hexc.lstrip('#')
    em.inputs[0].default_value = tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1,); em.inputs[1].default_value = 1.6
    nt.links.new(em.outputs[0], next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL').inputs[0]); cu.materials.append(m)
    o = bpy.data.objects.new(name, cu); bpy.data.collections["Parts"].objects.link(o); o.hide_render = True
    return o

def projected(target, c, r1, r2, axis=0, sign=1, n=56):
    """Ellipse round c (radius r1 along the first other axis, r2 along Z) dropped onto target by rays from the `sign` side of `axis`."""
    u = 1 if axis == 0 else 0; d = Vector((0, 0, 0)); d[axis] = -sign; pts = []
    for i in range(n):
        t = 2 * math.pi * i / n; p = Vector(c)
        p[u] += r1 * math.cos(t); p[2] += r2 * math.sin(t); p[axis] += 2 * sign
        ok, loc, nrm, _ = target.ray_cast(p, d)
        if ok: pts.append(loc + nrm * 0.003)
    return pts

def build_parts():
    O = {o.name: o for o in bpy.data.collections["Haru"].objects}
    bpy.context.scene.collection.children.link(bpy.data.collections.new("Parts"))
    ARM = lambda s: {f"{b}.{s}" for b in ("shoulder", "upper_arm", "forearm", "hand")}
    LEG = {f"{b}.{s}" for b in ("thigh", "shin", "foot") for s in "LR"}
    P = {}
    P["strand"] = cut(O["Hair"], "Strand", island=lambda bm: max(bm.verts, key=lambda v: v.co.z))
    P["eye"] = cut(O["Eyes"], "EyeL", side=1)
    P["brow"] = cut(O["Face"], "BrowL", mats={"Haru_Brow"}, side=1)
    P["nose"] = cut(O["Face"], "Nose", mats={"Haru_Skin"})
    P["mouth"] = cut(O["Face"], "MouthLine", mats={"Haru_Mouth"})
    arm = bpy.data.objects["HaruRig"].data.bones
    for s, sd in (("L", 1), ("R", -1)):   # skin of the arm + the sleeve/cuff pieces of the shirt on that side + the fingers
        P["arm" + s] = [cut(O["Body"], "Arm" + s, keep=lambda v, g, s=s: g in ARM(s) and g != f"shoulder.{s}"),
                        cut(O["Shirt"], "Sleeve" + s, islands=lambda c, sd=sd: c.y * sd > 0.1), O["Hand_" + s]]
    P["hand"] = [O["Hand_L"]]   # palm + fingers
    P["legs"] = [cut(O["Body"], "Legs", keep=lambda v, g: g in LEG), O["Socks"]]

    # head topology: feature loops dropped onto the head mesh (face ones from the front, ears from the side)
    head = O["Head"]; H0, H1 = bb([head])
    side_bb = lambda src, nm, s, mats=None: bb([cut(src, f"_{nm}{s}", side=s, mats=mats)])
    rings = []
    for s in (1, -1):
        a, b = side_bb(O["Eyes"], "eye", s)
        rings.append(ring(f"EyeLoop{s}", projected(head, (a + b) / 2, (b.y - a.y) / 2 * 1.25, (b.z - a.z) / 2 * 1.25), '#8f8cf2'))
        a, b = side_bb(O["Face"], "brow", s, {"Haru_Brow"})
        rings.append(ring(f"BrowLoop{s}", projected(head, (a + b) / 2, (b.y - a.y) / 2 * 1.2, max(0.012, b.z - a.z)), '#3cc060'))
        a, b = side_bb(O["Ears"], "ear", s)
        rings.append(ring(f"EarLoop{s}", projected(O["Ears"], (a + b) / 2, (b.x - a.x) / 2 * 0.7, (b.z - a.z) / 2 * 0.72, axis=1, sign=s), '#f08a30'))
    a, b = bb([P["nose"]]); rings.append(ring("NoseLoop", projected(head, (a + b) / 2, (b.y - a.y), (b.z - a.z)), '#f0a830'))
    a, b = bb([P["mouth"]]); rings.append(ring("MouthLoop", projected(head, (a + b) / 2, (b.y - a.y) / 2 * 1.4, max(0.016, (b.z - a.z) * 1.5)), '#e0404a'))
    top = side_bb(O["Face"], "browtop", 1, {"Haru_Brow"})[1].z + 0.02
    rings.append(ring("FaceContour", projected(head, Vector((0, 0, (top + H0.z) / 2)), (H1.y - H0.y) / 2 * 0.86, (top - H0.z) / 2 * 1.02), '#2fa8e8'))
    hz, pts = top + 0.035, []
    for i in range(72):  # hair base: a band round the skull where the hair cap starts
        t = 2 * math.pi * i / 72; d = Vector((math.cos(t), math.sin(t), 0))
        ok, loc, nrm, _ = head.ray_cast(Vector((0, 0, hz)) + d * 2, -d)
        if ok: pts.append(loc + nrm * 0.003)
    rings.append(ring("HairBase", pts, '#f0d040'))
    rings = [r for r in rings if r]
    head_parts = [head, O["Ears"], O["Eyes"], O["Face"]]
    hair = [O["Hair"], O["HairCap"]]

    # (name, visible, frame-to (None = visible), azimuth, elevation, pad); each is rendered shaded and as "<name>_wire"
    S = [("p_hair_" + v, hair, None, az, el, 1.08) for v, az, el in (("front", 0, 0), ("side", 90, 0), ("back", 180, 0), ("top", 0, 90))]
    S += [("p_strand", [P["strand"]], None, -70, 12, 1.15), ("p_eye", [P["eye"]], None, 0, 0, 1.15), ("p_brow", [P["brow"]], None, 0, 4, 1.25),
          ("p_nose", [head, O["Face"]], [P["nose"]], -30, 4, 4.0), ("p_mouth", [head, O["Face"]], [P["mouth"]], 0, 0, 2.6),
          ("p_torso", [O["Shirt"]], None, 0, 0, 1.08), ("p_armL", P["armL"], None, 0, 0, 1.08), ("p_armR", P["armR"], None, 0, 0, 1.08),
          ("p_hand_palm", P["hand"], None, -90, -19, 1.12), ("p_hand_side", P["hand"], None, 0, 0, 1.12),
          ("p_legs_front", P["legs"], None, 0, 0, 1.06), ("p_legs_back", P["legs"], None, 180, 0, 1.06),
          ("p_shorts_front", [O["Shorts"]], None, 0, 0, 1.08), ("p_shorts_back", [O["Shorts"]], None, 180, 0, 1.08),
          ("p_shoe_front", [O["Shoe_L"]], None, 0, 4, 1.1), ("p_shoe_side", [O["Shoe_L"]], None, 90, 4, 1.1), ("p_shoe_sole", [O["Shoe_L"]], None, 0, -90, 1.1)]
    out = [(n + suf, vis, fr, az, el, pad, suf == "_wire") for n, vis, fr, az, el, pad in S for suf in ("", "_wire")]
    out.append(("p_topology", head_parts + rings, head_parts, 0, 0, 1.12, True))   # wire head + glowing loops
    return out

def frame_ortho(cam, objs, az, el, pad):
    """Orthographic camera looking at objs from azimuth/elevation, scaled so they fill a square frame."""
    a, e = radians(az), radians(el); z = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    up = Vector((0, 0, 1)) if abs(el) < 80 else Vector((1, 0, 0))   # top / sole views: his front at the top of the frame
    x = up.cross(z).normalized(); y = z.cross(x)
    lo, hi = bb(objs); corners = [Vector((lo.x if i & 1 else hi.x, lo.y if i & 2 else hi.y, lo.z if i & 4 else hi.z)) for i in range(8)]
    px, py = [c.dot(x) for c in corners], [c.dot(y) for c in corners]
    cz = max(c.dot(z) for c in corners)
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(max(px) - min(px), max(py) - min(py)) * pad
    cam.data.clip_start, cam.data.clip_end = 0.01, 50
    R = Matrix((x, y, z)).transposed()
    cam.matrix_world = Matrix.Translation(x * (min(px) + max(px)) / 2 + y * (min(py) + max(py)) / 2 + z * (cz + 5)) @ R.to_4x4()

def lin2srgb(c): return round(255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055))
def dump_uv(path):
    """Per object: every UV face polygon + its colour (material base colour, or the averaged hair vertex colour)."""
    O = {o.name: o for o in bpy.data.collections["Haru"].objects}; out = {}
    for n in ("Head", "Hair", "Shirt", "Shorts", "Shoe_L", "Eyes", "Body"):
        me = O[n].data; uv = me.uv_layers.active
        if not uv: continue
        ca = me.color_attributes.get("Col"); cols = []
        for m in me.materials:
            b = next((k for k in m.node_tree.nodes if k.type == 'BSDF_PRINCIPLED'), None) if m and m.use_nodes else None
            cols.append(None if b is None or b.inputs["Base Color"].is_linked else [lin2srgb(c) for c in b.inputs["Base Color"].default_value[:3]])
        faces = []
        for p in me.polygons:
            rgb = cols[p.material_index] if p.material_index < len(cols) else None
            if rgb is None and ca:
                src = [ca.data[li].color for li in p.loop_indices] if ca.domain == 'CORNER' else [ca.data[me.loops[li].vertex_index].color for li in p.loop_indices]
                rgb = [lin2srgb(sum(c[i] for c in src) / len(src)) for i in range(3)]
            faces.append([[[round(uv.data[li].uv[0], 4), round(uv.data[li].uv[1], 4)] for li in p.loop_indices], rgb or [200, 200, 200]])
        out[n] = faces
    json.dump(out, open(path, "w"))

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    cam = studio(); sc = bpy.context.scene
    arm = bpy.data.objects.get("HaruRig")
    allv = list(bpy.data.collections["Haru"].objects)
    for name, az, el, dist, tz, lens, wire in shots():
        if ONLY and name not in ONLY.split(","): continue
        if name.startswith(("expr_", "pose_")) and not arm: continue
        show(allv); set_wire(wire); cam.data.type = 'PERSP'; cam.data.clip_start, cam.data.clip_end = 0.1, 100
        set_expression(name[5:] if name.startswith("expr_") else ("Happy" if name == "pose_wave" else None))
        if arm:
            for pb in arm.pose.bones: pb.matrix_basis.identity()
            if name == "pose_wave": pose_wave(arm)
        a, e = radians(az), radians(el)
        pos = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist + Vector((0, 0, tz))
        cam.location = pos; cam.data.lens = lens
        cam.rotation_euler = (Vector((0, 0, tz)) - pos).to_track_quat('-Z', 'Y' if el < 80 else 'X').to_euler()
        sc.render.resolution_x, sc.render.resolution_y = (900, 1200) if dist > 2 else (900, 900)
        sc.render.filepath = os.path.join(OUTDIR, name + ".png")
        bpy.ops.render.render(write_still=True)
        say("rendered", name)
    # every part on its own: rest pose, neutral face, orthographic, square
    set_expression(None)
    if arm:
        for pb in arm.pose.bones: pb.matrix_basis.identity()
    bpy.context.view_layer.update(); set_wire(False)
    for name, vis, fr, az, el, pad, wire in build_parts():
        if ONLY and name not in ONLY.split(","): continue
        show(vis); set_wire(wire); bpy.context.view_layer.update()
        frame_ortho(cam, fr or [o for o in vis if o.type == 'MESH'], az, el, pad)
        sc.render.resolution_x = sc.render.resolution_y = 800
        sc.render.filepath = os.path.join(OUTDIR, name + ".png"); bpy.ops.render.render(write_still=True); say("rendered", name)
    set_wire(False); dump_uv(os.path.join(OUTDIR, "uv.json")); say("uv.json written")

if __name__ == "__main__":
    log = open(LOG, "w")
    try: main(); say("DONE")
    except Exception: say(traceback.format_exc()); say("FAILED")
    log.close()
