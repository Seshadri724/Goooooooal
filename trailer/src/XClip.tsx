import {
  AbsoluteFill,
  Easing,
  Sequence,
  Series,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio, Video } from "@remotion/media";
import { FIGHTERS, FLAME, Flash, GOLD, Kicker, Logo, STONE, Vignette, dela, mono } from "./Trailer";

// 139.2 s gameplay clip for X (87 bars: under the 2:20 cap for accounts without Premium).
// Footage: public/raw/*.mp4, recorded from the live game by capture.mjs (1920x1080, 30 fps,
// already cropped to the pitch). Music: public/audio/music.wav from gen_audio.py at 150 BPM, so a beat is 12 frames and a
// bar is 48: every scene below lasts a whole number of bars and every cut lands on a downbeat.
export const BAR = 48;
const TEAL = "#35d6c0";
const ICE = "#7fd0ff";

// A cut from a raw recording: `from` is the source second; `push` slowly zooms in; `rate` < 1 is slow motion.
const Raw: React.FC<{
  src: string;
  from: number;
  push?: number;
  dim?: number;
  blur?: number;
  rate?: number;
  zoom?: number;
}> = ({ src, from, push = 0.06, dim = 1, blur = 0, rate = 1, zoom = 1 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#05070e" }}>
      <AbsoluteFill
        style={{
          scale: interpolate(frame, [0, durationInFrames], [zoom, zoom * (1 + push)], { extrapolateRight: "clamp" }),
        }}
      >
        <Video
          src={staticFile(`raw/${src}.mp4`)}
          trimBefore={Math.round(from * fps)}
          playbackRate={rate}
          muted
          premountFor={fps}
          style={{ width: "100%", height: "100%", filter: `brightness(${dim}) blur(${blur}px)` }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Centre slam: huge text that lands from 2.4x with a shake, for the hook and the big beats.
const Slam: React.FC<{ text: string; sub?: string; color: string; delay?: number }> = ({ text, sub, color, delay = 0 }) => {
  const frame = useCurrentFrame() - delay;
  const { fps } = useVideoConfig();
  const k = spring({ frame, fps, config: { damping: 12, stiffness: 220 } });
  const shake = frame >= 0 && frame < 10 ? Math.sin(frame * 2.7) * (10 - frame) * 1.6 : 0;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 18, pointerEvents: "none" }}>
      <div
        style={{
          fontFamily: dela,
          fontSize: 150,
          lineHeight: 1,
          color: "#fff",
          textAlign: "center",
          textShadow: `7px 7px 0 ${color}, 0 0 60px rgba(0,0,0,.6)`,
          scale: String(interpolate(k, [0, 1], [2.4, 1])),
          opacity: interpolate(k, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
          translate: `${shake}px ${-shake * 0.6}px`,
          rotate: "-4deg",
        }}
      >
        {text}
      </div>
      {sub ? (
        <div
          style={{
            fontFamily: mono,
            fontWeight: 700,
            fontSize: 42,
            letterSpacing: "0.12em",
            color: GOLD,
            background: "rgba(5,7,14,.7)",
            padding: "8px 24px",
            opacity: interpolate(frame, [10, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        >
          {sub}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// Top-left label chip: camera names, engine names.
const Tag: React.FC<{ text: string; color: string; n?: string }> = ({ text, color, n }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ padding: "110px 72px", pointerEvents: "none" }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 18,
          width: "fit-content",
          translate: `${interpolate(frame, [0, 6], [-60, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) })}px 0`,
          opacity: interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {n ? (
          <span style={{ fontFamily: dela, fontSize: 64, color, textShadow: "4px 4px 0 rgba(0,0,0,.6)" }}>{n}</span>
        ) : null}
        <span
          style={{
            fontFamily: mono,
            fontWeight: 700,
            fontSize: 40,
            letterSpacing: "0.12em",
            color: "#05070e",
            background: color,
            padding: "6px 18px",
            transform: "skewX(-10deg)",
          }}
        >
          {text}
        </span>
      </div>
    </AbsoluteFill>
  );
};

// Persistent corner bug so a muted, mid-scroll viewer always knows what this is and where to play it.
const Bug: React.FC = () => (
  <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "flex-end", padding: "0 48px 40px", pointerEvents: "none" }}>
    <div style={{ fontFamily: mono, fontWeight: 700, fontSize: 28, color: "rgba(255,255,255,.85)", textShadow: "2px 2px 0 rgba(0,0,0,.7)" }}>
      ▶ PLAY FREE · blaze-game.onrender.com
    </div>
  </AbsoluteFill>
);

const sfx = (name: string, volume = 1) => <Audio src={staticFile(`audio/${name}.wav`)} volume={volume} />;

const RosterCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ padding: "90px 140px", justifyContent: "center", gap: 18 }}>
      <div style={{ fontFamily: mono, fontWeight: 700, fontSize: 44, letterSpacing: "0.14em", color: GOLD, marginBottom: 6 }}>
        5 FIGHTERS · 3D RIGGED IN BLENDER
      </div>
      {FIGHTERS.map((f, i) => {
        const k = spring({ frame: frame - 6 - i * 6, fps, config: { damping: 15, stiffness: 150 } });
        return (
          <div
            key={f.name}
            style={{
              display: "flex",
              alignItems: "baseline",
              justifyContent: "space-between",
              borderBottom: `5px solid ${f.color}`,
              paddingBottom: 6,
              translate: `${interpolate(k, [0, 1], [-900, 0])}px 0`,
              opacity: k,
            }}
          >
            <span style={{ fontFamily: dela, fontSize: 104, lineHeight: 1.05, color: f.color }}>{f.name}</span>
            <span style={{ fontFamily: mono, fontWeight: 700, fontSize: 44, color: "#fff" }}>
              {f.elem} · {f.role}
            </span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const btn = spring({ frame: frame - 30, fps, config: { damping: 9, stiffness: 150 } });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 44 }}>
      <Logo size={150} />
      <div
        style={{
          fontFamily: dela,
          fontSize: 70,
          color: "#05070e",
          background: GOLD,
          padding: "22px 80px",
          transform: "skewX(-10deg)",
          boxShadow: "0 12px 0 #b39a1f",
          scale: String(btn * (1 + 0.04 * Math.sin(frame / 5))),
        }}
      >
        PLAY FREE NOW
      </div>
      <div
        style={{
          fontFamily: mono,
          fontWeight: 700,
          fontSize: 46,
          color: "#fff",
          opacity: interpolate(frame, [44, 58], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        blaze-game.onrender.com
      </div>
      <div
        style={{
          fontFamily: mono,
          fontWeight: 500,
          fontSize: 34,
          color: "#c9d2ea",
          opacity: interpolate(frame, [60, 74], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        No download · No sign-up · Online 1v1 with a friend
      </div>
    </AbsoluteFill>
  );
};

// Bottom-centre caption for muted autoplay: what the effect does, in one line.
const Caption: React.FC<{ text: string; color: string }> = ({ text, color }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 110, pointerEvents: "none" }}>
      <div
        style={{
          fontFamily: mono,
          fontWeight: 700,
          fontSize: 44,
          color: "#fff",
          background: "rgba(5,7,14,.78)",
          borderBottom: `6px solid ${color}`,
          padding: "12px 30px",
          opacity: interpolate(frame, [4, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          translate: `0 ${interpolate(frame, [4, 12], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) })}px`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// One special-shot cut of the montage. The game titles each special in its own cutscene, so this adds a numbered tag
// (the count builds the pace) and a caption, not a second name slam. A whoosh on the cut.
const Special: React.FC<{ src: string; from: number; n: string; name: string; note: string; color: string }> = ({ src, from, n, name, note, color }) => (
  <AbsoluteFill>
    <Raw src={src} from={from} push={0.08} />
    <Tag n={n} text={name} color={color} />
    <Caption text={note} color={color} />
    <Vignette />
    <Flash />
    {sfx("whoosh", 0.35)}
  </AbsoluteFill>
);

// One camera of the 12-camera tour: a numbered tag and a soft whoosh.
const Cam: React.FC<{ src: string; from: number; n: string; name: string }> = ({ src, from, n, name }) => (
  <AbsoluteFill>
    <Raw src={src} from={from} push={0.03} />
    <Tag n={n} text={name} color={TEAL} />
    <Vignette />
    {sfx("whoosh", 0.25)}
  </AbsoluteFill>
);

export const XClip: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#05070e" }}>
      <Audio src={staticFile("audio/music.wav")} />
      <Series>
        {/* ---- hook (2 bars): the most striking shot first, with the claim in one line */}
        <Series.Sequence name="Hook" durationInFrames={2 * BAR} premountFor={fps}>
          <Raw src="specials" from={83.9} push={0.12} />
          <Slam text="THE BALL IS A MISSILE." color={FLAME} />
          <Vignette />
          <Flash />
        </Series.Sequence>

        {/* ---- title (4 bars) */}
        <Series.Sequence name="Title" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="main" from={33} dim={0.35} blur={8} />
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 36 }}>
            <Logo size={160} />
            <div style={{ fontFamily: mono, fontWeight: 700, fontSize: 46, letterSpacing: "0.12em", color: GOLD }}>
              1v1 ANIME FOOTBALL · FREE IN YOUR BROWSER
            </div>
          </AbsoluteFill>
          <Vignette />
          <Flash />
          {sfx("impact", 0.6)}
        </Series.Sequence>

        {/* ---- the duel (8 bars) */}
        <Series.Sequence name="Time stops" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="main" from={44.5} />
          <Kicker text="TIME STOPS." sub="Run into them and every clash becomes a duel." color={FLAME} />
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="Elements" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="main" from={23.5} />
          <Kicker text="ELEMENTS DECIDE." sub="Flame › Gale › Stone › Flame. Advantage hits 20% harder." color={STONE} />
          <Vignette />
          <Flash />
        </Series.Sequence>

        {/* ---- special shots (24 bars, drop 1): 12 cuts of 2 bars */}
        <Series.Sequence name="Imperial Dragon" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="sari" from={2.6} n="01" name="IMPERIAL DRAGON" note="A dragon carries the ball in its jaws." color="#b06bff" />
        </Series.Sequence>
        <Series.Sequence name="Crimson Meteor" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={90.6} n="02" name="CRIMSON METEOR" note="Flame at full power." color={FLAME} />
        </Series.Sequence>
        <Series.Sequence name="Hellfire Missile" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={75.6} n="03" name="HELLFIRE MISSILE" note="Homing. No distance falloff." color={FLAME} />
        </Series.Sequence>
        <Series.Sequence name="Avalanche Snowball" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={35.6} n="04" name="AVALANCHE SNOWBALL" note="Flattens the keeper." color={ICE} />
        </Series.Sequence>
        <Series.Sequence name="Sword Storm" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={59.4} n="05" name="SWORD STORM" note="A fan of blades. Unblockable." color="#a7b4d6" />
        </Series.Sequence>
        <Series.Sequence name="Zigzag Comet" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={116.4} n="06" name="ZIGZAG COMET" note="Weaves past the defender." color={TEAL} />
        </Series.Sequence>
        <Series.Sequence name="Hydro Cannon" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="cams" from={10.6} n="07" name="HYDRO CANNON" note="The ball rides a water jet." color="#4dc3ff" />
        </Series.Sequence>
        <Series.Sequence name="Verdant Tempest" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="sari" from={30.4} n="08" name="VERDANT TEMPEST" note="A helix of magic leaves." color="#5be37a" />
        </Series.Sequence>
        <Series.Sequence name="Gatling Volley" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="cams" from={55.6} n="09" name="GATLING VOLLEY" note="A burst of brass slugs." color={GOLD} />
        </Series.Sequence>
        <Series.Sequence name="Thunderbolt Barrage" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="cams" from={1.8} n="10" name="THUNDERBOLT BARRAGE" note="Lightning strikes the keeper." color="#ffd84a" />
        </Series.Sequence>
        <Series.Sequence name="Titan Hands" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={66.8} n="11" name="TITAN HANDS" note="Keepers have specials too." color={GOLD} />
        </Series.Sequence>
        <Series.Sequence name="Bedrock Fortress" durationInFrames={2 * BAR} premountFor={fps}>
          <Special src="specials" from={78.8} n="12" name="BEDROCK FORTRESS" note="A stone wall rises from the pitch." color={STONE} />
        </Series.Sequence>

        {/* ---- breakdown (12 bars): the cast */}
        <Series.Sequence name="Roster" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="sari" from={10} dim={0.28} blur={10} />
          <RosterCard />
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="Full 3D" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="sari" from={9} push={0.1} />
          <Kicker text="FULL 3D." sub="Every fighter rigged and animated in Blender." color={ICE} />
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="Keepers" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="main" from={27.4} />
          <Kicker text="KEEPERS FIGHT BACK." sub="Save duels: your move against theirs." color={STONE} />
          <Vignette />
          <Flash />
        </Series.Sequence>

        {/* ---- build (12 bars): 12 cameras, one bar each */}
        <Series.Sequence name="Cam broadcast" durationInFrames={BAR} premountFor={fps}>
          <Cam src="main" from={21} n="01" name="BROADCAST" />
        </Series.Sequence>
        <Series.Sequence name="Cam cinematic" durationInFrames={BAR} premountFor={fps}>
          <Cam src="main" from={41} n="02" name="CINEMATIC" />
        </Series.Sequence>
        <Series.Sequence name="Cam follow" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={13} n="03" name="FOLLOW" />
        </Series.Sequence>
        <Series.Sequence name="Cam over-the-shoulder" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={18} n="04" name="OVER-THE-SHOULDER" />
        </Series.Sequence>
        <Series.Sequence name="Cam orbit" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={22.2} n="05" name="ORBIT" />
        </Series.Sequence>
        <Series.Sequence name="Cam first-person" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={27.6} n="06" name="FIRST-PERSON" />
        </Series.Sequence>
        <Series.Sequence name="Cam helmet" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={33.1} n="07" name="HELMET HUD" />
        </Series.Sequence>
        <Series.Sequence name="Cam cockpit" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={39} n="08" name="COCKPIT" />
        </Series.Sequence>
        <Series.Sequence name="Cam fixed" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={44.2} n="09" name="FIXED ANGLES" />
        </Series.Sequence>
        <Series.Sequence name="Cam isometric" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={49.6} n="10" name="ISOMETRIC" />
        </Series.Sequence>
        <Series.Sequence name="Cam top-down" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={57.9} n="11" name="TOP-DOWN" />
        </Series.Sequence>
        <Series.Sequence name="Cam CCTV" durationInFrames={BAR} premountFor={fps}>
          <Cam src="cams" from={63} n="12" name="CCTV" />
        </Series.Sequence>

        {/* ---- groove (8 bars): one match, three engines */}
        <Series.Sequence name="12-bit" durationInFrames={3 * BAR} premountFor={fps}>
          <Raw src="modes" from={1.2} push={0.04} />
          <Tag text="12-BIT RETRO" color={FLAME} />
          <Kicker text="3 ENGINES. 1 GAME." sub="Switch any time, mid-match." color={GOLD} />
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="32-bit" durationInFrames={3 * BAR} premountFor={fps}>
          <Raw src="modes" from={12.6} push={0.04} />
          <Tag text="32-BIT ARCADE" color={GOLD} />
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="HD 3D" durationInFrames={2 * BAR} premountFor={fps}>
          <Raw src="modes" from={24.6} push={0.06} />
          <Tag text="HD 3D" color={TEAL} />
          <Vignette />
          <Flash />
        </Series.Sequence>

        {/* ---- drop 2 (12 bars): goals */}
        <Series.Sequence name="Hydro goal" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="main" from={82} push={0.08} />
          <Sequence from={124} premountFor={fps}>
            {sfx("crowd", 0.7)}
          </Sequence>
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="Replay" durationInFrames={2 * BAR} premountFor={fps}>
          <Raw src="main" from={85} rate={0.5} push={0.1} />
          <Tag text="SLOW-MO REPLAY" color={GOLD} />
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="Some goal" durationInFrames={4 * BAR} premountFor={fps}>
          <Raw src="main" from={30.6} push={0.06} />
          <Kicker text="FIRST TO 3." sub="Every goal gets its own celebration." color={STONE} />
          <Sequence from={40} premountFor={fps}>
            {sfx("crowd", 0.6)}
          </Sequence>
          <Vignette />
          <Flash />
        </Series.Sequence>
        <Series.Sequence name="Thunder goal" durationInFrames={2 * BAR} premountFor={fps}>
          <Raw src="cams" from={4.8} push={0.08} />
          <Vignette />
          <Flash />
          {sfx("impact", 0.5)}
        </Series.Sequence>

        {/* ---- outro (5 bars): the ask */}
        <Series.Sequence name="End card" durationInFrames={5 * BAR} premountFor={fps}>
          <Raw src="main" from={87} dim={0.22} blur={16} push={0.04} />
          <EndCard />
          <Vignette />
          <Flash />
        </Series.Sequence>
      </Series>
      <Sequence from={6 * BAR} durationInFrames={76 * BAR} premountFor={fps}>
        <Bug />
      </Sequence>
    </AbsoluteFill>
  );
};

