VERTEX_HELPER=r'''
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
'''

FRAGMENT_HELPER=r'''
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
vec4 luFragment() {
    vec3 p=vec3(luPlane,1.0);
    vec3 bary=vec3(dot(luBary0,p),dot(luBary1,p),0.0);
    bary.z=1.0-bary.x-bary.y;
    if(any(lessThan(bary,vec3(0.0)))) discard;
    vec2 originalUV=bary.x*luUV0+bary.y*luUV1+bary.z*luUV2;
    ivec2 uv=ivec2(floor(originalUV));
    ivec2 size=luMode==1?ivec2(64,32):ivec2(64,64);
    uv=clamp(uv,ivec2(0),size-1);
    ivec2 origin=luAtlasOrigin+(luMode==1?ivec2(0):ivec2(64,0));
    vec4 albedo=texelFetch(Sampler0,origin+uv,0);
    if(albedo.a<0.1) discard;
    // POC keeps vanilla diffuse light; source Dungeons specular and normals are NOT ported here.
    vec4 color=albedo*vertexColor*ColorModulator;
    if(luMode==2) {
        vec3 auxiliary=luLinear(texelFetch(Sampler0,luAtlasOrigin+ivec2(128,0)+uv,0).rgb);
        // Verdant static emissive: linear(S).B*white + linear(Albedo)*0.699999988079071.
        // Kept as HDR float until the actual Minecraft framebuffer; its clipping/tone behavior is unverified.
        vec3 E=auxiliary.b*vec3(1.0)+luLinear(albedo.rgb)*0.699999988079071;
        color.rgb=luSRGB(luLinear(max(color.rgb,vec3(0)))+E);
    }
    return apply_fog(color,sphericalVertexDistance,cylindricalVertexDistance,
        FogEnvironmentalStart,FogEnvironmentalEnd,FogRenderDistanceStart,FogRenderDistanceEnd,FogColor);
}
'''
