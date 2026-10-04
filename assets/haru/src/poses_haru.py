"""Shooting pose sheet: Haru posed on his rig in five shots, each rendered as a hero shot with the ball and impact FX,
wireframe front/side/back, and three close-ups. Run headless (after rig_haru.py):
    bash run_blender.sh poses_haru.py ../haru.blend
Writes ../renders/pose_*.png (compose_sheet.py lays them out as poses.png). Does not save the .blend.
HARU_POSES=power,volley renders only those poses.
"""
import bpy, bmesh, math, os, random, sys, traceback
from math import radians
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render_haru as RH
OUT = RH.OUTDIR
RH.log = log = open(os.path.join(HERE, "poses_haru.log"), "w")
say = RH.say
BALL_R = 0.12
HOT = "#ff7a2e"      # Haru is a flame striker: impact energy is white-hot fading to orange

# Directions are world space (he faces +X, +Y is his left, Z up); bones are aimed parent-first. He kicks with the RIGHT leg.
# root: (lift, roll toward his left, lean back) · twist: hips/chest yaw (radians, + = toward his left)
# ball: offset from the right foot's tip, or ("air", x, y, z) · kick: where the ball is going · cam: hero (azimuth, elevation)
# fx: flash size, speed lines, shock rings, dust ("plant" / "contact" / None), trail length, swing arc (radians)
# details: (name, label, framing bones/'ball', azimuth, elevation)
POSES = [
    dict(id="power", title="POWER SHOT", expr="Angry", root=(0.0, 0.0, -0.24), twist={"hips": -0.45, "chest": 0.35}, cam=(-56, 0),
         dirs={"spine": (-0.25, 0, 0.97), "chest": (-0.35, 0.08, 0.93), "neck": (0.05, 0, 1), "head": (0.5, -0.12, 0.86),
               "thigh.L": (0.22, 0.08, -0.97), "shin.L": (-0.55, 0.03, -0.83), "foot.L": (1, 0.1, -0.2),
               "thigh.R": (0.86, -0.08, -0.45), "shin.R": (0.99, -0.04, -0.08), "foot.R": (0.75, 0, -0.62),
               "upper_arm.L": (0.5, 0.82, 0.1), "forearm.L": (0.9, 0.15, 0.4), "upper_arm.R": (-0.6, -0.75, -0.2), "forearm.R": (-0.15, -0.4, 0.9)},
         ball=(0.07, -0.01, 0.02), kick=(1, -0.1, 0.15),
         fx=dict(flash=1.0, lines=16, rings=2, dust="plant", trail=0.9, swing=1.7),
         details=[("contact", "FOOT CONTACT", ["foot.R", "ball"], -60, 6), ("ext", "LEG EXTENSION", ["thigh.R", "foot.R"], -90, 0),
                  ("twist", "BODY TWIST", ["hips", "chest", "upper_arm.L", "upper_arm.R"], -25, 10)]),
    dict(id="instep", title="INSTEP KICK", expr="Neutral", root=(0.0, 0.0, 0.12), twist={"hips": -0.3, "chest": 0.15}, cam=(-58, 7),
         dirs={"spine": (0.2, 0, 0.98), "chest": (0.25, 0.04, 0.97), "head": (0.6, -0.08, 0.8),
               "thigh.L": (0.18, 0.1, -0.98), "shin.L": (-0.4, 0.05, -0.91), "foot.L": (1, 0.05, -0.12),
               "thigh.R": (0.55, -0.05, -0.83), "shin.R": (0.88, -0.02, -0.47), "foot.R": (0.5, 0, -0.87),
               "upper_arm.L": (0.2, 0.95, 0.05), "forearm.L": (0.7, 0.55, 0.45), "upper_arm.R": (-0.45, -0.85, -0.25), "forearm.R": (-0.55, -0.25, 0.8)},
         ball=(0.08, 0, 0.0), kick=(1, -0.12, 0.06),
         fx=dict(flash=0.6, lines=10, rings=1, dust="contact", trail=0.7, swing=1.4),
         details=[("contact", "INSTEP CONTACT", ["foot.R", "ball"], -45, 8), ("angle", "FOOT ANGLE", ["shin.R", "foot.R"], -90, 4),
                  ("follow", "FOLLOW THROUGH", ["thigh.R", "foot.R", "foot.L"], 150, 6)]),
    dict(id="chip", title="CHIP SHOT", expr="Surprised", root=(0.0, 0.0, -0.22), twist={"hips": -0.15}, cam=(-68, -4),
         dirs={"spine": (-0.2, 0, 0.98), "chest": (-0.25, 0.03, 0.97), "head": (0.3, -0.1, 0.95),
               "thigh.L": (0.05, 0.06, -1), "shin.L": (-0.32, 0.03, -0.95), "foot.L": (1, 0.05, -0.1),
               "thigh.R": (0.8, -0.05, 0.25), "shin.R": (0.3, 0, -0.95), "foot.R": (0.75, 0, 0.62),
               "upper_arm.L": (0.55, 0.7, 0.45), "forearm.L": (0.9, 0.05, 0.42), "upper_arm.R": (-0.4, -0.85, -0.35), "forearm.R": (-0.45, -0.35, 0.82)},
         ball=("air", 0.55, -0.14, 1.3), kick=(0.35, -0.1, 0.94),
         fx=dict(flash=0.45, lines=7, rings=0, dust="plant", trail=1.0, swing=1.1),
         details=[("toe", "TOE CONTACT", ["foot.R"], -55, -5), ("lift", "LIFT MOTION", ["thigh.R", "shin.R", "foot.R"], -90, 0),
                  ("balance", "BODY BALANCE", ["hips", "foot.L", "foot.R", "chest"], -20, 4)]),
    dict(id="volley", title="VOLLEY SHOT", expr="Angry", root=(0.34, -0.4, -0.18), twist={"hips": -0.35, "chest": 0.1}, cam=(-52, 3),
         dirs={"spine": (0, 0.33, 0.94), "chest": (-0.12, 0.38, 0.92), "head": (0.5, 0.0, 0.87),
               "thigh.L": (0.4, 0.15, -0.9), "shin.L": (-0.78, 0.05, -0.62), "foot.L": (0.25, 0, -0.97),
               "thigh.R": (0.9, -0.15, 0.4), "shin.R": (0.95, -0.08, 0.3), "foot.R": (0.85, 0, 0.5),
               "upper_arm.L": (0.05, 0.88, 0.47), "forearm.L": (0.55, 0.45, 0.7), "upper_arm.R": (-0.25, -0.95, 0.15), "forearm.R": (0.25, -0.55, 0.8)},
         ball=(0.08, 0, 0.05), air=True, kick=(1, -0.15, 0.25),
         fx=dict(flash=1.0, lines=16, rings=2, dust=None, trail=0.8, swing=1.9),
         details=[("air", "AIR KICK", ["foot.R", "ball"], -50, 10), ("angle", "FOOT ANGLE", ["foot.R"], -90, -10),
                  ("aerial", "AERIAL BALANCE", ["chest", "upper_arm.L", "upper_arm.R", "head"], -15, 6)]),
    dict(id="finish", title="FINISHING SHOT", expr="Happy", root=(0.0, 0.0, 0.26), twist={"hips": 0.3, "chest": -0.2}, cam=(-58, 9),
         dirs={"spine": (0.32, 0, 0.95), "chest": (0.38, -0.03, 0.92), "head": (0.6, -0.08, 0.8),
               "thigh.L": (0.25, 0.1, -0.96), "shin.L": (-0.45, 0.05, -0.89), "foot.L": (1, 0.05, -0.15),
               "thigh.R": (0.45, 0.12, -0.88), "shin.R": (0.82, 0.2, -0.53), "foot.R": (0.55, 0.15, -0.82),
               "upper_arm.L": (0.25, 0.95, -0.1), "forearm.L": (0.75, 0.45, 0.48), "upper_arm.R": (-0.2, -0.95, 0.1), "forearm.R": (0.3, -0.55, 0.78)},
         ball=(0.09, 0.02, -0.01), kick=(1, -0.08, 0.02),
         fx=dict(flash=0.75, lines=12, rings=1, dust="contact", trail=0.7, swing=1.3),
         details=[("contact", "FOOT CONTACT", ["foot.R", "ball"], -40, 6), ("follow", "FOLLOW THROUGH", ["thigh.R", "foot.R", "foot.L"], -110, 4),
                  ("lean", "BODY LEAN", ["head", "chest", "hips"], -90, 2)]),
]

