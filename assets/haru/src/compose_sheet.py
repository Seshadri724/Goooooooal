"""Lay the transparent renders out as the model sheet (13 numbered sections like the reference + expressions/pose).
Plain Python + Pillow:   python compose_sheet.py   -> ../renders/sheet.png  (also draws ../renders/uv_*.png from uv.json)
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "renders")
BG, PANEL, INK = (14, 18, 30), (24, 29, 44), (230, 232, 238)
try: F, FS, FL = ImageFont.truetype("arialbd.ttf", 24), ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 17)
except OSError: F = FS = FL = ImageFont.load_default()

def uv_panels():
    """One image per UV set: every face filled with its colour, island edges in dark ink (the sheet's UV MAPS panel)."""
    p = os.path.join(R, "uv.json")
    if not os.path.exists(p): return
    for name, faces in json.load(open(p)).items():
        S = 512; im = Image.new("RGB", (S, S), (32, 36, 50)); d = ImageDraw.Draw(im)
        for poly, rgb in faces:
            pts = [(u * S, (1 - v) * S) for u, v in poly]
            if len(pts) > 2: d.polygon(pts, fill=tuple(rgb), outline=(20, 20, 26))
        im.save(os.path.join(R, f"uv_{name}.png"))

W2 = lambda n, lbl: [(n + "_wire", lbl + " (WIRE)"), (n, lbl + " (SHADED)")]
VIEW = {"front": "FRONT", "side": "SIDE", "back": "BACK", "three_quarter": "3/4 VIEW", "top": "TOP"}
LEGEND = [("Eye Loop", "#8f8cf2"), ("Mouth Loop", "#e0404a"), ("Nose Loop", "#f0a830"), ("Eyebrow Loop", "#3cc060"),
          ("Face Contour", "#2fa8e8"), ("Ear Loop", "#f08a30"), ("Hair Base", "#f0d040")]
# title, header colour, columns, cell w, cell h, cells [(render, label)], (optional legend)
SECTIONS = [
    ("FULL CHARACTER (WIREFRAME)", (40, 70, 140), 4, 200, 330, [(f"wire_{v}", VIEW[v]) for v in ("front", "side", "back", "three_quarter")]),
    ("FULL CHARACTER (SHADED)", (140, 30, 50), 4, 200, 330, [(v, VIEW[v]) for v in ("front", "side", "back", "three_quarter")]),
    ("HEAD (WIREFRAME & SHADED)", (30, 110, 60), 4, 150, 148, [x for v in ("front", "side", "back", "top") for x in ((f"wire_head_{v}", VIEW[v] + " (WIRE)"), (f"head_{v}", VIEW[v] + " (SHADED)"))]),
    ("HAIR (DETAIL)", (140, 30, 50), 5, 140, 130, [("p_hair_" + v, VIEW[v]) for v in ("front", "side", "back", "top")] + [("p_strand", "STRAND (SHADED)")]
        + [("p_hair_" + v + "_wire", VIEW[v] + " (WIRE)") for v in ("front", "side", "back", "top")] + [("p_strand_wire", "STRAND (WIRE)")]),
    ("FACE DETAILS", (110, 40, 60), 4, 140, 130, W2("p_eye", "EYE") + W2("p_brow", "EYEBROW") + W2("p_nose", "NOSE") + W2("p_mouth", "MOUTH")),
    ("HEAD TOPOLOGY", (40, 70, 140), 1, 290, 290, [("p_topology", "FEATURE LOOPS")], LEGEND),
    ("BODY (TORSO)", (40, 70, 140), 1, 170, 150, [("p_torso_wire", "FRONT (WIRE)"), ("p_torso", "FRONT (SHADED)")]),
    ("ARMS", (40, 70, 140), 2, 120, 150, [("p_armL_wire", "LEFT (WIRE)"), ("p_armR_wire", "RIGHT (WIRE)"), ("p_armL", "LEFT (SHADED)"), ("p_armR", "RIGHT (SHADED)")]),
    ("HAND (DETAIL)", (120, 100, 20), 2, 120, 150, [("p_hand_palm_wire", "PALM (WIRE)"), ("p_hand_palm", "PALM (SHADED)"), ("p_hand_side_wire", "SIDE (WIRE)"), ("p_hand_side", "SIDE (SHADED)")]),
    ("LEGS", (30, 100, 90), 2, 120, 150, [("p_legs_front_wire", "FRONT (WIRE)"), ("p_legs_back_wire", "BACK (WIRE)"), ("p_legs_front", "FRONT (SHADED)"), ("p_legs_back", "BACK (SHADED)")]),
    ("SHORTS", (40, 70, 140), 2, 120, 150, [("p_shorts_front_wire", "FRONT (WIRE)"), ("p_shorts_back_wire", "BACK (WIRE)"), ("p_shorts_front", "FRONT (SHADED)"), ("p_shorts_back", "BACK (SHADED)")]),
    ("SHOES (DETAIL)", (90, 50, 140), 2, 120, 96, [("p_shoe_front", "FRONT"), ("p_shoe_side", "SIDE"), ("p_shoe_front_wire", "FRONT (WIRE)"), ("p_shoe_side_wire", "SIDE (WIRE)"),
                                                 ("p_shoe_sole_wire", "SOLE (WIRE)"), ("p_shoe_sole", "SOLE (SHADED)")]),
    ("UV MAPS (SEPARATE)", (40, 90, 150), 2, 120, 96, [("uv_Head", "HEAD UV"), ("uv_Hair", "HAIR UV"), ("uv_Shirt", "BODY UV"), ("uv_Shorts", "SHORTS UV"),
                                                      ("uv_Shoe_L", "SHOES UV"), ("uv_Eyes", "EYE UV")]),
    ("EXPRESSIONS", (150, 60, 20), 3, 130, 118, [(f"expr_{e}", e.upper()) for e in ("Neutral", "Happy", "Surprised", "Angry", "Sad", "Wink")]),
    ("HAIR, FACE & POSE", (40, 70, 140), 1, 150, 100, [("hair", "HAIR BACK"), ("face", "FACE 3/4"), ("pose_wave", "POSE")]),
]
LAYOUT = [[0, 1, 2], [3, 4, 5, 13], [6, 7, 8, 9, 10, 11, 12, 14]]   # sections per sheet row
PAD, HDR, LBL = 10, 38, 24

def fit(img, w, h, trim=True):
    if trim: img = img.crop(img.getbbox() or (0, 0, *img.size))   # trim transparent margin so every view fills its cell
    s = min(w / img.width, h / img.height) * (0.94 if trim else 1)
    return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)

