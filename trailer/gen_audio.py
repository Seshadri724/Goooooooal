"""Synthesises the X clip's soundtrack and sound effects (no samples, no API): python gen_audio.py
150 BPM, so one beat = 12 frames and one bar = 48 frames at 30 fps; XClip.tsx cuts on the same grid.
Writes public/audio/music.wav (139.2 s) and whoosh.wav, impact.wav, crowd.wav, riser.wav.
"""
import os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR, BPM, LEN = 44100, 150, 87 * 1.6   # 87 bars = 139.2 s: under X's 2:20 cap for non-Premium accounts
BEAT = 60 / BPM; BAR = 4 * BEAT
N = int(SR * LEN)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "audio")
rng = np.random.default_rng(7)

def t_(sec): return np.arange(int(SR * sec)) / SR
def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-6)) * np.exp(-t / d)
def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, 'highpass', fs=SR, output='sos'), x)
def lp(x, f, order=2): return sosfilt(butter(order, f, 'lowpass', fs=SR, output='sos'), x)
def saw(f, t): return 2 * ((f * t) % 1) - 1
def sq(f, t, w=0.5): return np.where((f * t) % 1 < w, 1.0, -1.0)
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def put(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += g * x

# ---- one-shots
def kick():
    t = t_(0.45); f = 45 + 110 * np.exp(-t / 0.045)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.001, 0.22) + 0.3 * hp(rng.standard_normal(len(t)), 3000) * env(len(t), 0.0005, 0.006)
def snare():
    t = t_(0.35)
    return 0.6 * bp(rng.standard_normal(len(t)), 900, 7000) * env(len(t), 0.001, 0.11) + 0.5 * np.sin(2 * np.pi * 190 * t) * env(len(t), 0.001, 0.06)
def hat(open_=False):
    t = t_(0.3 if open_ else 0.06)
    return 0.35 * hp(rng.standard_normal(len(t)), 7000) * env(len(t), 0.0005, 0.09 if open_ else 0.018)
def crash():
    t = t_(2.5); return 0.4 * hp(rng.standard_normal(len(t)), 4000) * env(len(t), 0.001, 0.7)
def impact():
    t = t_(3.0)
    boom = np.sin(2 * np.pi * np.cumsum(30 + 70 * np.exp(-t / 0.12)) / SR) * env(len(t), 0.001, 0.9)
    crack = lp(rng.standard_normal(len(t)), 2500) * env(len(t), 0.001, 0.25)
    return np.tanh(1.6 * (boom + 0.6 * crack))
def riser(sec):
    t = t_(sec); u = t / sec; x = np.zeros(len(t))
    noise = rng.standard_normal(len(t))
    for k in range(8):   # a bandpass that climbs, in 8 segments
        a, b = int(len(t) * k / 8), int(len(t) * (k + 1) / 8); f = 300 * 2 ** (5 * (k + 0.5) / 8)
        x[a:b] = bp(noise, f * 0.7, min(f * 1.4, 18000))[a:b]
    sweep = np.sin(2 * np.pi * np.cumsum(200 * 2 ** (3 * u)) / SR)
    return (0.5 * x + 0.15 * sweep) * u ** 2
def whoosh():
    t = t_(0.5); u = t / 0.5; noise = rng.standard_normal(len(t))
    x = 0.5 * bp(noise, 400, 2000) * (u < 0.5) + 0.5 * bp(noise, 1500, 6000) * (u >= 0.5)
    return x * np.sin(np.pi * u) ** 2
def crowd(sec):
    t = t_(sec); u = t / sec
    x = bp(rng.standard_normal(len(t)), 300, 2500) + 0.4 * bp(rng.standard_normal(len(t)), 2500, 6000)
    wob = 1 + 0.25 * np.sin(2 * np.pi * 0.7 * t) * np.sin(2 * np.pi * 0.23 * t)
    return 0.35 * x * wob * np.minimum(1, u / 0.08) * np.minimum(1, (1 - u) / 0.5)

KICK, SNARE, HAT, OHAT, CRASH = kick(), snare(), hat(), hat(True), crash()

# ---- harmony: F#m - D - E - C#m (anime rock), one chord a bar
PROG = [(54, [0, 3, 7]), (50, [0, 4, 7]), (52, [0, 4, 7]), (49, [0, 3, 7])]

def pad_bar(root, iv, dur, bright):
    t = t_(dur); x = np.zeros(len(t))
    for n in iv + [12]:
        for det in (-0.12, 0.0, 0.12):
            x += saw(midi(root + 12 + n + det), t + rng.random())
    x = lp(x, 800 + 3500 * bright) / 9
    return x * np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.05)
def bass_note(f, dur):
    t = t_(dur); x = 0.6 * saw(f, t) + 0.5 * np.sin(2 * np.pi * f / 2 * t)
    return lp(x, 900) * np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.01)
def lead_note(f, dur):
    t = t_(dur); x = 0.5 * sq(f, t, 0.25) + 0.3 * saw(f * 2.003, t)
    return lp(x, 5000) * env(len(t), 0.002, dur * 0.8)

# sections in bars (1.6 s each): name, start bar, end bar
SECTIONS = [("hook", 0, 2), ("intro", 2, 6), ("grooveA", 6, 14), ("drop1", 14, 38), ("break", 38, 50),
            ("build", 50, 62), ("grooveB", 62, 70), ("drop2", 70, 82), ("outro", 82, 87)]