# ------------------------------------------------------------------ ball
def ball():
    """Football: icosphere whose faces near the 12 icosahedron vertices are black (round pentagon patches)."""
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=4, radius=BALL_R)
    t = (1 + 5 ** 0.5) / 2
    poles = [Vector(v).normalized() for v in [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]]
    for f in bm.faces:
        c = f.calc_center_median().normalized(); f.material_index = 1 if max(c.dot(p) for p in poles) > 0.94 else 0
        f.smooth = True
    me = bpy.data.meshes.new("Ball"); bm.to_mesh(me); bm.free()
    for nm, col, r in (("BallWhite", (0.9, 0.9, 0.92, 1), 0.35), ("BallBlack", (0.015, 0.015, 0.02, 1), 0.4)):
        m = bpy.data.materials.new(nm); m.use_nodes = True; b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = r; me.materials.append(m)
    col = bpy.data.collections.new("Props"); bpy.context.scene.collection.children.link(col)
    o = bpy.data.objects.new("Ball", me); col.objects.link(o)
    return o

# ------------------------------------------------------------------ impact FX
def srgb(h): h = h.lstrip('#'); return tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1,)

def blended(m):
    try: m.surface_render_method = 'BLENDED'
    except AttributeError: m.blend_method = 'BLEND'

FXM = {}
def fx_mat(hexc, strength, alpha):
    """Unlit glow: emission over transparency; the vertex colour's alpha ("Col") fades it further along a ribbon."""
    key = (hexc, strength, alpha)
    if key in FXM: return FXM[key]
    m = bpy.data.materials.new(f"FX_{hexc}_{strength}_{alpha}"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em, tr, mx, out = (nt.nodes.new(t) for t in ("ShaderNodeEmission", "ShaderNodeBsdfTransparent", "ShaderNodeMixShader", "ShaderNodeOutputMaterial"))
    va, mul = nt.nodes.new("ShaderNodeVertexColor"), nt.nodes.new("ShaderNodeMath"); va.layer_name = "Col"; mul.operation = 'MULTIPLY'
    em.inputs[0].default_value = srgb(hexc); em.inputs[1].default_value = strength; mul.inputs[1].default_value = alpha
    nt.links.new(va.outputs["Alpha"], mul.inputs[0]); nt.links.new(mul.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    blended(m); FXM[key] = m
    return m

def lit_mat(name, hexc, alpha, rough=1.0):
    if name in FXM: return FXM[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs["Base Color"].default_value = srgb(hexc); b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha
    blended(m); FXM[name] = m
    return m

def shadow_mat():
    if "Shadow" in FXM: return FXM["Shadow"]
    m = bpy.data.materials.new("FX_Shadow"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc, gr, mul, tr, em, mx, out = (nt.nodes.new(t) for t in ("ShaderNodeTexCoord", "ShaderNodeTexGradient", "ShaderNodeMath", "ShaderNodeBsdfTransparent",
                                                              "ShaderNodeEmission", "ShaderNodeMixShader", "ShaderNodeOutputMaterial"))
    gr.gradient_type = 'SPHERICAL'; mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 0.65; em.inputs[0].default_value = (0, 0, 0, 1)
    nt.links.new(tc.outputs["Object"], gr.inputs[0]); nt.links.new(gr.outputs[1], mul.inputs[0]); nt.links.new(mul.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    blended(m); FXM["Shadow"] = m
    return m

def fx_obj(name, verts, faces, mat, alphas=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], faces)
    ca = me.color_attributes.new("Col", 'FLOAT_COLOR', 'POINT')
    for i, a in enumerate(alphas or [1.0] * len(verts)): ca.data[i].color = (1, 1, 1, a)
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); bpy.data.collections["FX"].objects.link(o); o.visible_shadow = False
    return o

def ribbon(name, pts, widths, alphas, view, mat):
    """Camera-facing strip along a polyline (trails, speed lines): width runs across both the path and the view."""
    verts, faces, al = [], [], []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        s = t.cross((view - p).normalized()).normalized() * widths[i]
        verts += [p + s, p - s]; al += [alphas[i]] * 2
        if i: faces.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
    return fx_obj(name, verts, faces, mat, al)

def facing(view, c):
    """Orthonormal (right, up) for a flat shape at c facing the camera."""
    n = (view - c).normalized(); r = n.cross(Vector((0, 0, 1))).normalized() if abs(n.z) < 0.98 else Vector((1, 0, 0)); return r, r.cross(n)

def star(name, c, view, r_out, r_in, spikes, mat, rnd):
    r, u = facing(view, c); verts = [c]
    for i in range(spikes * 2):
        a = math.pi * i / spikes + rnd.uniform(-0.08, 0.08); rad = r_out * rnd.uniform(0.6, 1.15) if i % 2 == 0 else r_in
        verts.append(c + (r * math.cos(a) + u * math.sin(a)) * rad)
    n = spikes * 2
    return fx_obj(name, verts, [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)], mat, [1.0] + [0.35] * n)

def disk(name, c, normal, r_in, r_out, mat, seg=48, a_in=1.0, a_out=1.0):
    n = Vector(normal).normalized(); r = n.cross(Vector((0, 0, 1))).normalized() if abs(n.z) < 0.98 else Vector((1, 0, 0)); u = n.cross(r)
    verts, faces, al = [], [], []
    for i in range(seg):
        a = 2 * math.pi * i / seg; d = r * math.cos(a) + u * math.sin(a)
        verts += [c + d * r_in, c + d * r_out]; al += [a_in, a_out]
        j = (i + 1) % seg; faces.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    return fx_obj(name, verts, faces, mat, al)

def sphere(name, c, r, mat, sub=2):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    for v in bm.verts: v.co += c
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ca = me.color_attributes.new("Col", 'FLOAT_COLOR', 'POINT')
    for d in ca.data: d.color = (1, 1, 1, 1)
    me.materials.append(mat); me.shade_smooth()
    o = bpy.data.objects.new(name, me); bpy.data.collections["FX"].objects.link(o); o.visible_shadow = False
    return o

def clear_fx():
    for o in list(bpy.data.collections["FX"].objects): bpy.data.objects.remove(o, do_unlink=True)

def effects(P, arm, b, view):
    """Impact FX for this pose, built to face `view` (the camera position). Seeded per pose so every angle matches."""
    clear_fx(); fx = P["fx"]; rnd = random.Random(P["id"]); k = Vector(P["kick"]).normalized()
    pose = arm.pose.bones; W = arm.matrix_world
    tip, heel = W @ pose["foot.R"].tail, W @ pose["foot.R"].head
    air_ball = P["ball"][0] == "air"
    contact = tip if air_ball else b.location + (tip - b.location).normalized() * BALL_R * 0.95
    s = fx["flash"]
    # flash: white-hot core inside orange glow shells, an anime impact star behind the contact, plus a hot inner star
    behind = contact - (view - contact).normalized() * 0.06
    sphere("FlashCore", contact, 0.035 * s, fx_mat("#ffffff", 4.0, 1.0))
    sphere("FlashMid", contact, 0.09 * s, fx_mat("#ffd9a0", 2.0, 0.35))
    sphere("FlashOuter", contact, 0.18 * s, fx_mat(HOT, 1.5, 0.12))
    star("StarHot", behind, view, 0.34 * s, 0.07 * s, 13, fx_mat(HOT, 2.2, 0.75), rnd)
    star("StarWhite", behind + (view - behind).normalized() * 0.01, view, 0.2 * s, 0.05 * s, 11, fx_mat("#fff6e0", 3.0, 0.95), rnd)
    # speed lines radiating from the contact, thrown mostly forward with the ball
    for i in range(fx["lines"]):
        d = (k * 0.8 + Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.6, 1)))).normalized()
        r0, ln = rnd.uniform(0.1, 0.16) * max(s, 0.6), rnd.uniform(0.16, 0.38) * max(s, 0.6)
        pts = [contact + d * (r0 + ln * u) for u in (0, 0.5, 1)]
        ribbon(f"Line{i}", pts, [0.012, 0.007, 0.0], [1, 0.8, 0.2], view, fx_mat("#ffffff" if i % 3 else HOT, 2.5, 0.9))
    # shock rings travelling with the ball
    for i in range(fx["rings"]):
        disk(f"Ring{i}", contact + k * (0.06 + 0.14 * i), k, (0.11 + 0.08 * i) * s, (0.125 + 0.088 * i) * s, fx_mat("#fff1d6", 2.0, 0.55 - 0.2 * i), a_in=0.3, a_out=1.0)
    # ball trail: a fat glow ribbon + two thin streaks; a chip's trail arcs up from the toe to the ball
    if air_ball:
        path = [contact.lerp(b.location, u) + Vector((0.12, 0, 0)) * math.sin(math.pi * u) for u in [i / 13 for i in range(14)]]
    else:
        path = [b.location - k * fx["trail"] * u + Vector((0, 0, 0.04)) * math.sin(u * 3) for u in [1 - i / 13 for i in range(14)]]
    n = len(path); prog = [i / (n - 1) for i in range(n)]   # 0 at the tail, 1 at the ball
    ribbon("Trail", path, [BALL_R * 0.85 * p for p in prog], [0.75 * p for p in prog], view, fx_mat("#ffffff", 1.6, 0.6))
    for j, off in enumerate((-0.07, 0.07)):
        r_, u_ = facing(view, b.location); o = u_ * off
        ribbon(f"Streak{j}", [p + o for p in path], [0.012 * p for p in prog], [0.9 * p for p in prog], view, fx_mat(HOT, 2.0, 0.8))
    # swing arc: the kicking foot's path round the hip, fading toward where the swing began
    hip = W @ pose["thigh.R"].head; v = tip - hip; verts, faces, al = [], [], []
    for i in range(16):
        u = i / 15; q = Quaternion(Vector((0, 1, 0)), fx["swing"] * (1 - u)); w = q @ v
        verts += [hip + w * 0.62, hip + w * 1.04]; al += [u * u * 0.8, u * u]
        if i: faces.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
    fx_obj("Swing", verts, faces, fx_mat("#fff4e8", 1.6, 0.55), al)
    # dust + debris: kicked up behind the plant foot, or sprayed off the turf at a low contact
    if fx["dust"]:
        plant = W @ pose["foot.L"].tail
        src, d0, nd = (plant + Vector((-0.06, 0, 0.02)), Vector((-0.8, 0.15, 0.55)), 22) if fx["dust"] == "plant" else (Vector((contact.x, contact.y, 0.03)), Vector((0.7, -0.1, 0.5)), 16)
        for i in range(nd):
            dd = (d0.normalized() + Vector((rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), rnd.uniform(-0.2, 0.4)))).normalized(); t = rnd.uniform(0.02, 0.42)
            sphere(f"Dust{i}", src + dd * t, 0.018 + t * 0.12 * rnd.uniform(0.6, 1.1), lit_mat("FX_Dust", "#d8c3a5", 0.42), sub=2)
        for i in range(18):
            dd = (d0.normalized() + Vector((rnd.uniform(-0.7, 0.7), rnd.uniform(-0.7, 0.7), rnd.uniform(0, 0.6)))).normalized()
            sphere(f"Bit{i}", src + dd * rnd.uniform(0.05, 0.5), rnd.uniform(0.005, 0.011), lit_mat("FX_Turf" if i % 2 else "FX_Dirt", "#4f9a3a" if i % 2 else "#6b4a2c", 1.0), sub=1)
    # contact shadow on the (invisible) turf; airborne = smaller and fainter, it reads as height
    feet = [(W @ pose[f].tail) for f in ("foot.L", "foot.R")]
    c = Vector(((feet[0].x + feet[1].x) / 2, (feet[0].y + feet[1].y) / 2, 0.002))
    sh = disk("Shadow", Vector(), (0, 0, 1), 0.0, 1.0, shadow_mat(), seg=40)   # unit disk, placed + squashed by the object
    sh.location = c; sh.scale = (0.42, 0.3, 1) if not P.get("air") else (0.3, 0.22, 1)
    if not air_ball and not P.get("air"):
        bs = disk("BallShadow", Vector(), (0, 0, 1), 0.0, 1.0, shadow_mat(), seg=32)
        bs.location = (b.location.x, b.location.y, 0.002); bs.scale = (BALL_R * 1.3, BALL_R * 1.1, 1)

