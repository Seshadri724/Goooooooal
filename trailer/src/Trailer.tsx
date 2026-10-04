import {
  AbsoluteFill,
  Easing,
  Series,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
} from "remotion";
import { Video } from "@remotion/media";
import { loadFont as loadDela } from "@remotion/google-fonts/DelaGothicOne";
import { loadFont as loadMono } from "@remotion/google-fonts/AzeretMono";

const dela = loadDela().fontFamily;
const mono = loadMono("normal", { weights: ["500", "700"] }).fontFamily;

const FLAME = "#ff5a36";
const STONE = "#e0a93f";
const GOLD = "#ffe14d";

// The gameplay capture is the whole 1280x720 page. The game stage is the 1024x576 box at (128, 114); scaling by 1.875 puts
// exactly that box on a 1920x1080 frame (the page header and buttons fall outside it).
const Z = 1.875;

// A cut from the gameplay recording. `from` is the source time in seconds; the Series.Sequence around it sets the length.
const Clip: React.FC<{
  from: number;
  dim?: number;
  blur?: number;
  push?: number;
  duration: number;
}> = ({ from, dim = 1, blur = 0, push = 0.05, duration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#05070e" }}>
      <AbsoluteFill
        style={{
          scale: interpolate(frame, [0, duration], [1, 1 + push], {
            extrapolateRight: "clamp",
          }),
        }}
      >
        <Video
          src={staticFile("gameplay.mp4")}
          trimBefore={Math.round(from * fps)}
          muted
          premountFor={fps}
          style={{
            position: "absolute",
            width: 1280 * Z,
            height: 720 * Z,
            left: -128 * Z,
            top: -114 * Z,
            maxWidth: "none",
            filter: `brightness(${dim}) blur(${blur}px)`,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// A short white flash on every cut: the energy of an anime impact frame.
const Flash: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background: "#fff",
        opacity: interpolate(frame, [0, 5], [0.9, 0], {
          extrapolateRight: "clamp",
        }),
        pointerEvents: "none",
      }}
    />
  );
};

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)",
      pointerEvents: "none",
    }}
  />
);

