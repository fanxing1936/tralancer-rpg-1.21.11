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

void main() {
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