def section(bar):
    for name, a, b in SECTIONS:
        if a <= bar < b: return name, bar - a, b - a
    return "end", 0, 1

music = np.zeros((N, 2)); L = np.zeros(N); R = np.zeros(N); drums = np.zeros(N); side = np.ones(N)
total_bars = int(np.ceil(LEN / BAR))
for bar in range(total_bars):
    name, k, nb = section(bar)
    t0 = bar * BAR
    root, iv = PROG[bar % 4]
    full = name in ("hook", "drop1", "drop2")
    if name == "end": break
    # drums
    if name in ("hook", "drop1", "drop2", "grooveA", "grooveB"):
        for b in range(4):
            put(drums, KICK, t0 + b * BEAT, 1.0)
            if b in (1, 3): put(drums, SNARE, t0 + b * BEAT, 0.9)
            if full and b == 2: put(drums, KICK, t0 + (b + 0.5) * BEAT, 0.6)
            for h in range(4 if full else 2):
                put(drums, OHAT if (h == 2 and not full) else HAT, t0 + b * BEAT + h * BEAT / (4 if full else 2), 0.8 if h % 2 == 0 else 0.5)
            # sidechain: the pad and bass duck under every kick
            i = int((t0 + b * BEAT) * SR); n = int(0.25 * SR)
            side[i:i + n] = np.minimum(side[i:i + n], 0.35 + 0.65 * (np.arange(min(n, N - i)) / n) ** 0.6)
        if k == 0 and full: put(drums, CRASH, t0, 0.9)
    elif name == "intro":
        put(drums, KICK, t0, 0.9); put(drums, SNARE, t0 + 3 * BEAT, 0.6)
        for h in range(8): put(drums, HAT, t0 + h * BEAT / 2, 0.4)
    elif name == "build":
        div = 1 if k < 4 else 2 if k < 8 else 4 if k < 10 else 8   # snare roll accelerates into drop 2
        for s in range(4 * div): put(drums, SNARE, t0 + s * BEAT / div, 0.35 + 0.5 * (k / nb))
        put(drums, KICK, t0, 0.8)
    elif name == "outro" and k == 0:
        put(drums, KICK, t0, 1.0); put(drums, CRASH, t0, 1.0)
    # pad
    bright = {"hook": 1, "drop1": 1, "drop2": 1, "grooveA": 0.5, "grooveB": 0.6, "intro": 0.25, "break": 0.15, "build": 0.2 + 0.8 * k / nb, "outro": 0.3}[name]
    p = pad_bar(root, iv, BAR, bright) * (0.55 if name != "break" else 0.7)
    if name == "outro": p *= np.exp(-(k * BAR + t_(BAR)) / 4.0)   # the end card rings out over the last bars
    put(L, p, t0); put(R, np.roll(p, 300), t0)
    # bass: driving eighths in the drops and grooves
    if name in ("hook", "drop1", "drop2", "grooveA", "grooveB", "build"):
        for e in range(8):
            f = midi(root - 12 + (12 if (full and e % 4 == 3) else 0))
            put(L, bass_note(f, BEAT / 2 * 0.9) * 0.5, t0 + e * BEAT / 2); put(R, bass_note(f, BEAT / 2 * 0.9) * 0.5, t0 + e * BEAT / 2)
    # lead: 16th arp in the drops, a slow arp in the break
    if full or name == "break":
        notes = [root + 24 + n for n in iv] + [root + 36]
        step = BEAT / 4 if full else BEAT
        for s in range(int(BAR / step)):
            n = notes[[0, 1, 2, 3, 2, 1][s % 6] if full else s % 4]
            x = lead_note(midi(n), step * (0.9 if full else 1.8)) * (0.22 if full else 0.3)
            put(L, x, t0 + s * step); put(R, np.roll(x, 600), t0 + s * step)

# risers into the drops, impacts on them
for bar_at, bars in ((2, 2), (14, 2), (70, 4)):
    put(L, riser(bars * BAR) * 0.5, (bar_at - bars) * BAR if bar_at - bars >= 0 else 0)
    put(R, riser(bars * BAR) * 0.5, (bar_at - bars) * BAR if bar_at - bars >= 0 else 0)
IMP = impact()
for at in (0.0, 14 * BAR, 70 * BAR, 82 * BAR):
    put(drums, IMP, at, 0.9)

# mix: sidechain, a short room reverb on the music, drums dry-ish
L *= side; R *= side
ir = rng.standard_normal(int(SR * 1.2)) * np.exp(-np.arange(int(SR * 1.2)) / SR / 0.35); ir /= np.abs(ir).sum() ** 0.5 * 30
wetL, wetR = fftconvolve(L, ir)[:N], fftconvolve(R, np.roll(ir, 113))[:N]
music[:, 0] = L + 0.6 * wetL + drums; music[:, 1] = R + 0.6 * wetR + drums
music[-int(SR * 1.5):] *= np.linspace(1, 0, int(SR * 1.5))[:, None]   # tail fade
music = np.tanh(1.3 * music / np.abs(music).max()) ; music *= 0.89 / np.abs(music).max()

os.makedirs(OUT, exist_ok=True)
def save(name, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1: x = np.stack([x, x], 1)
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    wavfile.write(os.path.join(OUT, name), SR, (x * 32767).astype(np.int16))
save("music.wav", music)
save("whoosh.wav", whoosh()); save("impact.wav", IMP); save("crowd.wav", crowd(6.0)); save("riser.wav", riser(2 * BAR))
print("wrote", OUT, f"{LEN}s at {BPM} BPM")
