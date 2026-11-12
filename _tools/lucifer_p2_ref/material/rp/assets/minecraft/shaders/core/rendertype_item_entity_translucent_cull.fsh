#version 330

#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in float sphericalVertexDistance;
in float cylindricalVertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in vec2 texCoord1;

out vec4 fragColor;


// BEGIN LUCIFER_P2_OPT_IN declarations
flat in int lrp2Mode;
flat in int lrp2Phase;
in vec4 lrp2WhiteLight;

vec3 lrp2Linear(vec3 s) {
    return mix(s / 12.92, pow((s + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), s));
}
vec3 lrp2SRGB(vec3 s) {
    s = max(s, vec3(0.0));
    return mix(12.92 * s, 1.055 * pow(s, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), s));
}
vec3 lrp2DisplayMap(vec3 x) {
    // Explicit bounded display transform, shared with the BB preview.
    // ACES fitted curve; this is not a claim about the game's original exposure.
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}
vec3 lrp2Emission(vec3 albedo, float auxiliaryB, float phase) {
    float pulse = max(sin(6.283185307179586 * phase) / 3.0 + 2.0, 0.0);
    vec3 c = vec3(1.0, 0.13600000739097595, 0.9861199855804443);
    return albedo * 0.6000000238418579 + auxiliaryB * 10.0 * pulse * c * c;
}

// END LUCIFER_P2_OPT_IN declarations

void main() {

    // BEGIN LUCIFER_P2_OPT_IN fragment
    if (lrp2Mode != 0) {
        ivec2 lrp2Extent = textureSize(Sampler0, 0);
        ivec2 lrp2Pixel = ivec2(floor(texCoord0 * vec2(lrp2Extent)));
        ivec2 lrp2Aux = lrp2Pixel + (lrp2Mode == 1 ? ivec2(0, 2048) : ivec2(2048, 0));
        if (all(greaterThanEqual(lrp2Aux, ivec2(0))) && all(lessThan(lrp2Aux, lrp2Extent))) {
            vec4 lrp2Packed = texelFetch(Sampler0, lrp2Aux, 0);
            // Opaque data prevents browser Canvas premultiplication rounding B.
            ivec3 lrp2Magic = ivec3(floor(vec3(lrp2Packed.rg, lrp2Packed.a) * 255.0 + 0.5));
            if (all(equal(lrp2Magic, ivec3(19, 237, 255)))) {
                // LOD0 on both inputs prevents mips crossing cutout/data tiles.
                vec4 lrp2Base = texelFetch(Sampler0, lrp2Pixel, 0);
                float lrp2Alpha = lrp2Base.a * lrp2WhiteLight.a * ColorModulator.a;
                if (lrp2Alpha < 0.1) discard;
                vec3 lrp2A = lrp2Linear(lrp2Base.rgb);
                vec3 lrp2S = lrp2Linear(lrp2Packed.rgb);
                vec3 lrp2Lit = lrp2A * lrp2WhiteLight.rgb;
                vec3 lrp2E = lrp2Emission(lrp2A, lrp2S.b, float(lrp2Phase) / 200.0);
                vec4 lrp2Color = vec4(lrp2SRGB(lrp2DisplayMap(lrp2Lit + lrp2E)) * ColorModulator.rgb, lrp2Alpha);
                fragColor = apply_fog(lrp2Color, sphericalVertexDistance, cylindricalVertexDistance, FogEnvironmentalStart, FogEnvironmentalEnd, FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
                return;
            }
        }
    }
    // END LUCIFER_P2_OPT_IN fragment

    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (color.a < 0.1) {
        discard;
    }
    fragColor = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance, FogEnvironmentalStart, FogEnvironmentalEnd, FogRenderDistanceStart, FogRenderDistanceEnd, FogColor);
}
