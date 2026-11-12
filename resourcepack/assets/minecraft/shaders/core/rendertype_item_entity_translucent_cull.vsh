#version 330

#moj_import <minecraft:light.glsl>
#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:projection.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in vec2 UV1;
in ivec2 UV2;
in vec3 Normal;

uniform sampler2D Sampler2;


out float sphericalVertexDistance;
out float cylindricalVertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;
out vec2 texCoord1;
out vec2 texCoord2;


// BEGIN LUCIFER_P2_OPT_IN declarations
flat out int lrp2Mode;
flat out int lrp2Phase;
out vec4 lrp2WhiteLight;
// END LUCIFER_P2_OPT_IN declarations

// BEGIN LUCIFER_P1_MESH DECL

uniform sampler2D Sampler0;
flat out int luMode;
flat out ivec2 luAtlasOrigin;
flat out vec3 luBary0;
flat out vec3 luBary1;
flat out vec2 luUV0;
flat out vec2 luUV1;
flat out vec2 luUV2;
out vec2 luPlane;
out vec3 luWorldPosition;

uvec4 luBytes(ivec2 p) {
    return uvec4(floor(texelFetch(Sampler0, p, 0) * 255.0 + 0.5));
}
float luFloat(ivec2 base, int index) {
    uvec4 b = luBytes(base + ivec2(index % 8, 2 + index / 8));
    uint u = b.x | (b.y << 8u) | (b.z << 16u) | (b.w << 24u);
    return uintBitsToFloat(u);
}
void luDecode() {
    luMode = 0;
    luAtlasOrigin = ivec2(0);
    luBary0 = vec3(0); luBary1 = vec3(0);
    luUV0 = vec2(0); luUV1 = vec2(0); luUV2 = vec2(0);
    luPlane = vec2(0); luWorldPosition = Position;
    ivec2 extent = textureSize(Sampler0, 0);
    ivec2 at = ivec2(floor(UV0 * vec2(extent)));
    if (any(lessThan(at,ivec2(0))) || any(greaterThanEqual(at,extent))) return;
    uvec4 b = luBytes(at);
    if (any(notEqual(b.xyz,uvec3(17u,149u,83u))) || b.w < 240u || b.w > 243u) return;
    uint corner = b.w - 240u;
    ivec2 offset = ivec2(int(corner & 1u),int((corner >> 1u) & 1u));
    ivec2 base = at - offset;
    if (any(lessThan(base,ivec2(0))) || any(greaterThanEqual(base+ivec2(7),extent))) return;
    if (any(notEqual(luBytes(base+ivec2(2,0)),uvec4(211u,57u,193u,71u)))) return;
    if (any(notEqual(luBytes(base+ivec2(3,0)),uvec4(65u,27u,219u,156u)))) return;
    luAtlasOrigin = base-ivec2(int(luFloat(base,0)),int(luFloat(base,1)));
    luMode = 1+int(luFloat(base,2));
    luBary0 = vec3(luFloat(base,3),luFloat(base,4),luFloat(base,5));
    luBary1 = vec3(luFloat(base,6),luFloat(base,7),luFloat(base,8));
    luUV0 = vec2(luFloat(base,9),luFloat(base,10));
    luUV1 = vec2(luFloat(base,11),luFloat(base,12));
    luUV2 = vec2(luFloat(base,13),luFloat(base,14));
    luPlane = vec2(offset.x,1-offset.y);
}
out vec4 luTint; out vec4 luLight;
// END LUCIFER_P1_MESH DECL

void main() {
// BEGIN LUCIFER_P1_MESH MAIN
    luDecode();
    luTint=Color; luLight=texelFetch(Sampler2,UV2/16,0);
// END LUCIFER_P1_MESH MAIN

    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    sphericalVertexDistance = fog_spherical_distance(Position);
    cylindricalVertexDistance = fog_cylindrical_distance(Position);
    vertexColor = minecraft_mix_light(Light0_Direction, Light1_Direction, Normal, Color) * texelFetch(Sampler2, UV2 / 16, 0);
    texCoord0 = UV0;
    texCoord1 = UV1;
    texCoord2 = UV2;

    // BEGIN LUCIFER_P2_OPT_IN vertex
    ivec3 lrp2Bytes = ivec3(floor(Color.rgb * 255.0 + 0.5));
    lrp2Mode = 0;
    lrp2Phase = 0;
    if (lrp2Bytes.g == 211 && lrp2Bytes.b >= 0 && lrp2Bytes.b < 200) {
        if (lrp2Bytes.r == 37) lrp2Mode = 1;
        if (lrp2Bytes.r == 38) lrp2Mode = 2;
        lrp2Phase = lrp2Bytes.b;
    }
    // Separate white input: no division by tinted colors or zero components.
    lrp2WhiteLight = minecraft_mix_light(Light0_Direction, Light1_Direction, Normal, vec4(1.0, 1.0, 1.0, Color.a)) * texelFetch(Sampler2, UV2 / 16, 0);
    // END LUCIFER_P2_OPT_IN vertex
}
