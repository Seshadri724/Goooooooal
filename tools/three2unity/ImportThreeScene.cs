// three2unity: builds a Unity scene from Assets/ThreeImport/scene.glb + scene.json. Menu: Three2Unity > Build Scene.
// Needs the glTFast package (com.unity.cloud.gltfast) so that scene.glb imports as a GameObject.
// Everything is created under one "ThreeSceneRoot" whose scale is the --scale you gave the CLI; run it again to rebuild.
using System;
using UnityEditor;
using UnityEditor.Animations;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;

namespace Three2Unity
{
    public static class ImportThreeScene
    {
        const string Dir = "Assets/ThreeImport/";
        const float AmbientScale = 0.5f; // three's hemisphere / ambient intensities run hotter than Unity's ambient
        const float LightScale = 1f;     // multiplies every imported light's intensity

        [Serializable] public class FogData { public bool on, exp; public string color = "#ffffff"; public float near, far, density; }
        [Serializable] public class CamData { public bool on, ortho; public float fov = 50, near = 0.1f, far = 1000, size; public float[] pos, rot; }
        [Serializable] public class LightData { public string name, type, color, ground; public float intensity, distance, angle, penumbra; public bool shadow; public float[] pos, dir; }
        [Serializable] public class TrackData { public string path; public float[] p, r, s, v; }
        [Serializable] public class CamTrack { public bool on; public float[] p, r, fov; }
        [Serializable] public class ClipData { public string name; public float[] times; public TrackData[] tracks; public CamTrack camera; }
        [Serializable]
        public class Data
        {
            public string flip = "x", background = "";
            public float scale = 1;
            public string[] hidden = new string[0];
            public FogData fog = new FogData();
            public CamData camera = new CamData();
            public LightData[] lights = new LightData[0];
            public ClipData[] clips = new ClipData[0];
        }

        // three is right-handed, Unity left-handed. The glTF importer mirrors one axis (X for glTFast); every position, direction
        // and rotation we add ourselves must be mirrored the same way or lights and camera end up on the wrong side.
        static bool flipZ;
        static Vector3 V(float x, float y, float z) => flipZ ? new Vector3(x, y, -z) : new Vector3(-x, y, z);
        static Vector3 V(float[] a, int i = 0) => V(a[i], a[i + 1], a[i + 2]);
        static Quaternion Q(float x, float y, float z, float w) => flipZ ? new Quaternion(-x, -y, z, w) : new Quaternion(x, -y, -z, w);
        static Color Col(string hex) { ColorUtility.TryParseHtmlString(hex, out var c); c.a = 1; return c; }

        static Transform Find(Transform inst, string path)
        {
            var t = inst.Find(path);
            if (t == null && inst.childCount == 1) t = inst.GetChild(0).Find(path); // some importers add a wrapper node
            return t;
        }

        [MenuItem("Three2Unity/Build Scene")]
        static void Build()
        {
            var json = AssetDatabase.LoadAssetAtPath<TextAsset>(Dir + "scene.json");
            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(Dir + "scene.glb");
            if (json == null) { EditorUtility.DisplayDialog("Three2Unity", "Assets/ThreeImport/scene.json not found. Run the three2unity CLI first.", "OK"); return; }
            if (prefab == null)
            {
                EditorUtility.DisplayDialog("Three2Unity", "scene.glb did not import as a GameObject.\nInstall glTFast: Window > Package Manager > + > Add package by name > com.unity.cloud.gltfast, then reimport scene.glb.", "OK");
                return;
            }
            var d = JsonUtility.FromJson<Data>(json.text);
            flipZ = d.flip == "z";

            var old = GameObject.Find("ThreeSceneRoot");
            if (old != null) Undo.DestroyObjectImmediate(old);
            var root = new GameObject("ThreeSceneRoot");
            Undo.RegisterCreatedObjectUndo(root, "Three2Unity");
            root.transform.localScale = Vector3.one * d.scale;
            var inst = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
            inst.name = "ThreeScene";
            inst.transform.SetParent(root.transform, false);

            int lost = 0;
            foreach (var h in d.hidden) { var t = Find(inst.transform, h); if (t != null) t.gameObject.SetActive(false); else lost++; }
            foreach (var L in d.lights) MakeLight(L, root.transform, d.scale);
            if (d.fog.on)
            {
                RenderSettings.fog = true; RenderSettings.fogColor = Col(d.fog.color);
                if (d.fog.exp) { RenderSettings.fogMode = FogMode.ExponentialSquared; RenderSettings.fogDensity = d.fog.density / d.scale; }
                else { RenderSettings.fogMode = FogMode.Linear; RenderSettings.fogStartDistance = d.fog.near * d.scale; RenderSettings.fogEndDistance = d.fog.far * d.scale; }
            }
            var (rig, cam) = MakeCamera(d, root.transform);
            lost += BuildClips(d, root, inst.transform, rig, cam);
            if (lost > 0) Debug.LogWarning($"Three2Unity: {lost} hidden / animated nodes were not found in the imported hierarchy (the importer may have renamed nodes); they were skipped.");

            Selection.activeGameObject = root;
            EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());
            Debug.Log($"Three2Unity: built {inst.GetComponentsInChildren<Transform>(true).Length} nodes, {d.lights.Length} lights, {d.clips.Length} clip(s). See Assets/ThreeImport/REPORT.md for what was left out.");
        }

