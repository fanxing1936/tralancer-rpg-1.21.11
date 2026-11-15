(function () {
    const touched = new Map();
    const subscriptions = [];
    const fragment = `
#ifdef GL_ES
precision highp float;
#endif
#include <common>
#include <clipping_planes_pars_fragment>
#include <tonemapping_pars_fragment>
uniform sampler2D map;
uniform sampler2D sourceAuxiliary;
uniform vec3 sourcePaletteTintLinear;
uniform vec3 sourcePaletteFrom[64];
uniform vec3 sourcePaletteTo[64];
uniform int sourcePaletteCount;
uniform vec3 sourceEmissiveColor;
uniform float sourceEmissivePower;
uniform float sourceNaturalEmissive;
uniform float sourceDeathEmissive;
uniform float sourceOpacityClip;
uniform float sourcePreviewMode;
uniform float sourceEmissionEnabled;
uniform bool SHADE;
uniform bool EMISSIVE;
uniform vec3 LIGHTCOLOR;
centroid varying vec2 vUv;
varying float light;
varying float lift;
vec3 sourceSRGBToLinear(vec3 s) {
    return mix(s / 12.92, pow((s + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), s));
}
vec3 sourceLinearToSRGB(vec3 s) {
    s = max(s, vec3(0.0));
    return mix(12.92 * s, 1.055 * pow(s, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), s));
}
vec3 dungeonsStaticEmissive(vec3 albedo, vec3 auxiliary) {
    vec3 primary = auxiliary.b * sourceEmissiveColor;
    vec3 natural = albedo * sourceNaturalEmissive;
    vec3 emissive = primary * sourceEmissivePower + natural;
    return max(emissive * sourceDeathEmissive, vec3(0.0));
}
vec3 sourceRemapPalette(vec3 color) {
    for (int i = 0; i < 64; i++) {
        if (i < sourcePaletteCount && all(lessThan(abs(color - sourcePaletteFrom[i]), vec3(0.001)))) {
            return sourcePaletteTo[i];
        }
    }
    return color;
}
void main() {
    vec4 original = texture2D(map, vUv);
    if (original.a < sourceOpacityClip) discard;
    // Optional project palette changes surface and natural emission together.
    // The original auxiliary-mask emission remains independent of this tint.
    vec3 albedo = sourceSRGBToLinear(sourceRemapPalette(original.rgb)) * sourcePaletteTintLinear;
    vec3 auxiliary = sourceSRGBToLinear(texture2D(sourceAuxiliary, vUv).rgb);
    vec3 emissive = dungeonsStaticEmissive(albedo, auxiliary) * sourceEmissionEnabled;
    if (sourcePreviewMode > 1.5) {
        gl_FragColor = vec4(emissive, original.a);
    } else {
        vec3 surface = sourcePreviewMode > 0.5 ? vec3(0.0) : albedo * light * LIGHTCOLOR;
        vec3 preview = ACESFilmicToneMapping(surface + emissive);
        gl_FragColor = vec4(sourceLinearToSRGB(preview) + lift, original.a);
        if (lift > 0.2) gl_FragColor.rgb *= vec3(0.6, 0.7, 1.0);
    }
    #include <clipping_planes_fragment>
}`;

    function paletteTint(config) {
        const tint = config?.palette_tint_linear;
        return Array.isArray(tint) && tint.length === 3 && tint.every(v => Number.isFinite(v) && v >= 0)
            ? tint : [1, 1, 1];
    }

    function applyEye(project) {
        const config = project?.lucifer_eye_emission;
        if (config?.schema !== 'lucifer-eye-emission-v1') return false;
        const texture = project.textures.find(t => t.uuid === config.texture_uuid);
        const layer = project.textures.find(t => t.uuid === config.emissive_layer_uuid);
        const material = texture?.getOwnMaterial();
        if (!material?.uniforms?.map || config.texels?.length !== 2) return false;
        if (!touched.has(material)) touched.set(material, material.fragmentShader);
        const base = touched.get(material);
        const declarations = `
uniform vec2 luciferEyeTextureSize;
uniform vec2 luciferEyeTexels[2];
uniform vec3 luciferEyeEmissionLinear;
uniform float luciferEyeEnabled;
uniform sampler2D luciferEyeLayer;
uniform float luciferEyeHasLayer;
uniform float luciferEyeHaloStrength;
vec3 luciferEyeToSRGB(vec3 s) {
    return mix(12.92 * s, 1.055 * pow(s, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), s));
}
`;
        const body = `
vec2 eyePixel = floor(vec2(vUv.x, 1.0 - vUv.y) * luciferEyeTextureSize);
bool isLeftEye = all(lessThan(abs(eyePixel - luciferEyeTexels[0]), vec2(0.1)))
    || all(lessThan(abs(eyePixel - luciferEyeTexels[1]), vec2(0.1)));
if (isLeftEye && luciferEyeEnabled > 0.5) {
    gl_FragColor.rgb = luciferEyeToSRGB(ACESFilmicToneMapping(luciferEyeEmissionLinear));
} else if (luciferEyeEnabled > 0.5 && luciferEyeHasLayer > 0.5) {
    vec4 halo = texture2D(luciferEyeLayer, vUv);
    gl_FragColor.rgb = 1.0 - (1.0 - gl_FragColor.rgb)
        * (1.0 - halo.rgb * halo.a * luciferEyeHaloStrength);
}
`;
        material.fragmentShader = '#include <tonemapping_pars_fragment>\n' + declarations + base.replace(/}\s*$/, body + '\n}');
        Object.assign(material.uniforms, {
            luciferEyeTextureSize: {value: new THREE.Vector2(...config.texture_size_pixels)},
            luciferEyeTexels: {value: config.texels.map(p => new THREE.Vector2(...p))},
            luciferEyeEmissionLinear: {value: new THREE.Vector3(...config.emission_linear)},
            luciferEyeEnabled: {value: 1},
            luciferEyeLayer: {value: (layer || texture).getOwnMaterial().uniforms.map.value},
            luciferEyeHasLayer: {value: layer ? 1 : 0},
            luciferEyeHaloStrength: {value: config.halo_strength || 0},
            toneMappingExposure: {value: 1}
        });
        material.needsUpdate = true;
        return true;
    }

    function apply(project = Project) {
        applyEye(project);
        const config = project?.dungeons_material_source;
        if (!config || config.schema !== 'dungeons-static-emissive-v1') return false;
        const albedo = project.textures.find(t => t.uuid === config.albedo_uuid);
        const auxiliary = project.textures.find(t => t.uuid === config.auxiliary_uuid);
        if (!albedo || !auxiliary) return false;
        const material = albedo.getOwnMaterial();
        if (!material?.uniforms?.map) return false;
        if (!touched.has(material)) touched.set(material, material.fragmentShader);
        const p = config.parameters;
        const remap = config.palette_remap_srgb8 || [];
        if (remap.length > 64) throw new Error('Lucifer palette supports at most 64 source colors');
        const from = Array.from({length: 64}, (_, i) => new THREE.Vector3(...(remap[i]?.from || [0, 0, 0])).multiplyScalar(1 / 255));
        const to = Array.from({length: 64}, (_, i) => new THREE.Vector3(...(remap[i]?.to || [0, 0, 0])).multiplyScalar(1 / 255));
        Object.assign(material.uniforms, {
            sourceAuxiliary: {value: auxiliary.getOwnMaterial().uniforms.map.value},
            sourcePaletteTintLinear: {value: new THREE.Vector3(...paletteTint(config))},
            sourcePaletteFrom: {value: from},
            sourcePaletteTo: {value: to},
            sourcePaletteCount: {value: remap.length},
            sourceEmissiveColor: {value: new THREE.Vector3(...p.Emissive)},
            sourceEmissivePower: {value: p.EmissivePower},
            sourceNaturalEmissive: {value: p.NaturalEmissive},
            sourceDeathEmissive: {value: p.DeathEmissive},
            sourceOpacityClip: {value: p.OpacityMaskClipValue},
            sourcePreviewMode: {value: 0},
            sourceEmissionEnabled: {value: 1},
            toneMappingExposure: {value: config.preview.exposure}
        });
        material.fragmentShader = fragment;
        material.side = THREE.DoubleSide;
        material.needsUpdate = true;
        if (project === Project) Canvas.updateAllFaces();
        return true;
    }

    Plugin.register('lucifer_original_material', {
        title: 'Lucifer Original Dungeons Material',
        author: 'Codex',
        description: 'Restores the verified original static emissive equation with separate, unmodified source textures and HDR parameters.',
        icon: 'lightbulb',
        version: '1.2.0',
        min_version: '5.2.0',
        variant: 'desktop',
        onload() {
            subscriptions.push(Codecs.project.on('compile', ({model}) => {
                const config = Project?.dungeons_material_source;
                if (config?.schema === 'dungeons-static-emissive-v1') {
                    model.dungeons_material_source = structuredClone(config);
                }
                if (Project?.lucifer_eye_emission?.schema === 'lucifer-eye-emission-v1') {
                    model.lucifer_eye_emission = structuredClone(Project.lucifer_eye_emission);
                }
            }));
            subscriptions.push(Codecs.project.on('parse', ({model}) => {
                if (model.dungeons_material_source?.schema === 'dungeons-static-emissive-v1') {
                    Project.dungeons_material_source = structuredClone(model.dungeons_material_source);
                }
                if (model.lucifer_eye_emission?.schema === 'lucifer-eye-emission-v1') {
                    Project.lucifer_eye_emission = structuredClone(model.lucifer_eye_emission);
                }
            }));
            subscriptions.push(Codecs.project.on('parsed', () => {
                const project = Project;
                apply(project);
                for (const texture of project.textures) {
                    if (!texture.img.complete) texture.img.addEventListener('load', () => apply(project), {once: true});
                }
            }));
            globalThis.LuciferOriginalMaterial = {
                apply,
                fragment,
                status() {
                    const config = Project?.dungeons_material_source;
                    const texture = config && Project.textures.find(t => t.uuid === config.albedo_uuid);
                    return {project: Project?.name, configured: !!config,
                        active: !!texture && touched.has(texture.getOwnMaterial()),
                        parameters: config?.parameters, preview: config?.preview,
                        palette_tint_linear: paletteTint(config),
                        palette_remap_colors: config?.palette_remap_srgb8?.length || 0,
                        eye_configured: !!Project?.lucifer_eye_emission,
                        eye_active: !!Project?.lucifer_eye_emission && touched.has(Project.textures.find(t => t.uuid === Project.lucifer_eye_emission.texture_uuid)?.getOwnMaterial())};
                }
            };
            for (const project of ModelProject.all) apply(project);
        },
        onunload() {
            for (const subscription of subscriptions) subscription.delete();
            for (const [material, previous] of touched) {
                material.fragmentShader = previous;
                material.needsUpdate = true;
            }
            touched.clear();
            delete globalThis.LuciferOriginalMaterial;
            Canvas.updateAllFaces();
        }
    });
})();