# ------------------------------------------------------------------ posing
def twist(arm, bone, ang):
    bpy.context.view_layer.update()
    pb = arm.pose.bones[bone]; m = pb.matrix.copy(); q = Quaternion(Vector((0, 0, 1)), ang)
    pb.matrix = Matrix.Translation(m.translation) @ (q.to_matrix() @ m.to_3x3()).to_4x4()

ORDER = ["spine", "chest", "neck", "head", "thigh.L", "shin.L", "foot.L", "thigh.R", "shin.R", "foot.R",
         "upper_arm.L", "forearm.L", "hand.L", "upper_arm.R", "forearm.R", "hand.R"]

def pose(arm, P):
    for pb in arm.pose.bones: pb.matrix_basis.identity()
    bpy.context.view_layer.update()
    lift, roll, lean = P["root"]; piv = arm.pose.bones["hips"].matrix.translation.copy(); root = arm.pose.bones["root"]
    root.matrix = Matrix.Translation(piv) @ Matrix.Rotation(roll, 4, 'X') @ Matrix.Rotation(lean, 4, 'Y') @ Matrix.Translation(-piv) @ root.matrix
    for b, a in P["twist"].items(): twist(arm, b, a)
    for b in ORDER:
        if b in P["dirs"]: RH.aim(arm, b, P["dirs"][b])
    for s in "LR":   # hands carry on from the forearm unless posed
        if "hand." + s not in P["dirs"]:
            bpy.context.view_layer.update(); fa = arm.pose.bones["forearm." + s]; RH.aim(arm, "hand." + s, fa.tail - fa.head)
    bpy.context.view_layer.update()
    # ground him: lowest shoe point on the turf (or `lift` above it when airborne)
    dg = bpy.context.evaluated_depsgraph_get()
    low = min((o.matrix_world @ v.co).z for n in ("Shoe_L", "Shoe_R") for o in [bpy.data.objects[n].evaluated_get(dg)] for v in o.data.vertices)
    root.matrix = Matrix.Translation((0, 0, (lift if P.get("air") else 0.0) - low)) @ root.matrix
    bpy.context.view_layer.update()

