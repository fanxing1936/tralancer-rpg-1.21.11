# Phase 2 material integration

This extension implements the source-backed default Jungle Abomination material, including the base `NaturalEmissive` contribution and the B-channel pink pulse. It is opt-in for this model. It does not change phase 1 assets or vanilla branch statements.

## Executable components

- `_tools/dungeons_conversion/materials.py`: isolated atlas/shader preparation, p2 item model and item definition postprocessing, phase marker contract, numeric reference.
- `lucifer_p2_material.js`: Blockbench single-atlas material preview, time controls, and four-eye affine animation preview.
- Generated `material_contract.json`: exact colors, reserved tint slots, eight pulse parts, original/derived hashes and numeric bounds.
- Generated `rp/assets/minecraft/shaders/core/rendertype_item_entity_translucent_cull.vsh/.fsh`: actual 1.21.11 paper item_display shader override. No `entity_cutout` shader is changed.

Example preparation (an isolated output directory is required):

```powershell
python _tools/dungeons_conversion/materials.py --out D:/agent/dungeons_extract/phase2_material_runtime --client-jar D:/minecraft/cyclone_mod_final/tmp/gradle-home/caches/fabric-loom/1.21.11/minecraft-client.jar
```

The caller copies the resulting atlas into its own opt-in p2 build. For each generated p2 Java part model, use `configure_part_model(model)`; it returns a copy and a face count. For each p2 item definition use `configure_item_definition(item)`. No API edits its input object. All p2 elements explicitly use `light_emission:0, shade:true` so source emission is not doubled by vanilla full-bright lightmaps. Geometry and face UV/rotation remain identical.

## Atlas and identification

The 4096² atlas retains its reference, nonglow and glow quadrants pixel-for-pixel. Its previously empty bottom-right 2048² quadrant receives exact nearest-sampled original `_E.B`, encoded as `[19,237,B,255]`. R/G/A provide the data guard; opaque alpha prevents a browser Canvas premultiply/unpremultiply round trip from rounding the B byte. The original complete `_E` RGBA PNG remains untouched; the derived quadrant intentionally carries only the B channel needed by the verified default material. All 51 triangle cutout tiles are rebuilt by the same source rasterizer; the corresponding rebuilt albedo must equal the entire 2048² reference atlas before auxiliary pixels are accepted. `_E.b` nonzero support must equal the existing alpha split.

Vertex tint marker slots are:

| Slot | Face layer | RGB | Integer |
| --- | --- | --- | --- |
| 0 | Existing ordinary item color convention | white initially | 16777215 |
| 1 | Nonglow | 37,211,0 | 2478848 |
| 2 | Glow | 38,211,phase | 2544384 + phase |

Initial `minecraft:custom_model_data.colors` is `[16777215,2478848,2544384]`. The phase is integer 0…199. It is reserved for this material; hurt coloring must not replace these slots. A separate entity outline can indicate damage.

Nonglow pixels sample auxiliary data at pixel offset `(0,2048)`, glow pixels at `(2048,0)`. These offsets are applied to `floor(UV * textureSize(Sampler0,0))`, so they are independent of the sprite's position in Minecraft's stitched atlas. A bounds test and the exact R/G/A guard precede entry into the material branch. Both samples use nearest LOD 0 to avoid mip mixtures crossing alpha or data partitions; this intentionally retains pixel detail but can alias at long distances.

The vertex shader calculates a separate lighting value from a white color input; it never divides by a marker or by zero color components. If tint or auxiliary data guard does not match, the fragment executes the original shader body. Removing exactly the inserted declaration/statement blocks restores the original vanilla source strings byte-for-byte; this is asserted during generation.

## Pulse clock and output mapping

This local 1.21.11 render pipeline registers DynamicTransforms, Projection, Fog and Lighting, but does not register Globals. Therefore adding a GameTime import would not supply a reliable time buffer. The data pack advances one global phase modulo 200 ticks and writes slot 2 on the eight `rpg.lu2.pulse` item_display parts. The other 94 parts need no phase update because their visible `_E.b` is zero. At 20 TPS this is a ten-second cycle; all bosses share the phase as the original global clock does. Server tick-rate changes affect wall-clock duration, and the original game's start phase is not recovered.

With A and S decoded to linear sampling values:

```text
pulse = max(sin(2π * phase/200)/3 + 2, 0)
C = [1, 0.13600000739097595, 0.9861199855804443]
E = 0.6000000238418579*A + S.b*10*pulse*(C*C)
linear_preview = A*vanilla_white_light + E
display = linear_to_sRGB(clamp(x*(2.51*x+0.03)/(x*(2.43*x+0.59)+0.14),0,1))
```

