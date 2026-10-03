import { Composition } from "remotion";
import { Trailer } from "./Trailer";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Trailer"
      component={Trailer}
      durationInFrames={1071}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