# ------------------------------------------------------------------ game export
GAME_BONES = ["hips", "chest", "head", "upper_arm.L", "forearm.L", "upper_arm.R", "forearm.R", "thigh.L", "shin.L", "foot.L", "thigh.R", "shin.R", "foot.R"]
FACE = {"Angry": [1, 0, 0], "Surprised": [0, 1, 0], "Happy": [0, 0, 1], "Neutral": [0, 0, 0]}   # the game's fierce / shock / smug channels
def game_pose(arm, P, rest_hips):
    """This pose for the game: per bone the world rotation from rest -> posed, as a quaternion in the game rig's axes
    (x forward, y up, z = his right: Blender (x, y, z) -> (x, z, -y)). Arms are measured from the game's resting arms
    (hanging 8 deg out, see dressHaru) rather than Blender's A-pose, so the same numbers fit every character's rig."""
    out = {}
    for n in GAME_BONES:
        pb = arm.pose.bones[n]; rest = pb.bone.matrix_local.to_quaternion()
        if n.startswith(("upper_arm", "forearm")):   # rest -> the game's hanging arm (same construction as dressHaru's fix)
            ua = arm.pose.bones["upper_arm" + n[-2:]].bone; d = (ua.matrix_local.to_3x3() @ Vector((0, 1, 0))).normalized()
            h = Vector((d.x, d.y, 0)).normalized(); tgt = h * math.sin(0.14) + Vector((0, 0, -math.cos(0.14)))
            rest = d.rotation_difference(tgt) @ rest
        q = pb.matrix.to_quaternion() @ rest.inverted()
        out[n.replace(".", "")] = [round(v, 4) for v in (q.x, q.z, -q.y, q.w)]   # three.js order x, y, z, w
    dh = arm.pose.bones["hips"].head - rest_hips                                   # metres: crouch / lean / jump
    return dict(bones=out, hip=[round(v, 4) for v in (dh.x, dh.z, -dh.y)], face=FACE[P["expr"]])