        static void MakeLight(LightData L, Transform parent, float scale)
        {
            if (L.type == "HemisphereLight")
            {
                var sky = Col(L.color) * (L.intensity * AmbientScale); var ground = Col(L.ground) * (L.intensity * AmbientScale);
                RenderSettings.ambientMode = AmbientMode.Trilight;
                RenderSettings.ambientSkyColor = sky; RenderSettings.ambientGroundColor = ground; RenderSettings.ambientEquatorColor = Color.Lerp(sky, ground, 0.5f);
                return;
            }
            if (L.type == "AmbientLight") { RenderSettings.ambientMode = AmbientMode.Flat; RenderSettings.ambientLight = Col(L.color) * (L.intensity * AmbientScale); return; }

            var go = new GameObject(string.IsNullOrEmpty(L.name) ? L.type : L.name);
            go.transform.SetParent(parent, false);
            go.transform.localPosition = V(L.pos);
            var light = go.AddComponent<Light>();
            light.color = Col(L.color); light.intensity = L.intensity * LightScale; light.shadows = L.shadow ? LightShadows.Soft : LightShadows.None;
            if (L.type == "DirectionalLight") { light.type = LightType.Directional; go.transform.localRotation = Quaternion.LookRotation(V(L.dir)); }
            else if (L.type == "SpotLight")
            {
                light.type = LightType.Spot; light.spotAngle = L.angle * 2; light.innerSpotAngle = light.spotAngle * (1 - L.penumbra);
                if (L.distance > 0) light.range = L.distance * scale;
                go.transform.localRotation = Quaternion.LookRotation(V(L.dir));
            }
            else if (L.type == "PointLight") { light.type = LightType.Point; if (L.distance > 0) light.range = L.distance * scale; }
            else { Debug.LogWarning("Three2Unity: unsupported light type " + L.type); UnityEngine.Object.DestroyImmediate(go); }
        }

        // three cameras look down -Z, Unity cameras down +Z. The rig gets the same mirrored transform as every other node. With X mirrored
        // its -Z is three's view direction, so the Camera child turns 180 degrees about Y to look along it; with Z mirrored +Z already is.
        static (GameObject rig, GameObject cam) MakeCamera(Data d, Transform parent)
        {
            var c = d.camera;
            if (!c.on) { Debug.LogWarning("Three2Unity: no camera was found in the page; add one by hand."); return (null, null); }
            var existing = GameObject.FindWithTag("MainCamera");
            if (existing != null) existing.SetActive(false); // one listener, one main camera
            var rig = new GameObject("Camera Rig");
            rig.transform.SetParent(parent, false);
            rig.transform.localPosition = V(c.pos); rig.transform.localRotation = Q(c.rot[0], c.rot[1], c.rot[2], c.rot[3]);
            var go = new GameObject("Main Camera") { tag = "MainCamera" };
            go.transform.SetParent(rig.transform, false);
            go.transform.localRotation = flipZ ? Quaternion.identity : Quaternion.Euler(0, 180, 0);
            var cam = go.AddComponent<Camera>(); go.AddComponent<AudioListener>();
            cam.nearClipPlane = c.near * d.scale; cam.farClipPlane = c.far * d.scale; // clip planes are world units, not affected by the parent's scale
            if (c.ortho) { cam.orthographic = true; cam.orthographicSize = c.size * d.scale; } else cam.fieldOfView = c.fov;
            if (!string.IsNullOrEmpty(d.background)) { cam.clearFlags = CameraClearFlags.SolidColor; cam.backgroundColor = Col(d.background); }
            return (rig, go);
        }

