(function () {
    'use strict';
    const schema = 'dungeons-jungle-emissive-v1';
    const touched = new Map();
    const affineTouched = new Map();
    const subscriptions = [];
    const eventSubscriptions = [];
    let timer = null;
    let frozenTime = null;
    let started = performance.now();
    function isP2(project = Project) {
        return project?.dungeons_material_source?.schema === schema && /^lucifer_p2(?:$|[_ ])/.test(project.name);
    }

    function restoreAffine(project = null) {
        for (const [group, saved] of affineTouched) {
            if (project && saved.project !== project) continue;
            const mesh = saved.mesh;
            if (mesh) {
                mesh.matrixAutoUpdate = saved.auto;
                if (mesh.fix_position) mesh.position.copy(mesh.fix_position);
                if (mesh.fix_rotation) mesh.rotation.copy(mesh.fix_rotation);
                mesh.scale.set(1, 1, 1);
                mesh.updateMatrix(); mesh.updateMatrixWorld(true);
            }
            affineTouched.delete(group);
        }
    }

    function sampleAffine(track, seconds) {
        if (!Array.isArray(track) || !track.length) return null;
        let left = 0, right = track.length - 1;
        if (seconds <= track[0][0]) return track[0][1];
        if (seconds >= track[right][0]) return track[right][1];
        while (right - left > 1) {
            const middle = (left + right) >> 1;
            if (track[middle][0] <= seconds) left = middle; else right = middle;
        }
        const f = (seconds - track[left][0]) / (track[right][0] - track[left][0]);
        return track[left][1].map((row, i) => row.map((v, j) => v + (track[right][1][i][j] - v) * f));
    }

    function applyAffine() {
        if (!isP2() || !Animator.open || !Animation.selected) { restoreAffine(); return false; }
        const tracks = Animation.selected.dungeons_affine_tracks;
        if (!tracks) { restoreAffine(Project); return false; }
        const project = Project;
        project.model_3d.updateWorldMatrix(true, true);
        for (const [name, track] of Object.entries(tracks)) {
            if (!/^p2_head_09[3-6]$/.test(name)) continue;
            const group = project.groups.find(g => g.name === name);
            const matrix = sampleAffine(track, Timeline.time);
            if (!group?.mesh?.parent || !matrix || matrix.flat().some(v => !Number.isFinite(v))) continue;
            const mesh = group.mesh;
            if (!affineTouched.has(group)) affineTouched.set(group, {project, mesh, auto: mesh.matrixAutoUpdate});
            // Tracks act on authored absolute BB coordinates. Native group
            // geometry is pivot-relative: worldMesh = modelRoot * W * T(pivot).
            // Use the actual modelRoot matrix to retain Canvas/display transforms.
            const world = new THREE.Matrix4().set(...matrix.flat());
            world.multiply(new THREE.Matrix4().makeTranslation(...group.origin));
            world.premultiply(project.model_3d.matrixWorld);
            mesh.parent.updateWorldMatrix(true, false);
            if (Math.abs(mesh.parent.matrixWorld.determinant()) < 1e-12) throw new Error('p2 affine parent is singular');
            const local = mesh.parent.matrixWorld.clone().invert().multiply(world);
            mesh.matrixAutoUpdate = false;
            mesh.matrix.copy(local); mesh.matrixWorldNeedsUpdate = true;
            // No TRS decomposition: fully closed eyelids may be rank deficient.
            mesh.updateMatrixWorld(true);
        }
        return true;
    }

    function importAffine(animations) {
        if (!isP2()) return 0;
        let count = 0;
        for (const raw of animations || []) {
            const target = Animation.all.find(a => a.uuid === raw.uuid || a.name === raw.name);
            if (target && raw.dungeons_affine_tracks) {
                target.dungeons_affine_tracks = structuredClone(raw.dungeons_affine_tracks); count++;
            }
        }
        return count;
    }
    const fragment = `
#ifdef GL_ES
precision highp float;
#endif
#include <common>
#include <clipping_planes_pars_fragment>
uniform sampler2D map;
uniform float lrp2Time;
uniform float lrp2FlipY;
uniform float lrp2Mode;
uniform float lrp2EmissionEnabled;
uniform bool SHADE;
uniform bool EMISSIVE;
uniform vec3 LIGHTCOLOR;
centroid varying vec2 vUv;
varying float light;
varying float lift;
vec3 lrp2Linear(vec3 s) {
    return mix(s / 12.92, pow((s + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), s));
}
vec3 lrp2SRGB(vec3 s) {
    s = max(s, vec3(0.0));
    return mix(12.92 * s, 1.055 * pow(s, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), s));
}
vec3 lrp2DisplayMap(vec3 x) {
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}
vec3 lrp2Emission(vec3 a, float b, float seconds) {
    float pulse = max(sin(6.283185307179586 * seconds / 10.0) / 3.0 + 2.0, 0.0);
    vec3 c = vec3(1.0, 0.13600000739097595, 0.9861199855804443);
    return a * 0.6000000238418579 + b * 10.0 * pulse * c * c;
}
void main() {
    vec4 base = texture2D(map, vUv);
    if (base.a < 0.1) discard;
    // Image coordinates have their origin at the top left; Three may flip Y.
    vec2 imageUV = vec2(vUv.x, lrp2FlipY > 0.5 ? 1.0 - vUv.y : vUv.y);
    vec2 auxUV = imageUV;
    if (imageUV.x >= 0.5 && imageUV.y < 0.5) auxUV.y += 0.5;
    else if (imageUV.x < 0.5 && imageUV.y >= 0.5) auxUV.x += 0.5;
    else discard;
    auxUV.y = lrp2FlipY > 0.5 ? 1.0 - auxUV.y : auxUV.y;
    vec4 packed = texture2D(map, auxUV);
    if (abs(packed.r * 255.0 - 19.0) > 0.6 || abs(packed.g * 255.0 - 237.0) > 0.6 || abs(packed.a * 255.0 - 255.0) > 0.6) discard;
    vec3 a = lrp2Linear(base.rgb);
    vec3 e = lrp2Emission(a, lrp2Linear(packed.rgb).b, lrp2Time) * lrp2EmissionEnabled;
    vec3 surface = lrp2Mode > 0.5 ? vec3(0.0) : a * light * LIGHTCOLOR;
    if (lrp2Mode > 1.5) {
        // Diagnostic shader output preserves HDR before framebuffer display.
        gl_FragColor = vec4(e, base.a);
    } else {
        gl_FragColor = vec4(lrp2SRGB(lrp2DisplayMap(surface + e)) + lift, base.a);
        if (lift > 0.2) gl_FragColor.rgb *= vec3(0.6, 0.7, 1.0);
    }
    #include <clipping_planes_fragment>
}`;

    function time() {
        if (frozenTime !== null) return frozenTime;
        if (typeof Animator !== 'undefined' && Animator.open && typeof Timeline !== 'undefined' && Number.isFinite(Timeline.time)) return Timeline.time;
        return (performance.now() - started) / 1000;
    }

    function apply(project = Project) {
        const config = project?.dungeons_material_source;
        if (!isP2(project)) return false;
        const texture = project.textures.find(t => t.uuid === config.albedo_uuid);
        const material = texture?.getOwnMaterial();
        if (!material?.uniforms?.map?.value) return false;
        const map = material.uniforms.map.value;
        if (!touched.has(material)) {
            touched.set(material, {fragment: material.fragmentShader, side: material.side,
                minFilter: map.minFilter, magFilter: map.magFilter, generateMipmaps: map.generateMipmaps, project});
        }
        Object.assign(material.uniforms, {
            lrp2Time: {value: time()}, lrp2FlipY: {value: map.flipY ? 1 : 0},
            lrp2Mode: {value: 0}, lrp2EmissionEnabled: {value: 1}
        });
        map.minFilter = THREE.NearestFilter;
        map.magFilter = THREE.NearestFilter;
        map.generateMipmaps = false;
        map.needsUpdate = true;
        material.fragmentShader = fragment;
        material.side = THREE.DoubleSide;
        material.needsUpdate = true;
        if (project === Project) Canvas.updateAllFaces();
        return true;
    }

    function update() {
        const seconds = time();
        for (const [material, saved] of touched) {
            material.uniforms.lrp2Time.value = seconds;
            if (saved.project === Project && typeof Preview !== 'undefined') {
                for (const preview of Preview.all) if (preview.canvas?.isConnected) preview.render();
            }
        }
    }

    function hdrSample(a, b, seconds) {
        const c = [1, 0.13600000739097595, 0.9861199855804443];
        const pulse = Math.max(Math.sin(2 * Math.PI * seconds / 10) / 3 + 2, 0);
        return a.map((v, i) => v * 0.6000000238418579 + b * 10 * pulse * c[i] * c[i]);
    }

    Plugin.register('lucifer_p2_material', {
        title: 'Lucifer Phase 2 Original Material', author: 'Codex', icon: 'lightbulb',
        description: 'Verified Jungle B-channel HDR pulsation and NaturalEmissive, with an explicit bounded display transform.',
        version: '1.0.0', min_version: '5.2.0', variant: 'desktop',
        onload() {
            subscriptions.push(Codecs.project.on('compile', ({model}) => {
                const config = Project?.dungeons_material_source;
                if (isP2()) {
                    model.dungeons_material_source = structuredClone(config);
                    if (Project.display_dungeons) model.display_dungeons = structuredClone(Project.display_dungeons);
                    for (const raw of model.animations || []) {
                        const animation = Animation.all.find(a => a.uuid === raw.uuid || a.name === raw.name);
                        if (animation?.dungeons_affine_tracks) raw.dungeons_affine_tracks = structuredClone(animation.dungeons_affine_tracks);
                    }
                }
            }));
            subscriptions.push(Codecs.project.on('parse', ({model}) => {
                if (model.dungeons_material_source?.schema === schema && /^lucifer_p2(?:$|[_ ])/.test(model.name)) {
                    Project.dungeons_material_source = structuredClone(model.dungeons_material_source);
                    if (model.display_dungeons) Project.display_dungeons = structuredClone(model.display_dungeons);
                }
            }));
            subscriptions.push(Codecs.project.on('parsed', ({model}) => {
                const project = Project;
                importAffine(model.animations);
                apply(project);
                for (const texture of project.textures) if (!texture.img.complete) texture.img.addEventListener('load', () => apply(project), {once: true});
            }));
            globalThis.LuciferP2Material = {
                apply, fragment, hdrSample, applyAffine, restoreAffine, sampleAffine, importAffine,
                setTime(seconds = null) {
                    if (seconds !== null && !Number.isFinite(seconds)) throw new TypeError('time must be finite or null');
                    frozenTime = seconds; update();
                },
                setMode(mode = 0) {
                    if (![0, 1, 2].includes(mode)) throw new RangeError('mode 0=composite, 1=emission, 2=raw HDR diagnostic');
                    for (const [material, saved] of touched) if (saved.project === Project) material.uniforms.lrp2Mode.value = mode;
                    update();
                },
                setEmission(enabled = true) {
                    for (const [material, saved] of touched) if (saved.project === Project) material.uniforms.lrp2EmissionEnabled.value = enabled ? 1 : 0;
                    update();
                },
                status() {
                    return {project: Project?.name, schema: Project?.dungeons_material_source?.schema,
                        active: [...touched.values()].some(x => x.project === Project), seconds: time(), frozen: frozenTime !== null,
                        affineGroups: [...affineTouched.keys()].map(g => g.name),
                        mapping: 'verified linear HDR expression + ACES fitted/sRGB display', gameValidation: false};
                }
            };
            for (const project of ModelProject.all) apply(project);
            eventSubscriptions.push(Blockbench.on('display_default_pose', () => restoreAffine(Project)));
            eventSubscriptions.push(Blockbench.on('display_animation_frame', applyAffine));
            eventSubscriptions.push(Blockbench.on('select_project', () => restoreAffine()));
            timer = setInterval(update, 50);
        },
        onunload() {
            clearInterval(timer);
            restoreAffine();
            for (const subscription of subscriptions) subscription.delete();
            for (const subscription of eventSubscriptions) subscription.delete();
            for (const [material, saved] of touched) {
                material.fragmentShader = saved.fragment;
                material.side = saved.side;
                for (const key of ['lrp2Time', 'lrp2FlipY', 'lrp2Mode', 'lrp2EmissionEnabled']) delete material.uniforms[key];
                const map = material.uniforms.map.value;
                map.minFilter = saved.minFilter; map.magFilter = saved.magFilter;
                map.generateMipmaps = saved.generateMipmaps; map.needsUpdate = true;
                material.needsUpdate = true;
            }
            touched.clear(); delete globalThis.LuciferP2Material; Canvas.updateAllFaces();
        }
    });
})();