def bone_pts(arm, names, b):
    pts = []
    for n in names:
        if n == "ball": pts += [b.location + Vector((x, y, z)) * BALL_R for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        else: pb = arm.pose.bones[n]; pts += [arm.matrix_world @ pb.head, arm.matrix_world @ pb.tail]
    return pts

def body_pts():
    dg = bpy.context.evaluated_depsgraph_get(); pts = []
    for o in bpy.data.collections["Haru"].objects:
        if o.type == 'MESH' and not o.hide_render:
            e = o.evaluated_get(dg); pts += [o.matrix_world @ Vector(c) for c in e.bound_box]
    return pts

def frame(cam, pts, az, el, pad, persp=False, grow=0.0):
    """Point the camera from azimuth/elevation so the points fill a square frame (ortho, or a 50mm perspective)."""
    a, e = radians(az), radians(el); z = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    up = Vector((0, 0, 1)) if abs(el) < 80 else Vector((1, 0, 0)); x = up.cross(z).normalized(); y = z.cross(x)
    px, py, pz = [p.dot(x) for p in pts], [p.dot(y) for p in pts], [p.dot(z) for p in pts]
    size = max(max(px) - min(px), max(py) - min(py)) * pad + grow
    c = x * (min(px) + max(px)) / 2 + y * (min(py) + max(py)) / 2 + z * (min(pz) + max(pz)) / 2
    if persp:
        cam.data.type = 'PERSP'; cam.data.lens = 50; dist = size / 2 / math.tan(math.atan(18 / 50)) + (max(pz) - min(pz)) / 2
    else:
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = size; dist = 6
    cam.data.clip_start, cam.data.clip_end = 0.01, 60
    cam.matrix_world = Matrix.Translation(c + z * dist) @ Matrix((x, y, z)).transposed().to_4x4()
    return c + z * dist

def render(sc, name, res=800):
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True); say("rendered", name)