        static int BuildClips(Data d, GameObject root, Transform inst, GameObject rig, GameObject cam)
        {
            int lost = 0;
            if (d.clips.Length == 0) return 0;
            if (!AssetDatabase.IsValidFolder(Dir + "Clips")) AssetDatabase.CreateFolder("Assets/ThreeImport", "Clips");
            AssetDatabase.DeleteAsset(Dir + "Clips/ThreeScene.controller");
            AnimatorController ctrl = null;
            foreach (var c in d.clips)
            {
                var clip = new AnimationClip { name = c.name, frameRate = 30 };
                var n = c.times.Length;
                foreach (var tr in c.tracks)
                {
                    var t = Find(inst, tr.path); if (t == null) { lost++; continue; }
                    var path = AnimationUtility.CalculateTransformPath(t, root.transform);
                    if (tr.p.Length == n * 3) Vec(clip, path, "localPosition", c.times, i => V(tr.p, i * 3));
                    if (tr.s.Length == n * 3) Vec(clip, path, "localScale", c.times, i => new Vector3(tr.s[i * 3], tr.s[i * 3 + 1], tr.s[i * 3 + 2]));
                    if (tr.r.Length == n * 4)
                    {
                        var q = new Quaternion[n]; for (int i = 0; i < n; i++) q[i] = Q(tr.r[i * 4], tr.r[i * 4 + 1], tr.r[i * 4 + 2], tr.r[i * 4 + 3]);
                        Set(clip, path, typeof(Transform), "localRotation.x", c.times, i => q[i].x); Set(clip, path, typeof(Transform), "localRotation.y", c.times, i => q[i].y);
                        Set(clip, path, typeof(Transform), "localRotation.z", c.times, i => q[i].z); Set(clip, path, typeof(Transform), "localRotation.w", c.times, i => q[i].w);
                    }
                    if (tr.v.Length == n) Set(clip, path, typeof(GameObject), "m_IsActive", c.times, i => tr.v[i], true);
                }
                if (rig != null && c.camera != null && c.camera.on && c.camera.p.Length == n * 3)
                {
                    var path = AnimationUtility.CalculateTransformPath(rig.transform, root.transform);
                    var k = c.camera;
                    Vec(clip, path, "localPosition", c.times, i => V(k.p, i * 3));
                    var q = new Quaternion[n]; for (int i = 0; i < n; i++) q[i] = Q(k.r[i * 4], k.r[i * 4 + 1], k.r[i * 4 + 2], k.r[i * 4 + 3]);
                    Set(clip, path, typeof(Transform), "localRotation.x", c.times, i => q[i].x); Set(clip, path, typeof(Transform), "localRotation.y", c.times, i => q[i].y);
                    Set(clip, path, typeof(Transform), "localRotation.z", c.times, i => q[i].z); Set(clip, path, typeof(Transform), "localRotation.w", c.times, i => q[i].w);
                    if (!d.camera.ortho) Set(clip, AnimationUtility.CalculateTransformPath(cam.transform, root.transform), typeof(Camera), "field of view", c.times, i => k.fov[i]);
                }
                var settings = AnimationUtility.GetAnimationClipSettings(clip); settings.loopTime = true; AnimationUtility.SetAnimationClipSettings(clip, settings);
                var file = Dir + "Clips/" + c.name + ".anim";
                AssetDatabase.DeleteAsset(file);
                AssetDatabase.CreateAsset(clip, file);
                if (ctrl == null) ctrl = AnimatorController.CreateAnimatorControllerAtPathWithClip(Dir + "Clips/ThreeScene.controller", clip);
                else ctrl.AddMotion(clip);
            }
            var anim = root.GetComponent<Animator>() ?? root.AddComponent<Animator>();
            anim.runtimeAnimatorController = ctrl; anim.applyRootMotion = false;
            return lost;
        }

        static void Vec(AnimationClip clip, string path, string prop, float[] times, Func<int, Vector3> v)
        {
            Set(clip, path, typeof(Transform), prop + ".x", times, i => v(i).x);
            Set(clip, path, typeof(Transform), prop + ".y", times, i => v(i).y);
            Set(clip, path, typeof(Transform), prop + ".z", times, i => v(i).z);
        }

        // Linear keys: each key's tangents are the slopes to its neighbours, so the Hermite curve is exactly the recorded polyline.
        // step = holds the value until the next key (visibility).
        static void Set(AnimationClip clip, string path, Type type, string prop, float[] times, Func<int, float> value, bool step = false)
        {
            var keys = new Keyframe[times.Length];
            for (int i = 0; i < keys.Length; i++) keys[i] = new Keyframe(times[i], value(i));
            for (int i = 0; i < keys.Length; i++)
            {
                if (step) { keys[i].inTangent = keys[i].outTangent = float.PositiveInfinity; continue; }
                float dIn = i > 0 ? Slope(keys[i - 1], keys[i]) : 0, dOut = i < keys.Length - 1 ? Slope(keys[i], keys[i + 1]) : dIn;
                keys[i].inTangent = i > 0 ? dIn : dOut; keys[i].outTangent = dOut;
            }
            clip.SetCurve(path, type, prop, new AnimationCurve(keys));
        }
        static float Slope(Keyframe a, Keyframe b) => (b.value - a.value) / Mathf.Max(1e-5f, b.time - a.time);
    }
}
