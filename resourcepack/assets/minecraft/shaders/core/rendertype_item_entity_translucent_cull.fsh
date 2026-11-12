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

// BEGIN LUCIFER_P1_MESH DECL
#moj_import <minecraft:light.glsl>
vec3 luRemap(vec3 s) { ivec3 c=ivec3(floor(s*255.0+0.5));
if(all(equal(c,ivec3(16,75,9)))) return vec3(0.07450980392156863,0.28627450980392155,0.19215686274509805);
if(all(equal(c,ivec3(21,95,11)))) return vec3(0.10196078431372549,0.36470588235294116,0.24705882352941178);
if(all(equal(c,ivec3(21,77,11)))) return vec3(0.0784313725490196,0.2980392156862745,0.19607843137254902);
if(all(equal(c,ivec3(17,74,9)))) return vec3(0.07058823529411765,0.2823529411764706,0.18823529411764706);
if(all(equal(c,ivec3(30,98,17)))) return vec3(0.10588235294117647,0.3764705882352941,0.2549019607843137);
if(all(equal(c,ivec3(21,76,11)))) return vec3(0.07450980392156863,0.29411764705882354,0.19607843137254902);
if(all(equal(c,ivec3(21,96,11)))) return vec3(0.10196078431372549,0.3686274509803922,0.24705882352941178);
if(all(equal(c,ivec3(19,44,10)))) return vec3(0.03137254901960784,0.17254901960784313,0.10980392156862745);
if(all(equal(c,ivec3(42,101,23)))) return vec3(0.11372549019607843,0.39215686274509803,0.26666666666666666);
if(all(equal(c,ivec3(22,90,11)))) return vec3(0.09411764705882353,0.34509803921568627,0.23137254901960785);
if(all(equal(c,ivec3(22,91,11)))) return vec3(0.09803921568627451,0.34901960784313724,0.23529411764705882);
if(all(equal(c,ivec3(21,89,11)))) return vec3(0.09411764705882353,0.3411764705882353,0.23137254901960785);
if(all(equal(c,ivec3(22,101,11)))) return vec3(0.10980392156862745,0.38823529411764707,0.2627450980392157);
if(all(equal(c,ivec3(22,96,11)))) return vec3(0.10196078431372549,0.3686274509803922,0.24705882352941178);
if(all(equal(c,ivec3(21,92,11)))) return vec3(0.09803921568627451,0.35294117647058826,0.23921568627450981);
if(all(equal(c,ivec3(17,59,10)))) return vec3(0.050980392156862744,0.22745098039215686,0.14901960784313725);
if(all(equal(c,ivec3(21,90,11)))) return vec3(0.09411764705882353,0.34509803921568627,0.23137254901960785);
if(all(equal(c,ivec3(22,107,11)))) return vec3(0.11764705882352941,0.40784313725490196,0.2784313725490196);
if(all(equal(c,ivec3(21,101,11)))) return vec3(0.10980392156862745,0.38823529411764707,0.2627450980392157);
if(all(equal(c,ivec3(20,62,10)))) return vec3(0.054901960784313725,0.23921568627450981,0.1568627450980392);
if(all(equal(c,ivec3(19,49,10)))) return vec3(0.0392156862745098,0.19215686274509805,0.12156862745098039);
if(all(equal(c,ivec3(32,98,17)))) return vec3(0.10588235294117647,0.3803921568627451,0.2549019607843137);
if(all(equal(c,ivec3(17,80,10)))) return vec3(0.08235294117647059,0.3058823529411765,0.20392156862745098);
if(all(equal(c,ivec3(19,48,10)))) return vec3(0.03529411764705882,0.18823529411764706,0.12156862745098039);
if(all(equal(c,ivec3(19,46,10)))) return vec3(0.03529411764705882,0.1803921568627451,0.11372549019607843);
if(all(equal(c,ivec3(20,49,10)))) return vec3(0.0392156862745098,0.19215686274509805,0.12156862745098039);
if(all(equal(c,ivec3(23,107,11)))) return vec3(0.11764705882352941,0.40784313725490196,0.2784313725490196);
if(all(equal(c,ivec3(23,106,11)))) return vec3(0.11764705882352941,0.403921568627451,0.27450980392156865);
if(all(equal(c,ivec3(23,104,12)))) return vec3(0.11372549019607843,0.4,0.27058823529411763);
if(all(equal(c,ivec3(21,97,11)))) return vec3(0.10588235294117647,0.37254901960784315,0.25098039215686274);
if(all(equal(c,ivec3(42,102,23)))) return vec3(0.11372549019607843,0.396078431372549,0.27058823529411763);
if(all(equal(c,ivec3(22,105,11)))) return vec3(0.11764705882352941,0.4,0.27450980392156865);
if(all(equal(c,ivec3(22,103,11)))) return vec3(0.11372549019607843,0.396078431372549,0.26666666666666666);
if(all(equal(c,ivec3(22,102,11)))) return vec3(0.11372549019607843,0.39215686274509803,0.26666666666666666);
if(all(equal(c,ivec3(109,63,15)))) return vec3(0.34509803921568627,0.27450980392156865,0.27450980392156865);
if(all(equal(c,ivec3(62,21,0)))) return vec3(0.1607843137254902,0.12156862745098039,0.12156862745098039);
if(all(equal(c,ivec3(42,13,0)))) return vec3(0.10588235294117647,0.0784313725490196,0.0784313725490196);
if(all(equal(c,ivec3(92,52,11)))) return vec3(0.2901960784313726,0.22745098039215686,0.22745098039215686);
if(all(equal(c,ivec3(63,21,0)))) return vec3(0.16470588235294117,0.12549019607843137,0.12549019607843137);
if(all(equal(c,ivec3(50,17,0)))) return vec3(0.12941176470588237,0.09803921568627451,0.09803921568627451);
if(all(equal(c,ivec3(33,11,0)))) return vec3(0.08627450980392157,0.058823529411764705,0.058823529411764705);
if(all(equal(c,ivec3(54,18,0)))) return vec3(0.1411764705882353,0.10588235294117647,0.10588235294117647);
if(all(equal(c,ivec3(36,11,0)))) return vec3(0.09019607843137255,0.06666666666666667,0.06666666666666667);
if(all(equal(c,ivec3(75,42,8)))) return vec3(0.23529411764705882,0.1843137254901961,0.1843137254901961);
return s; }