The bounded ACES fitted display curve is explicit and identical between the Java shader branch and Blockbench preview. It is a chosen HDR-to-screen presentation, not a claim of original UE exposure/Bloom equivalence. It retains ordinary Minecraft alpha clipping, ColorModulator and fog at the final display stage. It does not emit world light or add bloom.

The pulse is sampled once per server tick. Against a continuous ten-second sine, the worst sample-and-hold pulse error is at most `2π/(3*200)=0.01047198`, or 0.6284% of the minimum pulse value. Color-space conversion uses the standard sRGB default documented by the original asset parser; no live D3D SRV capture has been performed.

## Native Blockbench behavior

Load `lucifer_p2_material.js` before opening the generated preview/project. Activation requires both schema `dungeons-jungle-emissive-v1` and project name `lucifer_p2` or a `lucifer_p2_`/`lucifer_p2 ` prefix. `textures[0]` remains the sole texture; no material behavior is attached to other projects.

`LuciferP2Material.setTime(seconds)` freezes the material at a known time; `setTime(null)` restores the editor timeline or elapsed preview time. `setMode(0/1/2)` selects composite, emission-only, or raw linear HDR diagnostic output. Raw values need a float render target for validation; an ordinary screen framebuffer may clip them. `hdrSample(A,B,time)` supplies the corresponding numeric equation.

The plugin preserves `animations[].dungeons_affine_tracks` on native parse/compile. On `display_animation_frame`, only `p2_head_093` through `p2_head_096` can receive an affine override. The tracks transform absolute authored BB coordinates, while Blockbench group geometry is pivot-relative. The native target is therefore:

```text
desiredWorldMesh = Project.model_3d.matrixWorld * W_track * T(group.origin)
localMesh = inverse(actualParent.matrixWorld) * desiredWorldMesh
```

It assigns the temporary mesh matrix with `matrixAutoUpdate=false`; it never edits persistent origin/rotation or decomposes a singular closed-eyelid transform. Glow descendants inherit the parent. Default-pose, project-switch and unload handling restore automatic updates and the rest pose. Matrix samples use elementwise interpolation and clamp endpoints, matching the runtime affine track contract; blend-controller combinations are outside this preview extension.

## Verification and remaining boundary

The actual modified and original GL33 shaders were compiled, linked and rasterized in a hidden standalone NVIDIA context. There were 1040 positive samples covering all 200 phases plus bright/dark lighting, and 288 non-opt-in or marker-collision samples. The non-opt-in difference from the original shader was exactly zero. A full-size sprite moved to `(73,49)` inside a 4352² atlas retained correct auxiliary addressing. Maximum RGBA error against the independent CPU equation was `9.06283e-7`; no GL error occurred. This proves shader execution and sampled addressing, not a Minecraft client session.

An isolated native Blockbench project also executed the actual preview material in an RGBA32F framebuffer. Three times (0, 2.5 and 7.5 seconds) each covered 149 visible texture samples with exact alpha and maximum HDR component error `3.81470e-6`; peak HDR reached `19.61466`, so this comparison did not hide values above one through display clipping. The opaque auxiliary encoding preserves the original B bytes through the native Canvas texture loader.

All 18 native animation clips were sampled at 1,735 times, including source keys and intermediate times. The actual group/cube geometry uploaded to the GPU yielded 20,820 checked eye vertices: maximum world-position error was `1.24548e-6` internal model units (`1.24548e-5` after model scale 10); the independent CPU matrix comparison reached `8.93e-15`. A separate nonidentity Canvas transform fixture covered 4,032 vertices with GPU error `9.184e-7`. Synthetic singular eyelid transforms remained finite, native parse/compile preserved all affine tracks and material/scale metadata, and leaving animation preview restored matrix auto-updates without changing persistent group properties. These are native editor and GPU checks, not an in-game animation claim.

The shader override occupies a shared core-shader filename. Installing another resource pack or renderer that replaces the same shader can supersede it; integration must detect a conflicting existing override rather than silently overwrite it. No existing user game instance has been synchronized by this module. A separate vanilla 1.21.11 client in `phase2_client_test/game` subsequently loaded the complete RP and rendered fixed phase-50/150 screenshots: 795 selected model pixels became brighter at the peak and none darker, with RGB maxima `[3,20,4]`; the actual items atlas was 8192². Live walk and material-clock progression were also observed, but no continuous GIF/video was completed. The separate client report preserves startup warnings and initial full-pack tick lag; these visual checks are not a production performance pass. Third-party shader compatibility, original UE exposure comparison and complete in-game combat/outline interactions remain separate checks.