try:
    cam = RH.studio(); sc = bpy.context.scene; arm = bpy.data.objects["HaruRig"]
    bpy.context.scene.collection.children.link(bpy.data.collections.new("FX"))
    body = list(bpy.data.collections["Haru"].objects); b = ball(); only = os.environ.get("HARU_POSES")
    for pb in arm.pose.bones: pb.matrix_basis.identity()
    bpy.context.view_layer.update(); rest_hips = arm.pose.bones["hips"].head.copy(); game = {}
    for P in POSES:
        if only and P["id"] not in only.split(","): continue
        RH.set_wire(False); RH.show(body); RH.set_expression(P["expr"]); pose(arm, P)
        game[P["id"]] = game_pose(arm, P, rest_hips)
        if os.environ.get("HARU_EXPORT_ONLY"): continue
        ft, fh = arm.matrix_world @ arm.pose.bones["foot.R"].tail, arm.matrix_world @ arm.pose.bones["foot.R"].head
        bp = P["ball"]
        b.location = Vector(bp[1:]) if bp[0] == "air" else ft + (ft - fh).normalized() * BALL_R * 0.9 + Vector(bp)
        if not P.get("air") and bp[0] != "air": b.location.z = max(b.location.z, BALL_R)   # resting on (or skimming) the turf
        b.rotation_euler = (0.4, 0.7, 0.2); b.hide_render = False
        bpy.context.view_layer.update()
        view = frame(cam, body_pts() + bone_pts(arm, ["ball"], b), *P["cam"], 1.0, persp=True)
        effects(P, arm, b, view); render(sc, f"pose_{P['id']}_hero", 900)
        for nm, lbl, bones, az, el in P["details"]:
            view = frame(cam, bone_pts(arm, bones, b), az, el, 1.35, grow=0.12)
            effects(P, arm, b, view); render(sc, f"pose_{P['id']}_{nm}", 600)
        clear_fx(); b.hide_render = True; RH.set_wire(True)
        for v, az in (("front", 0), ("side", -90), ("back", 180)):
            frame(cam, body_pts(), az, 0, 1.04); render(sc, f"pose_{P['id']}_wire_{v}", 600)
    RH.set_wire(False)
    if game and not only:
        import json
        with open(os.path.join(os.path.dirname(HERE), "poses.json"), "w") as fh: json.dump(game, fh, separators=(",", ":"))
        say("poses.json written:", list(game))
    say("DONE")
except Exception:
    say(traceback.format_exc()); say("FAILED")
log.close()