def section(i):
    title, col, n, cw, ch, cells, *rest = SECTIONS[i]; legend = rest[0] if rest else None
    rows = -(-len(cells) // n); lw = 170 if legend else 0
    W = max(PAD + n * (cw + PAD) + lw, int(F.getlength(f"{i + 1}. {title}")) + 2 * PAD)   # never clip the title
    cw += (W - PAD - n * (cw + PAD) - lw) // n; H = HDR + PAD + rows * (ch + LBL + PAD)
    im = Image.new("RGB", (W, H), PANEL); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, HDR), fill=col); d.text((PAD, 7), f"{i + 1}. {title}", font=F, fill=INK)
    for k, (name, label) in enumerate(cells):
        x = PAD + (k % n) * (cw + PAD); y = HDR + PAD + (k // n) * (ch + LBL + PAD)
        d.rectangle((x, y, x + cw, y + ch + LBL), fill=BG)
        p = os.path.join(R, name + ".png")
        if os.path.exists(p):
            uv = name.startswith("uv_"); src = fit(Image.open(p).convert("RGBA"), cw - 6, ch - 6, trim=not uv)
            im.paste(src, (x + (cw - src.width) // 2, y + (ch - src.height) // 2), src)
        d.text((x + cw // 2, y + ch + LBL // 2), label, font=FS, fill=INK, anchor="mm")
    if legend:
        x0 = PAD + n * (cw + PAD) + 6
        for k, (lbl, hexc) in enumerate(legend):
            y = HDR + PAD + 18 + k * 30
            d.ellipse((x0, y - 7, x0 + 14, y + 7), fill=hexc); d.text((x0 + 24, y), lbl, font=FL, fill=INK, anchor="lm")
    return im

uv_panels()
rows = [[section(i) for i in r] for r in LAYOUT]
W = max(sum(s.width for s in r) + PAD * (len(r) + 1) for r in rows)
H = sum(max(s.height for s in r) for r in rows) + PAD * (len(rows) + 1)
sheet = Image.new("RGB", (W, H), BG); y = PAD
for r in rows:
    x = PAD; rh = max(s.height for s in r)
    for s in r:
        sheet.paste(s, (x, y))
        if s.height < rh: ImageDraw.Draw(sheet).rectangle((x, y + s.height, x + s.width - 1, y + rh - 1), fill=PANEL)  # even panel bottoms
        x += s.width + PAD
    y += rh + PAD
sheet.save(os.path.join(R, "sheet.png")); print("sheet", W, "x", H)

# ---- shooting pose sheet (poses_haru.py): per pose a column of hero shot, wireframe front/side/back, three close-ups
POSES = [("power", "POWER SHOT", [("contact", "FOOT CONTACT"), ("ext", "LEG EXTENSION"), ("twist", "BODY TWIST")]),
         ("instep", "INSTEP KICK", [("contact", "INSTEP CONTACT"), ("angle", "FOOT ANGLE"), ("follow", "FOLLOW THROUGH")]),
         ("chip", "CHIP SHOT", [("toe", "TOE CONTACT"), ("lift", "LIFT MOTION"), ("balance", "BODY BALANCE")]),
         ("volley", "VOLLEY SHOT", [("air", "AIR KICK"), ("angle", "FOOT ANGLE"), ("aerial", "AERIAL BALANCE")]),
         ("finish", "FINISHING SHOT", [("contact", "FOOT CONTACT"), ("follow", "FOLLOW THROUGH"), ("lean", "BODY LEAN")])]

def pose_sheet():
    if not os.path.exists(os.path.join(R, "pose_power_hero.png")): return
    CW, HERO, SW, SH, DH = 340, 340, 106, 150, 106
    col_h = HDR + HERO + PAD + SH + LBL + PAD + DH + LBL + PAD
    W = PAD + len(POSES) * (CW + PAD); TOP = 64
    sheet = Image.new("RGB", (W, TOP + col_h + PAD), BG); d = ImageDraw.Draw(sheet)
    d.rounded_rectangle((PAD, 10, PAD + 420, 54), 10, fill=(196, 34, 48)); d.text((PAD + 16, 32), "FOOTBALL POSES - SHOOTING", font=F, fill=INK, anchor="lm")
    def cell(name, x, y, w, h, label=None, back=True):
        if back: d.rectangle((x, y, x + w, y + h + (LBL if label else 0)), fill=BG)
        p = os.path.join(R, name + ".png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            src = fit(im, w - 4, h - 4) if "_wire_" in name else fit(im, w, h, trim=False)   # wire: trimmed to the figure; shots keep their framing
            sheet.paste(src, (x + (w - src.width) // 2, y + (h - src.height) // 2), src)
        if label:
            ft = FS if FS.getlength(label) <= w else ImageFont.truetype("arial.ttf", max(9, int(15 * w / FS.getlength(label))))   # shrink long labels to the cell
            d.text((x + w // 2, y + h + LBL // 2), label, font=ft, fill=INK, anchor="mm")
    for k, (pid, title, det) in enumerate(POSES):
        x = PAD + k * (CW + PAD); y = TOP
        d.rectangle((x, y, x + CW, y + col_h), fill=PANEL); d.rectangle((x, y, x + CW, y + HDR), fill=(120, 26, 36))
        d.text((x + PAD, y + 7), f"{k + 1}.  {title}", font=F, fill=INK)
        cell(f"pose_{pid}_hero", x, y + HDR, CW, HERO, back=False)
        y2 = y + HDR + HERO + PAD
        for j, v in enumerate(("front", "side", "back")):
            cell(f"pose_{pid}_wire_{v}", x + 4 + j * (SW + 6), y2, SW, SH, v.upper())
        y3 = y2 + SH + LBL + PAD
        for j, (nm, lbl) in enumerate(det):
            cell(f"pose_{pid}_{nm}", x + 4 + j * (SW + 6), y3, SW, DH, lbl)
    sheet.save(os.path.join(R, "poses.png")); print("poses", sheet.size)

pose_sheet()
