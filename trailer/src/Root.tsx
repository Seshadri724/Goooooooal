import { Composition } from "remotion";
import { Trailer } from "./Trailer";
import { BAR, XClip } from "./XClip";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Trailer"
        component={Trailer}
        durationInFrames={1071}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="XClip"
        component={XClip}
        durationInFrames={87 * BAR}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