flat in int luMode;
flat in ivec2 luAtlasOrigin;
flat in vec3 luBary0;
flat in vec3 luBary1;
flat in vec2 luUV0;
flat in vec2 luUV1;
flat in vec2 luUV2;
in vec2 luPlane;
in vec3 luWorldPosition;

vec3 luLinear(vec3 c) {
    return mix(c/12.92,pow((c+0.055)/1.055,vec3(2.4)),greaterThan(c,vec3(0.04045)));
}
vec3 luSRGB(vec3 c) {
    return mix(c*12.92,1.055*pow(max(c,vec3(0)),vec3(1.0/2.4))-0.055,greaterThan(c,vec3(0.0031308)));
}
vec2 luSourceUV;
vec4 luSample(out ivec2 uv) {
    vec3 p=vec3(luPlane,1.0);
    vec3 b=vec3(dot(luBary0,p),dot(luBary1,p),0); b.z=1.0-b.x-b.y;
    if(any(lessThan(b,vec3(0)))) discard;
    luSourceUV=b.x*luUV0+b.y*luUV1+b.z*luUV2;
    uv=ivec2(floor(luSourceUV));
    ivec2 limit=luMode==3?ivec2(191,63):(luMode==1?ivec2(63,31):ivec2(63));
    ivec2 offset=luMode==3?ivec2(0,320):(luMode==1?ivec2(0):ivec2(64,0));
    uv=clamp(uv,ivec2(0),limit);
    vec4 a=texelFetch(Sampler0,luAtlasOrigin+offset+uv,0);
    if(a.a < (luMode==2?0.33329999446868896:0.1)) discard;
    return a;
}
in vec4 luTint; in vec4 luLight;
vec4 luFragment() {
    ivec2 uv; vec4 a=luSample(uv);
    vec3 n=normalize(cross(dFdx(luWorldPosition),dFdy(luWorldPosition)));
    n *= gl_FrontFacing?1.0:-1.0;
    vec4 light=minecraft_mix_light(Light0_Direction,Light1_Direction,n,luTint)*luLight;
    vec4 color=a*light*ColorModulator;
    if(luMode==2) {
        vec3 albedo=luLinear(luRemap(a.rgb))*vec3(0.4,0.4,0.4);
        vec3 aux=luLinear(texelFetch(Sampler0,luAtlasOrigin+ivec2(128,0)+uv,0).rgb);
        vec3 E=max((aux.b*vec3(1.0,1.0,1.0)*1.0+albedo*0.699999988079071)*1.0,vec3(0));
        color.rgb=luSRGB(albedo*light.rgb*ColorModulator.rgb+E);
    }
    if(luMode==1) { vec2 eyePixel=clamp(luSourceUV*4.0,vec2(0.5),vec2(255.5,127.5)); vec4 layer=textureLod(Sampler0,(vec2(luAtlasOrigin)+vec2(256,0)+eyePixel)/vec2(textureSize(Sampler0,0)),0.0); color.rgb=1.0-(1.0-color.rgb)*(1.0-layer.rgb*layer.a*0.14); }
    if(luMode==1 && (all(equal(uv,ivec2(13,12))) || all(equal(uv,ivec2(14,12))))) { color.rgb=vec3(0.6588235294117647,0.3333333333333333,0.9686274509803922); }
    return apply_fog(color,sphericalVertexDistance,cylindricalVertexDistance,FogEnvironmentalStart,FogEnvironmentalEnd,FogRenderDistanceStart,FogRenderDistanceEnd,FogColor);
}
// END LUCIFER_P1_MESH DECL

void main() {
// BEGIN LUCIFER_P1_MESH MAIN
    if(luMode!=0) { fragColor=luFragment(); return; }
// END LUCIFER_P1_MESH MAIN


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