// Lower-left headline over gameplay: a slanted slam with a coloured rule and a line of explanation.
const Kicker: React.FC<{ text: string; sub: string; color: string }> = ({
  text,
  sub,
  color,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = spring({ frame: frame - 6, fps, config: { damping: 14, stiffness: 140 } });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", padding: "0 100px 160px" }}>
      <div
        style={{
          translate: `${interpolate(k, [0, 1], [-160, 0])}px 0`,
          opacity: interpolate(k, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
          transform: "skewX(-10deg)",
          transformOrigin: "left bottom",
          width: "fit-content",
          background: "linear-gradient(90deg, rgba(5,7,14,.88), rgba(5,7,14,.55) 80%, rgba(5,7,14,0))",
          borderLeft: `10px solid ${color}`,
          padding: "20px 80px 22px 32px",
        }}
      >
        <div
          style={{
            fontFamily: dela,
            fontSize: 96,
            lineHeight: 1,
            color: "#fff",
            textShadow: `5px 5px 0 ${color}`,
            marginBottom: 12,
          }}
        >
          {text}
        </div>
        <div
          style={{
            fontFamily: mono,
            fontWeight: 500,
            fontSize: 38,
            color: "#e9edf8",
            opacity: interpolate(frame, [18, 30], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          {sub}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Logo: React.FC<{ size: number }> = ({ size }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = spring({ frame, fps, config: { damping: 11, stiffness: 160 } });
  const b = spring({ frame: frame - 5, fps, config: { damping: 11, stiffness: 160 } });
  const v = spring({ frame: frame - 10, fps, config: { damping: 14 } });
  return (
    <div
      style={{
        display: "flex",
        alignItems: "baseline",
        justifyContent: "center",
        gap: size * 0.2,
        fontFamily: dela,
        fontSize: size,
        lineHeight: 1,
      }}
    >
      <span
        style={{
          color: FLAME,
          translate: `${interpolate(a, [0, 1], [-700, 0])}px 0`,
          opacity: a,
        }}
      >
        Blaze
      </span>
      <span
        style={{
          color: "#fff",
          fontSize: size * 0.34,
          scale: String(interpolate(v, [0, 1], [3, 1])),
          opacity: v,
        }}
      >
        vs
      </span>
      <span
        style={{
          color: STONE,
          translate: `${interpolate(b, [0, 1], [700, 0])}px 0`,
          opacity: b,
        }}
      >
        Bedrock
      </span>
    </div>
  );
};

const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Clip from={29} dim={0.32} blur={8} duration={90} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 36 }}>
        <Logo size={150} />
        <div
          style={{
            fontFamily: mono,
            fontWeight: 700,
            fontSize: 44,
            letterSpacing: "0.14em",
            color: GOLD,
            opacity: interpolate(frame, [30, 44], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          ANIME FOOTBALL DUELS
        </div>
      </AbsoluteFill>
      <Vignette />
      <Flash />
    </AbsoluteFill>
  );
};

type Fighter = { name: string; elem: string; role: string; color: string };
const FIGHTERS: Fighter[] = [
  { name: "HARU", elem: "FLAME", role: "STRIKER", color: "#ff5a36" },
  { name: "JIN", elem: "STONE", role: "LIBERO", color: "#e0a93f" },
  { name: "RAIJIN", elem: "THUNDER", role: "WINGER", color: "#ffd84a" },
  { name: "FUBUKI", elem: "FROST", role: "MIDFIELDER", color: "#7fd0ff" },
  { name: "AOI", elem: "WATER", role: "PLAYMAKER", color: "#4dc3ff" },
];

const RosterScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Clip from={30} dim={0.28} blur={10} duration={105} />
      <AbsoluteFill style={{ padding: "90px 140px", justifyContent: "center", gap: 18 }}>
        <div
          style={{
            fontFamily: mono,
            fontWeight: 700,
            fontSize: 44,
            letterSpacing: "0.14em",
            color: GOLD,
            marginBottom: 6,
            opacity: interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          PICK YOUR FIGHTER
        </div>
        {FIGHTERS.map((f, i) => {
          const k = spring({ frame: frame - 8 - i * 6, fps, config: { damping: 15, stiffness: 150 } });
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
              <span style={{ fontFamily: dela, fontSize: 104, lineHeight: 1.05, color: f.color }}>
                {f.name}
              </span>
              <span style={{ fontFamily: mono, fontWeight: 700, fontSize: 44, color: "#fff" }}>
                {f.elem} · {f.role}
              </span>
            </div>
          );
        })}
      </AbsoluteFill>
      <Vignette />
      <Flash />
    </AbsoluteFill>
  );
};

const Stat: React.FC<{ n: number; label: string; color: string; delay: number }> = ({
  n,
  label,
  color,
  delay,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = spring({ frame: frame - delay, fps, config: { damping: 16, stiffness: 120 } });
  const v = interpolate(frame, [delay, delay + 28], [0, n], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div style={{ textAlign: "center", opacity: k, translate: `0 ${interpolate(k, [0, 1], [60, 0])}px` }}>
      <div style={{ fontFamily: dela, fontSize: 260, lineHeight: 1, color, textShadow: "6px 6px 0 rgba(0,0,0,.6)" }}>
        {Math.round(v)}
      </div>
      <div style={{ fontFamily: mono, fontWeight: 700, fontSize: 44, letterSpacing: "0.1em", color: "#fff", marginTop: 8 }}>
        {label}
      </div>
    </div>
  );
};

const StatsScene: React.FC = () => (
  <AbsoluteFill>
    <Clip from={72} dim={0.3} blur={6} duration={90} />
    <AbsoluteFill style={{ flexDirection: "row", justifyContent: "space-around", alignItems: "center", padding: "0 100px" }}>
      <Stat n={11} label="ELEMENTS" color={FLAME} delay={4} />
      <Stat n={16} label="SIGNATURE SHOTS" color={GOLD} delay={14} />
      <Stat n={4} label="RENDER MODES" color="#4dc3ff" delay={24} />
    </AbsoluteFill>
    <Vignette />
    <Flash />
  </AbsoluteFill>
);

const EndScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const btn = spring({ frame: frame - 40, fps, config: { damping: 9, stiffness: 150 } });
  const pulse = 1 + 0.04 * Math.sin(frame / 5);
  return (
    <AbsoluteFill>
      <Clip from={31} dim={0.3} blur={8} duration={120} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <Logo size={140} />
        <div
          style={{
            fontFamily: dela,
            fontSize: 64,
            color: "#05070e",
            background: GOLD,
            padding: "22px 80px",
            transform: "skewX(-10deg)",
            boxShadow: "0 12px 0 #b39a1f",
            scale: String(interpolate(btn, [0, 1], [0, 1]) * pulse),
          }}
        >
          Kick off
        </div>
        <div
          style={{
            fontFamily: mono,
            fontWeight: 500,
            fontSize: 38,
            color: "#e9edf8",
            opacity: interpolate(frame, [54, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        >
          First to 3 goals · plays in your browser
        </div>
      </AbsoluteFill>
      <Vignette />
      <AbsoluteFill
        style={{
          background: "#000",
          opacity: interpolate(frame, [102, 120], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      />
    </AbsoluteFill>
  );
};

// One gameplay scene: the cut, a kicker line (optional), the flash and vignette.
const Gameplay: React.FC<{
  from: number;
  duration: number;
  kicker?: { text: string; sub: string; color: string };
}> = ({ from, duration, kicker }) => (
  <AbsoluteFill>
    <Clip from={from} duration={duration} />
    {kicker ? <Kicker {...kicker} /> : null}
    <Vignette />
    <Flash />
  </AbsoluteFill>
);

export const Trailer: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      <Series.Sequence name="Title" durationInFrames={90} premountFor={fps}>
        <TitleScene />
      </Series.Sequence>
      <Series.Sequence name="Time stops" durationInFrames={90} premountFor={fps}>
        <Gameplay from={48.7} duration={90} kicker={{ text: "TIME STOPS.", sub: "Every clash is a duel. Pick your move.", color: FLAME }} />
      </Series.Sequence>
      <Series.Sequence name="Elements clash" durationInFrames={96} premountFor={fps}>
        <Gameplay from={88} duration={96} kicker={{ text: "ELEMENTS CLASH.", sub: "Flame beats Gale beats Stone beats Flame.", color: STONE }} />
      </Series.Sequence>
      <Series.Sequence name="Crimson Meteor" durationInFrames={90} premountFor={fps}>
        <Gameplay from={84.9} duration={90} kicker={{ text: "SIGNATURE SHOTS.", sub: "16 of them, each with its own camera.", color: FLAME }} />
      </Series.Sequence>
      <Series.Sequence name="Tectonic Hammer" durationInFrames={135} premountFor={fps}>
        <Gameplay from={18.9} duration={135} />
      </Series.Sequence>
      <Series.Sequence name="Keeper duel" durationInFrames={75} premountFor={fps}>
        <Gameplay from={72} duration={75} kicker={{ text: "KEEPER DUELS.", sub: "Save it or concede.", color: "#35d6c0" }} />
      </Series.Sequence>
      <Series.Sequence name="Goal" durationInFrames={96} premountFor={fps}>
        <Gameplay from={95.8} duration={96} />
      </Series.Sequence>
      <Series.Sequence name="Replay" durationInFrames={84} premountFor={fps}>
        <Gameplay from={99} duration={84} kicker={{ text: "SLOW-MO REPLAY.", sub: "Every goal gets its moment.", color: GOLD }} />
      </Series.Sequence>
      <Series.Sequence name="Fighters" durationInFrames={105} premountFor={fps}>
        <RosterScene />
      </Series.Sequence>
      <Series.Sequence name="Stats" durationInFrames={90} premountFor={fps}>
        <StatsScene />
      </Series.Sequence>
      <Series.Sequence name="End card" durationInFrames={120} premountFor={fps}>
        <EndScene />
      </Series.Sequence>
    </Series>
  );
};
