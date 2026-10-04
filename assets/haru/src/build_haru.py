"""Nuem (#9, Akebono FC) - built from the character sheet. Run headless:
    bash run_blender.sh build_haru.py
Writes ../haru.blend. Metres, +X forward, +Y = his left, Z up (a glTF export turns this into the game's axes).
"""
import bpy, bmesh, math, random, traceback, os
from math import radians, sin, cos, pi
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "build_haru.log")
OUT = os.path.join(os.path.dirname(HERE), "haru.blend")
log = open(LOG, "w")
def say(*a): print(*a, file=log, flush=True)

# ------------------------------------------------------------------ helpers
def lin(h):
    h = h.lstrip('#'); f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(f(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)) + (1,)

MATS = {}
def mat(name, hexc, rough=0.5, sss=0.0, spec=0.5):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new("Haru_" + name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Roughness"].default_value = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs: b.inputs[k].default_value = spec; break
    if sss and "Subsurface Weight" in b.inputs:
        b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2)
        if "Subsurface Scale" in b.inputs: b.inputs["Subsurface Scale"].default_value = 0.01
    m.diffuse_color = lin(hexc); MATS[name] = m
    return m

def mat_vc(name, rough=0.45, spec=0.3):
    """Material whose base colour is the "Col" vertex colour (exported to glTF as COLOR_0)."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new("Haru_" + name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = spec
    vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "Col"
    nt.links.new(vc.outputs["Color"], b.inputs["Base Color"]); MATS[name] = m
    return m

def mix(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))

EXPRESSIONS = ("Happy", "Surprised", "Angry", "Sad", "Wink")
def add_keys(o, fn):
    """Shape keys for every expression on a part whose mesh is in world space. fn(name, co, i) -> new co."""
    o.shape_key_add(name="Basis", from_mix=False)
    base = [v.co.copy() for v in o.data.vertices]
    for name in EXPRESSIONS:
        k = o.shape_key_add(name=name, from_mix=False)
        for i, c in enumerate(base): k.data[i].co = fn(name, c, i)

COL = None
def new_obj(name, bm, mats, smooth=True, recalc=True):
    if recalc: bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in (mats if isinstance(mats, (list, tuple)) else [mats]): me.materials.append(m)
    try: me.shade_smooth() if smooth else me.shade_flat()
    except AttributeError:
        for p in me.polygons: p.use_smooth = smooth
    o = bpy.data.objects.new(name, me); COL.objects.link(o)
    return o

def bake_modifiers(o):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    old = o.data; o.modifiers.clear(); o.data = me; me.name = o.name
    bpy.data.meshes.remove(old)

def tube(name, pts, radii, mats, seg=12, bands=None, zig=0.0, ref=Vector((0, 0, 1)), smooth=True, vcol=None):
    """Tube along a polyline. radii[i] = r or (rn, rb) (rn across, rb along the ref side). A final radius of 0 ends in a point.
    bands[k] = material slot for the band between ring k and k+1. zig lifts every other vertex of ring 0 (zig-zag hem)."""
    n = len(pts); bm = bmesh.new(); rings = []
    cl = bm.verts.layers.float_color.new("Col") if vcol else None   # before any vertex: adding a layer later invalidates them
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        u = ref if abs(t.dot(ref.normalized())) < 0.97 else (Vector((1, 0, 0)) if abs(t.x) < 0.9 else Vector((0, 1, 0)))
        nn = t.cross(u).normalized(); bb = t.cross(nn).normalized()
        r = radii[i]; rn, rb = r if isinstance(r, tuple) else (r, r)
        if i == n - 1 and rn == 0:
            rings.append(bm.verts.new(p)); continue
        ring = []
        for j in range(seg):
            a = 2 * pi * j / seg
            v = bm.verts.new(p + nn * (rn * cos(a)) + bb * (rb * sin(a)))
            if i == 0 and zig and j % 2: v.co.z += zig
            ring.append(v)
        rings.append(ring)
    if vcol:   # one RGBA per ring
        for ring, c in zip(rings, vcol):
            for v in (ring if isinstance(ring, list) else [ring]): v[cl] = c
    band = lambda k: (bands[min(k, len(bands) - 1)] if bands else 0)
    for k in range(n - 1):
        a, b = rings[k], rings[k + 1]
        for j in range(seg):
            f = bm.faces.new((a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j])) if isinstance(b, list) else bm.faces.new((a[j], a[(j + 1) % seg], b))
            f.material_index = band(k)
    c = bm.verts.new(sum((v.co for v in rings[0]), Vector()) / seg)
    if vcol: c[cl] = vcol[0]
    for j in range(seg): bm.faces.new((c, rings[0][(j + 1) % seg], rings[0][j])).material_index = band(0)
    if isinstance(rings[-1], list):
        c = bm.verts.new(sum((v.co for v in rings[-1]), Vector()) / seg)
        if vcol: c[cl] = vcol[-1]
        for j in range(seg): bm.faces.new((c, rings[-1][j], rings[-1][(j + 1) % seg])).material_index = band(n - 2)
    return new_obj(name, bm, mats, smooth)

def ellipsoid(name, r, m, loc, scale=(1, 1, 1), seg=24, rings=16, mw=None):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    for v in bm.verts: v.co.x *= scale[0]; v.co.y *= scale[1]; v.co.z *= scale[2]
    o = new_obj(name, bm, m)
    if mw is not None: o.matrix_world = mw
    else: o.location = loc
    return o

def rbox(name, size, loc, m, bevel=0.01, segs=3, rot=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
    if bevel: bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=segs, affect='EDGES')
    o = new_obj(name, bm, m); o.location = loc; o.rotation_euler = rot
    return o

def bezier(p0, p1, p2, n):
    return [p0 * (1 - t) ** 2 + p1 * 2 * (1 - t) * t + p2 * t * t for t in (i / (n - 1) for i in range(n))]

def join(name, objs):
    objs = [o for o in objs if o]
    for o in bpy.context.selected_objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active; o.name = name; o.data.name = name
    return o

def apply_transforms(o):
    o.data.transform(o.matrix_world); o.matrix_world = Matrix.Identity(4)

# ------------------------------------------------------------------ build
def build():
    global COL
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    COL = bpy.data.collections.new("Haru"); bpy.context.scene.collection.children.link(COL)
    random.seed(9)

    # palette (sheet: red, amber, white, skin, grey, charcoal)
    SKIN = mat("Skin", '#f6c9a6', 0.55, sss=0.15, spec=0.35)
    SKIN_D = mat("SkinShade", '#e9a98a', 0.6, spec=0.3)
    WHITE = mat("Shirt", '#f3f4f7', 0.75, spec=0.3)
    RED = mat("KitRed", '#e3262e', 0.6, spec=0.35)
    RED_D = mat("KitRedDark", '#b81a24', 0.65, spec=0.3)
    SHOE_R = mat("ShoeRed", '#e5262d', 0.4)
    BLACK = mat("ShoeBlack", '#1c1d22', 0.45)
    SOLE = mat("Sole", '#f1f2f5', 0.5)
    GREY = mat("Stud", '#9aa0aa', 0.4)
    HAIR = mat_vc("Hair", 0.32, spec=0.55)                      # sheet: glossy candy-red spikes
    H_ROOT, H_MID, H_TIP = lin('#8e0a1c'), lin('#dc1020'), lin('#ff2e36')   # crimson -> red -> hot red, no orange
    LASH_UP = mat("LashUp", '#121216', 0.4)
    LASH_LO = mat("LashLow", '#2b1c1c', 0.5)
    TEETH = mat("Teeth", '#fbfaf6', 0.3)
    MOUTH_IN = mat("MouthIn", '#58161b', 0.6)
    TONGUE = mat("Tongue", '#e26a72', 0.5)
    EYE_W = mat("EyeWhite", '#fbfbfd', 0.2)
    IRIS = mat("Iris", '#f5a91c', 0.25)
    IRIS_D = mat("IrisRim", '#b8640c', 0.3)
    PUPIL = mat("Pupil", '#0d0d10', 0.2)
    GLINT = mat("Glint", '#ffffff', 0.1)
    MOUTH = mat("Mouth", '#7c2d2d', 0.5)
    BROW = mat("Brow", '#1a1416', 0.6)

    # ---- body: one skinned mesh (Skin + Subsurf modifiers baked), A-pose 22 deg
    bm = bmesh.new(); sl = bm.verts.layers.skin.verify()
    def sv(p, rx, ry=None, root=False):
        v = bm.verts.new(p); v[sl].radius = (rx, ry if ry else rx); v[sl].use_root = root; return v
    def se(a, b): bm.edges.new((a, b))
    pelvis = sv((0, 0, 0.52), 0.085, 0.10, root=True)
    waist = sv((0, 0, 0.62), 0.075, 0.09); chest = sv((0.005, 0, 0.76), 0.085, 0.10); up = sv((0, 0, 0.86), 0.07, 0.09)
    neck0 = sv((0, 0, 0.93), 0.046); neck1 = sv((0.005, 0, 1.01), 0.043)
    for a, b in ((pelvis, waist), (waist, chest), (chest, up), (up, neck0), (neck0, neck1)): se(a, b)
    ARM = {}
    for s in (1, -1):
        sh = Vector((0, 0.125 * s, 0.865)); d1 = Vector((0.0, 0.375 * s, -0.927)).normalized(); d2 = Vector((0.06, 0.33 * s, -0.94)).normalized()
        el = sh + d1 * 0.195; wr = el + d2 * 0.18; palm = wr + d2 * 0.045
        ARM[s] = (sh, d1, el, d2, wr)
        # The Skin modifier melts fingers into a mitten (and Subsurf shrinks a palm to a nub), so the body arm ends at the
        # wrist; palm + fingers are a separate mesh (Hand_L / Hand_R, built below, rigid on the hand bone).
        vs = sv(sh, 0.054); ve = sv(el, 0.045); vw = sv(wr, 0.036)
        se(up, vs); se(vs, ve); se(ve, vw)
        hip = sv((0, 0.066 * s, 0.50), 0.064); kn = sv((0.006, 0.068 * s, 0.29), 0.048); an = sv((0, 0.068 * s, 0.085), 0.036)
        se(pelvis, hip); se(hip, kn); se(kn, an)
    body = new_obj("Body", bm, SKIN)
    m = body.modifiers.new("Skin", 'SKIN'); m.branch_smoothing = 0.6; m.use_smooth_shade = True
    m = body.modifiers.new("Subsurf", 'SUBSURF'); m.levels = 2; m.render_levels = 2
    bake_modifiers(body)

    # ---- head: round and wide like the sheet, short round chin
    HC = Vector((0.006, 0, 1.12)); HA, HB, HZ = 0.13, 0.132, 0.135
    CHIN = 0.9                                         # lower half of the head is squashed: short, round chin
    jaw = lambda dz: 1 - 0.1 * (max(0.0, -dz) / (HZ * CHIN)) ** 1.3
    cheek = lambda dz: 0.007 * sin(pi * (-dz / 0.075)) if -0.075 < dz < 0.0 else 0.0   # full cheeks (front only)
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=28, radius=1)
    for v in bm.verts:
        zz = v.co.z * HZ * (CHIN if v.co.z < 0 else 1); k = jaw(zz)
        v.co.x *= HA * k; v.co.y *= HB * k; v.co.z = zz
        if v.co.x > 0: v.co.x += cheek(v.co.z)
    head = new_obj("Head", bm, SKIN); head.location = HC
    def surf(y, z):
        dz = z - HC.z; k = jaw(dz); a, b = HA * k, HB * k; c = HZ * (CHIN if dz < 0 else 1)
        x = a * math.sqrt(max(0.0, 1 - (y / b) ** 2 - (dz / c) ** 2))
        nrm = Vector((x / a ** 2, y / b ** 2, dz / c ** 2)).normalized()
        return HC + Vector((x + (cheek(dz) if x > 0 else 0.0), y, dz)), nrm
    def on_face(y, z, out): q, nq = surf(y, z); return q + nq * out
    def frame(p, n, scale=(1, 1, 1), fwd=0.0):
        return (Matrix.Translation(p) @ n.to_track_quat('X', 'Z').to_matrix().to_4x4() @ Matrix.Translation((fwd, 0, 0))
                @ Matrix.Diagonal((*scale, 1)))
    for s in (1, -1):  # big ears that stand out from the head (the hair is cut away around them)
        rot = Matrix.Rotation(-0.3 * s, 4, 'Z')
        ellipsoid("Ear", 0.038, SKIN, None, (0.5, 0.32, 0.85), seg=18, rings=12, mw=Matrix.Translation(HC + Vector((-0.01, 0.134 * s, -0.014))) @ rot)
        ellipsoid("EarInner", 0.024, SKIN_D, None, (0.36, 0.2, 0.68), seg=14, rings=10, mw=Matrix.Translation(HC + Vector((-0.006, 0.143 * s, -0.014))) @ rot)

    # ---- eyes. Eye space: +X out of the face, +Y = his left, +Z up. The sheet: white, big amber iris, big pupil,
    # heavy upper lash with an outer flick, thin lower line. Expressions move each part in eye space.
    EA, EB = 0.034, 0.038
    def eye_part(name, m, F, kind, s, build):
        o = build(); apply_transforms(o); Fi = F.inverted()
        def fn(expr, c, i):
            l = Fi @ c
            l = eye_expr(expr, kind, s, l)
            return F @ l
        add_keys(o, fn); return o
    def lid(expr, s, ly):
        if expr == "Angry": return 0.3 * EB + 0.5 * (ly * s)     # inner corner low: diagonal scowl lid
        if expr == "Sad": return 0.55 * EB - 0.35 * (ly * s)     # outer corner droops
        return None
    def eye_expr(expr, kind, s, l):
        l = l.copy(); L = lid(expr, s, l.y)
        if expr == "Surprised":
            l.y *= 1.07; l.z *= 1.07
            if kind == "pupil": l.y *= 0.85; l.z *= 0.85
        elif expr == "Happy":
            if l.z < 0 and kind != "lash_up": l.z *= 0.85
        elif expr == "Wink" and s < 0:                           # his right eye closes to an arc
            if kind == "lash_up":
                zc = EB * math.sqrt(max(0.0, 1 - (l.y / EA) ** 2)); l.z = (l.z - zc) + (-0.004 + zc * 0.4)
            else:
                l.z *= 0.03; l.y *= 0.9; l.x -= 0.024               # tucked inside the head
        elif L is not None:
            if kind == "lash_up":
                zc = EB * math.sqrt(max(0.0, 1 - (l.y / EA) ** 2)); l.z += min(zc, L) - zc
            elif kind != "lash_lo":
                l.z = min(l.z, L)
        return l
    for s in (1, -1):
        p, n = surf(0.05 * s, HC.z + 0.004); F = frame(p, n)
        def blob(nm, m, fwd, sx, ry, rz, at=(0, 0)):
            return lambda: ellipsoid(nm, 1.0, m, None, (1, 1, 1), seg=24, rings=16, mw=F @ Matrix.Translation((fwd, at[0], at[1])) @ Matrix.Diagonal((sx, ry, rz, 1)))
        eye_part("EyeWhite", EYE_W, F, "white", s, blob("EyeWhite", EYE_W, -0.002, 0.016, EA, EB))
        eye_part("IrisRim", IRIS_D, F, "iris", s, blob("IrisRim", IRIS_D, 0.003, 0.0125, 0.0275, 0.03))
        eye_part("Iris", IRIS, F, "iris", s, blob("Iris", IRIS, 0.0045, 0.0125, 0.0245, 0.027))
        eye_part("Pupil", PUPIL, F, "pupil", s, blob("Pupil", PUPIL, 0.011, 0.008, 0.015, 0.017))
        eye_part("Glint", GLINT, F, "glint", s, blob("Glint", GLINT, 0.018, 0.003, 0.0075, 0.0075, (0.007 * s, 0.01)))
        eye_part("Glint2", GLINT, F, "glint", s, blob("Glint2", GLINT, 0.018, 0.003, 0.0035, 0.0035, (-0.008 * s, -0.009)))
        inner, outer = (pi, 0.0) if s > 0 else (0.0, pi)
        rim = lambda t, g=0.001: F @ Vector((-0.0005, (EA + g) * cos(t), (EB + g) * sin(t)))
        up = [rim(inner + (outer - inner) * i / 12) for i in range(13)] + [F @ Vector((-0.002, (EA + 0.009) * s, 0.007))]
        up_r = [k * 1.3 for k in [0.0025, 0.0035, 0.0045, 0.0052, 0.0056] + [0.0058] * 5 + [0.0056, 0.0052, 0.0048, 0.0022]]
        eye_part("EyeLashUp", LASH_UP, F, "lash_up", s, lambda: tube("EyeLashUp", up, [(r, r * 0.6) for r in up_r], LASH_UP, seg=10, ref=n))
        lo_end = 2 * pi if s > 0 else -pi          # under the eye, inner corner -> outer corner
        lo = [rim(inner + (lo_end - inner) * i / 12, 0.0) for i in range(13)]
        eye_part("EyeLashLow", LASH_LO, F, "lash_lo", s, lambda: tube("EyeLashLow", lo, [0.0008] + [0.0016] * 11 + [0.0008], LASH_LO, seg=8, ref=n))

        # brows: thick rounded bars like the sheet
        bpts = []
        for i in range(9):
            t = i / 8; y = (0.016 + 0.056 * t) * s; z = HC.z + 0.064 + 0.006 * sin(pi * t) - 0.002 * t
            bpts.append(on_face(y, z, 0.003))
        brow = tube("Brow", bpts, [(0.0075, 0.0045), (0.012, 0.0052)] + [(0.0132, 0.0055)] * 5 + [(0.012, 0.0052), (0.0075, 0.0045)], BROW, seg=12, ref=Vector((1, 0, 0)))
        def brow_fn(expr, c, i, s=s):
            v = min(1.0, max(0.0, (abs(c.y) - 0.016) / 0.056))   # 0 at the inner end
            dz = {"Happy": 0.004, "Surprised": 0.014 + 0.003 * sin(pi * v), "Angry": -0.016 * (1 - v) + 0.005 * v,
                  "Sad": 0.012 * (1 - v) - 0.006 * v, "Wink": -0.006 if s < 0 else 0.003}[expr]
            return c + Vector((0, 0, dz))
        add_keys(brow, brow_fn)

    pn, nn = surf(0, HC.z - 0.027)   # no cheek blush: the sheet's face is clean skin
    ellipsoid("Nose", 0.011, SKIN, None, (1, 0.95, 0.85), seg=16, rings=12, mw=frame(pn, nn, (1, 1, 1), 0.001))

    # ---- mouth: a closed smile line + an open mouth (teeth / inside / tongue) that is tucked into the head until
    # Happy, Surprised or Wink pulls it out. Both are driven by the same shape key names as the eyes and brows.
    MZ = HC.z - 0.066
    line_y = lambda t: t * 0.044
    line_z = lambda t: MZ + 0.008 * (2 * t) ** 2
    pts = [on_face(line_y(i / 10 - 0.5), line_z(i / 10 - 0.5), 0.0012) for i in range(11)]
    mline = tube("Mouth", pts, [0.0016, 0.0022] + [0.0025] * 7 + [0.0022, 0.0016], MOUTH, seg=8)
    def mline_fn(expr, c, i):
        t = max(-0.5, min(0.5, c.y / 0.044)); off = c - on_face(line_y(t), line_z(t), 0.0012)
        if expr in ("Happy", "Surprised", "Wink"): return on_face(line_y(t), line_z(t), -0.012) + off
        if expr == "Angry": return on_face(line_y(t) * 0.72, MZ + 0.002 - 0.008 * (2 * t) ** 2, 0.0012) + off
        return on_face(line_y(t) * 0.8, MZ + 0.003 - 0.007 * (2 * t) ** 2, 0.0012) + off   # Sad
    add_keys(mline, mline_fn)
    def mouth_d(u, v, W, H, top, curve, tilt):
        zt = MZ + top + curve * u * u + tilt * u; zb = zt - H * max(0.0, 1 - u * u) ** 0.6
        return u * W * (1 - 0.08 * v), zt + (zb - zt) * v
    def mouth_at(expr, u, v):
        if expr == "Happy": return on_face(*mouth_d(u, v, 0.034, 0.03, 0.004, 0.006, 0.0), 0.0012)
        if expr == "Wink": return on_face(*mouth_d(u, v, 0.026, 0.019, 0.003, 0.006, 0.006), 0.0012)
        if expr == "Surprised":
            hw = 0.017 * max(0.35, math.sqrt(max(0.0, 1 - (2 * v - 1) ** 2)))
            return on_face(u * hw, MZ + 0.007 - 0.032 * v, 0.0012)
        return on_face(u * 0.02, MZ + 0.008 * u * u, -0.012)   # closed: tucked inside the head
    NU, NV = 14, 8; bm = bmesh.new(); grid = {}; uvs = []
    for j in range(NV + 1):
        for i in range(NU + 1):
            u, v = -1 + 2 * i / NU, j / NV; uvs.append((u, v))
            grid[i, j] = bm.verts.new(mouth_at("Neutral", u, v))
    for j in range(NV):
        for i in range(NU):
            f = bm.faces.new((grid[i, j], grid[i, j + 1], grid[i + 1, j + 1], grid[i + 1, j]))   # faces +X
            uc, vc = -1 + 2 * (i + 0.5) / NU, (j + 0.5) / NV
            f.material_index = 0 if vc < 0.22 else (2 if vc > 0.58 and abs(uc) < 0.8 else 1)
    mopen = new_obj("MouthOpen", bm, [TEETH, MOUTH_IN, TONGUE], recalc=False)
    add_keys(mopen, lambda expr, c, i: mouth_at(expr, *uvs[i]))

    # ---- hair: big smooth leaf-petals in an artichoke crown, crimson root -> red -> orange tip (vertex colour)
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=48, radius=1)
    for v in bm.verts: v.co.x *= HA * 1.06; v.co.y *= HB * 1.07; v.co.z *= HZ * 1.05
    def ss(a, b, x): t = min(1, max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
    cut = [v for v in bm.verts if v.co.z < -0.115 + 0.225 * ss(-0.02, 0.12, v.co.x)
           or (abs(v.co.y) > 0.085 and v.co.z < 0.018 and v.co.x > -0.075)    # around the ears
           or (v.co.x > 0.03 and v.co.z < 0.115)]   # whole front: the fringe + temple locks are the hairline (cap sat over their tips)
    bmesh.ops.delete(bm, geom=cut, context='VERTS')
    cl = bm.verts.layers.float_color.new("Col")
    for v in bm.verts: v[cl] = mix(H_ROOT, H_MID, 0.3)
    cap = new_obj("HairCap", bm, HAIR); cap.location = HC + Vector((-0.004, 0, 0.004))
    sol = cap.modifiers.new("Solidify", 'SOLIDIFY'); sol.thickness = 0.006; sol.offset = -1
    bake_modifiers(cap)

    petals = []
    def petal(phi, theta, length, width, axis_bias, bend, root_in=0.9):
        ph, th = radians(phi), radians(theta)
        d = Vector((sin(ph) * cos(th), sin(ph) * sin(th), cos(ph)))
        root = HC + Vector((d.x * HA, d.y * HB, d.z * HZ)) * root_in
        ax = (d + axis_bias).normalized()
        ax = (Matrix.Rotation(radians(random.uniform(-7, 7)), 3, 'Z') @ Matrix.Rotation(radians(random.uniform(-6, 6)), 3, 'Y') @ ax).normalized()
        length *= random.uniform(0.9, 1.1); w = width * random.uniform(0.92, 1.08)
        pts = bezier(root, root + ax * length * 0.55 + bend * length * 0.05, root + ax * length + bend * length * 0.25, 7)
        prof = (0.62, 0.95, 1.0, 0.86, 0.6, 0.3, 0)
        radii = [(w * k, w * k * 0.62) for k in prof[:-1]] + [0]       # sheet spikes are plump rounded cones, not flat blades
        cols = [mix(H_ROOT, H_MID, min(1, u / 0.45)) if u < 0.45 else mix(H_MID, H_TIP, (u - 0.45) / 0.55) for u in (i / 6 for i in range(7))]
        petals.append(tube("Petal", pts, radii, HAIR, seg=10, ref=d, vcol=cols))
    swirl = lambda th: Vector((-sin(radians(th)), cos(radians(th)), 0))
    wrap = lambda th: ((th + 180) % 360) - 180
    petal(0, 0, 0.15, 0.062, Vector((-0.1, 0, 0.6)), Vector((-0.25, 0, 0)))
    for i in range(5): th = i * 72 + 20; petal(17, th, 0.14, 0.062, Vector((-0.1, 0, 0.85)), swirl(th) * 0.3)
    for i in range(9): th = i * 40 + 5; petal(36, th, 0.13, 0.06, Vector((-0.12, 0, 0.6)), swirl(th) * 0.3)
    for i in range(12):
        th = i * 30 + 15
        if abs(wrap(th)) > 50: petal(56, th, 0.115, 0.058, Vector((-0.15, 0, 0.4)), swirl(th) * 0.3)
    for i in range(12):
        th = i * 30
        if abs(wrap(th)) > 75: petal(78, th, 0.1, 0.054, Vector((-0.2, 0, 0.05)), swirl(th) * 0.25)
    for i in range(8):
        th = 112.5 + i * 19.3
        petal(98, th, 0.085, 0.05, Vector((-0.3, 0, -0.45)), Vector((0, 0, -0.3)))
    for i in range(6):
        th = 135 + i * 18
        petal(116, th, 0.065, 0.045, Vector((-0.2, 0, -0.7)), Vector((0, 0, -0.3)), root_in=0.93)
    # fringe: petals that lie along the forehead (wide face to the front) and hang down to a point.
    # The centre one drops between the brows, the outer ones stop above them (the sheet).
    def fringe(th_root, th_tip, tip_z, width):
        cos_t = max(-1.0, min(1.0, (tip_z - HC.z) / HZ)); ph_tip = math.degrees(math.acos(cos_t)); ph_root = 24
        pts = []
        for i in range(7):
            u = i / 6
            ph, th = radians(ph_root + (ph_tip - ph_root) * u), radians(th_root + (th_tip - th_root) * u)
            d = Vector((sin(ph) * cos(th), sin(ph) * sin(th), cos(ph)))
            on = HC + Vector((d.x * HA, d.y * HB, d.z * HZ))
            pts.append(on + d * (0.01 + 0.02 * sin(pi * min(1.0, u * 1.15)) + 0.01 * (1 - u)))   # clears the hair cap, bulges, tip rests on the skin
        d0 = (pts[0] - HC).normalized()
        prof = (0.6, 0.88, 1.0, 1.0, 0.85, 0.5, 0)     # stays full low down, then a short point
        radii = [(width * k, width * k * 0.6) for k in prof[:-1]] + [0]
        cols = [mix(H_ROOT, H_MID, min(1, u / 0.4)) if u < 0.4 else mix(H_MID, H_TIP, (u - 0.4) / 0.6) for u in (i / 6 for i in range(7))]
        petals.append(tube("Fringe", pts, radii, HAIR, seg=10, ref=d0, vcol=cols))
    # w is a half-width: ~6 cm petals 20 deg apart overlap by half, so each keeps its own point (scalloped edge)
    for th, z, w in ((-60, 0.09, 0.026), (60, 0.09, 0.026), (-40, 0.084, 0.029), (40, 0.084, 0.029),
                     (-20, 0.078, 0.031), (20, 0.078, 0.031), (0, 0.069, 0.034)):
        fringe(th * 0.75, th, HC.z + z, w)    # outer petals splay a little toward the temples
    for sd in (1, -1):
        fringe(62 * sd, 80 * sd, HC.z + 0.005, 0.03)    # temple locks, in front of the ears
    hair = join("Hair", petals)

    # ---- shirt: zig-zag hem, red collar + cuffs, chest badge
    rings = [(0.548, 0.098, 0.128, 0.0), (0.58, 0.095, 0.124, 0.0), (0.66, 0.088, 0.116, 0.004), (0.76, 0.096, 0.128, 0.008),
             (0.845, 0.095, 0.152, 0.006), (0.89, 0.08, 0.138, 0.0), (0.92, 0.062, 0.086, 0.0), (0.935, 0.056, 0.058, 0.0)]
    shirt = tube("Shirt", [Vector((cx, 0, z)) for z, rx, ry, cx in rings], [(ry, rx) for z, rx, ry, cx in rings], WHITE, seg=32, zig=0.03, ref=Vector((1, 0, 0)))
    collar = tube("Collar", [Vector((0.002, 0, 0.918)), Vector((0.004, 0, 0.948))], [(0.063, 0.061), (0.057, 0.055)], RED, seg=24, ref=Vector((1, 0, 0)))
    parts = [shirt, collar]
    for s in (1, -1):
        sh, d1, el, d2, wr = ARM[s]
        a0 = sh - d1 * 0.02 + Vector((0, -0.012 * s, 0.004))
        parts.append(tube("Sleeve", [a0, a0 + d1 * 0.08, a0 + d1 * 0.115], [0.062, 0.058, 0.055], WHITE, seg=20))
        parts.append(tube("Cuff", [a0 + d1 * 0.105, a0 + d1 * 0.128], [0.058, 0.056], RED, seg=20))
    pb, nb = Vector((0.11, 0.05, 0.795)), Vector((1, 0.35, 0.05)).normalized()
    parts.append(ellipsoid("Badge", 0.022, RED, None, (1, 1, 1), seg=20, rings=12, mw=frame(pb, nb, (0.3, 1, 1))))
    shirt = join("Shirt", parts)

    # ---- shorts: wide legs, rolled cuffs, side pockets
    sh_parts = [tube("ShortsHip", [Vector((0, 0, 0.6)), Vector((0, 0, 0.53)), Vector((0, 0, 0.47))], [(0.118, 0.09), (0.125, 0.096), (0.128, 0.098)], RED, seg=28, ref=Vector((1, 0, 0)))]
    for s in (1, -1):
        c = 0.067 * s
        sh_parts.append(tube("ShortsLeg", [Vector((0, c, 0.5)), Vector((0, c * 1.02, 0.42)), Vector((0, c * 1.05, 0.355))], [(0.072, 0.076), (0.073, 0.077), (0.075, 0.079)], RED, seg=20, ref=Vector((1, 0, 0))))
        sh_parts.append(tube("ShortsCuff", [Vector((0, c * 1.05, 0.372)), Vector((0, c * 1.05, 0.345))], [(0.081, 0.085), (0.08, 0.084)], RED_D, seg=20, ref=Vector((1, 0, 0))))
    shorts = join("Shorts", sh_parts)

    # ---- socks with two red bands
    sk = []
    for s in (1, -1):
        c = Vector((0, 0.068 * s, 0))
        sk.append(tube("Sock", [c + Vector((0.004, 0, 0.31)), c + Vector((0.004, 0, 0.22)), c + Vector((0, 0, 0.13)), c + Vector((0, 0, 0.05))], [0.052, 0.05, 0.043, 0.044], WHITE, seg=18))
        for z in (0.285, 0.262):
            sk.append(tube("SockBand", [c + Vector((0.004, 0, z - 0.006)), c + Vector((0.004, 0, z + 0.006))], [0.0535, 0.0535], RED, seg=18))
    socks = join("Socks", sk)

    # ---- sneakers: white sole + black outsole, red upper, black toe cap, two velcro straps, studs
    shoes = []
    for s in (1, -1):
        y = 0.068 * s; ox = 0.04
        P = lambda x, z, yy=0.0: Vector((ox + x, y + yy, z))
        prt = []
        sole_x = [-0.13, -0.11, -0.05, 0.05, 0.12, 0.15]
        # sole hugs the upper (sheet: chunky rounded cupsole, not a flat slab sticking out)
        sole_x = [-0.122, -0.105, -0.05, 0.05, 0.115, 0.14]
        prt.append(tube("Sole", [P(x, 0.028) for x in sole_x], [(0.03, 0.018), (0.05, 0.024), (0.054, 0.025), (0.056, 0.025), (0.05, 0.023), (0.028, 0.016)], SOLE, seg=24))
        prt.append(tube("Outsole", [P(x, 0.01) for x in sole_x], [(0.028, 0.009), (0.047, 0.011), (0.051, 0.011), (0.053, 0.011), (0.047, 0.011), (0.026, 0.008)], BLACK, seg=24))
        up_pts = [P(-0.115, 0.08), P(-0.075, 0.09), P(0.0, 0.082), P(0.06, 0.068), P(0.105, 0.058), P(0.137, 0.05)]
        up_r = [(0.044, 0.04), (0.052, 0.056), (0.054, 0.053), (0.054, 0.041), (0.049, 0.032), (0.0, 0.0)]
        up_r[-1] = 0
        prt.append(tube("Upper", up_pts, up_r, SHOE_R, seg=20, ref=Vector((0, 0, 1))))
        prt.append(ellipsoid("ToeCap", 0.047, BLACK, P(0.105, 0.052), (0.9, 1.1, 0.62), seg=20, rings=12))
        prt.append(tube("Collar", [P(-0.062, 0.115), P(-0.048, 0.142)], [(0.05, 0.046), (0.048, 0.044)], BLACK, seg=18, ref=Vector((1, 0, 0))))
        for x, zc, rn, rb in ((0.0, 0.082, 0.054, 0.053), (0.058, 0.068, 0.054, 0.041)):   # upper's cross-section there
            arc = [P(x, zc + (rb + 0.003) * sin(a), (rn + 0.003) * cos(a)) for a in (pi * i / 12 for i in range(13))]
            prt.append(tube("Strap", arc, [(0.0045, 0.015)] * 13, BLACK, seg=8, ref=Vector((1, 0, 0))))
            arc = [P(x, zc + (rb + 0.008) * sin(a), (rn + 0.008) * cos(a)) for a in (pi * i / 12 for i in range(3, 10))]
            prt.append(tube("StrapStripe", arc, [(0.0015, 0.004)] * 7, SOLE, seg=6, ref=Vector((1, 0, 0))))
        for sx in (-0.085, -0.035, 0.03, 0.08):
            for sy in (-0.028, 0.028):
                prt.append(rbox("Stud", (0.016, 0.016, 0.012), P(sx, -0.004, sy), GREY, bevel=0.004))
        sh_o = join("Shoe_" + ("L" if s > 0 else "R"), prt); apply_transforms(sh_o)
        c = Vector((ox, y, 0)); sh_o.data.transform(Matrix.Translation(c) @ Matrix.Diagonal((1.1, 1.14, 1.2, 1)) @ Matrix.Translation(-c))
        shoes.append(sh_o)

    # ---- hands: four curled fingers + a thumb per side. Fingers fan along X (front-back) from the palm, curl toward
    # the palm side (n_in), and end in round tips; one mesh per hand so it can ride the hand bone rigidly.
    for s in (1, -1):
        sh, d1, el, d2, wr = ARM[s]; X = Vector((1, 0, 0))
        n_in = X.cross(d2).normalized() * -s                     # palm faces the body
        def finger(base, d, ln, r, curl):
            pts, radii = [], []
            for i in range(10):
                u = i / 9; pts.append(base + d * ln * u + n_in * curl * ln * u * u)
                radii.append(r * (1 - 0.12 * u) if u < 0.78 else r * 0.88 * math.sqrt(max(0.0, 1 - ((u - 0.78) / 0.22) ** 2)))
            radii[-1] = 0
            return tube("Finger", pts, radii, SKIN, seg=12)
        Xo = (X - d2 * X.dot(d2)).normalized()
        palm_m = Matrix((Xo * 0.035, n_in * 0.019, d2 * 0.042)).transposed().to_4x4(); palm_m.translation = wr + d2 * 0.036
        palm_end = wr + d2 * 0.07
        parts = [ellipsoid("Palm", 1.0, SKIN, None, mw=palm_m, seg=24, rings=16)] + [finger(palm_end - d2 * 0.012 + X * off, (d2 + X * fan).normalized(), ln, r, 0.35)
                 for off, fan, ln, r in ((0.021, 0.16, 0.046, 0.0102), (0.007, 0.05, 0.052, 0.0108), (-0.007, -0.05, 0.049, 0.0104), (-0.02, -0.16, 0.039, 0.0094))]
        tb = wr + d2 * 0.022 + X * 0.026 + n_in * 0.006          # thumb: forward and in, from the heel of the palm
        parts.append(finger(tb, (d2 * 0.55 + X * 0.75 + n_in * 0.35).normalized(), 0.044, 0.012, 0.3))
        h = join("Hand_" + ("L" if s > 0 else "R"), parts); apply_transforms(h)
        h.data.transform(Matrix.Translation(wr) @ Matrix.Scale(1.45, 4) @ Matrix.Translation(-wr))   # toon hands: wider than the wrist

    # ---- tidy: apply transforms, then scale the head group about the chin (sheet proportions: big head, short neck)
    for o in list(COL.objects):
        if o.type == 'MESH': apply_transforms(o)
    piv = Vector((0.006, 0, 0.985)); big = Matrix.Translation(piv + Vector((0, 0, -0.012))) @ Matrix.Scale(1.28, 4) @ Matrix.Translation(-piv)
    for o in list(COL.objects):
        if o.name.startswith(("Head", "Hair", "Eye", "Iris", "Pupil", "Glint", "Brow", "Mouth", "Nose", "Ear", "Blush")): o.data.transform(big, shape_keys=True)
    eyes = [o for o in COL.objects if o.name.startswith(("EyeLash", "EyeWhite", "Iris", "Pupil", "Glint"))]
    join("Eyes", eyes)
    join("Face", [o for o in COL.objects if o.name.startswith(("Brow", "Mouth", "Nose", "Blush"))])
    join("Ears", [o for o in COL.objects if o.name.startswith("Ear")])
    for o in COL.objects:
        if o.type == 'MESH' and o.data.shape_keys:
            for kb in o.data.shape_keys.key_blocks: kb.value = 0.0
    sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'
    names = sorted(o.name for o in COL.objects)
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in COL.objects)
    say("objects:", names); say("triangles:", tris)
    for nm in ("Face", "Eyes"): say(nm, "shape keys:", [k.name for k in bpy.data.objects[nm].data.shape_keys.key_blocks])
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    say("saved", OUT)

try:
    build(); say("DONE")
except Exception:
    say(traceback.format_exc()); say("FAILED")
log.close()
