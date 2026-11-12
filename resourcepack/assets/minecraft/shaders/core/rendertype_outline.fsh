#version 330

#moj_import <minecraft:dynamictransforms.glsl>

uniform sampler2D Sampler0;

in vec4 vertexColor;
in vec2 texCoord0;

out vec4 fragColor;

// BEGIN LUCIFER_P1_MESH DECL

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
// END LUCIFER_P1_MESH DECL

void main() {
// BEGIN LUCIFER_P1_MESH MAIN
    if(luMode!=0) { ivec2 uv; vec4 source=luSample(uv); fragColor=vec4(ColorModulator.rgb*vertexColor.rgb,ColorModulator.a); return; }
// END LUCIFER_P1_MESH MAIN

    vec4 color = texture(Sampler0, texCoord0);
    if (color.a == 0.0) {
        discard;
    }
    fragColor = vec4(ColorModulator.rgb * vertexColor.rgb, ColorModulator.a);
}
