"""Source-frame scale audit of the eight non-strike M3 clips.

Reviewed all 530 decoded frames, at fixed image scale within each clip, from
the original GIFs (not just M1's saved keyframes).  Suspect phases were also
inspected at the original pixel dimensions.  The animation names ``appear``
and ``hurt`` correspond to the source GIF names ``Spawn`` and ``Staggered``.

No non-unit LOCAL bone scale is sufficiently supported in these eight clips.
The screen-space changes can be explained by visible rotation, foreshortening,
occlusion, translation and articulated cloth.  In particular, the larger
silhouette of a raised fist is not by itself evidence of glove enlargement.
This is a conservative source-image finding, not a claim to have recovered
the game's original animation curves or proved that every hidden scale is 1.

Consequently this module intentionally adds no scale or seam-compensation
position tracks.  Keep the existing unit scale (1, 1, 1); do not introduce
speculative squash/stretch into a clip merely because it contains an impact.
There are no measured non-unit ratios to report and no non-unit anchor ranges
requiring unit keys before/after.  Strike-specific tracks belong to the other
two scale-audit modules, outside this file's scope.

Interface, when supported by evidence:
    SCALE = {clip: {bone: [(source_frame, (local_sx, local_sy, local_sz)), ...]}}
    POSITION = {clip: {bone: [(source_frame, (local_dx, local_dy, local_dz)), ...]}}
"""

SCALE = {}
POSITION = {}

# Inclusive source frame ranges.  These are the images actually inspected;
# they are not new animation keyframes or inferred timing values.
REVIEWED_FRAMES = {
    'idle': (0, 23),
    'walk': (0, 21),
    'appear': (0, 56),
    'death': (0, 136),
    'launch': (0, 94),
    'overcharge': (0, 85),
    'hurt': (0, 54),
    'summon': (0, 53),
}

# Concrete checks behind the deliberately empty tracks.  Pixel silhouette
# lengths across different angles were not misreported as local 3-D ratios.
EVIDENCE = {
    'idle': (
        'f0-23: the glove/cuff/sleeve boundaries retain their proportions; '
        'the small outline changes follow the arm and torso rocking.',
    ),
    'walk': (
        'f0-5 and f10-16: opposite arm/leg extremes expose different faces; '
        'the sleeve and glove remain rigid cuboids without an independent '
        'bulge or length pulse.',
    ),
    'appear': (
        'Source Spawn f0-5 is fully transparent, so no scale is observable.',
        'f6-10: the landing compresses the pose, while the head, hanging '
        'gloves and cyan shoulder cuffs retain straight cuboid edges; the '
        'large upper outline is the raised, then falling, cape.',
        'f10-26: the crouched hold has stable cuff-to-glove proportions; '
        'f27-42 rises and rolls the shoulders into guard.  Neither phase '
        'provides evidence of a separate glove or sleeve scale pulse.',
    ),
    'death': (
        'f1-12 recoil, f30-40 kneeling and f108-113 collapse change the '
        'viewing angles and overlap substantially; no fist expands '
        'independently of those rotations.',
        'f114-136: the prone head, fists and sleeves settle with unchanged '
        'cuboid proportions.  The large remaining motion is cape rotation.',
    ),
    'launch': (
        'f2-24: apparent whole-character compression is the folded-leg '
        'crouch, with stable arm/glove dimensions.',
        'f25-26: the silhouette lengthens when the limbs unfold for takeoff; '
        'the full-resolution f26 sleeve and glove retain their ordinary '
        'proportions.  f27-52 is transparent and supplies no scale evidence.',
        'f53-59 landing repeats the Spawn-like rigid hand/cuff construction; '
        'f70-83 bends forward and recovers without an independent size pulse.',
    ),
    'overcharge': (
        'f6-12: the near fist turns toward the camera, exposing the broad '
        'end face and shortening its projected axis.',
        'f30-46: the near arm rises beside the head; a larger projected '
        'sleeve length accompanies the clearly changing arm orientation. '
        'Its cuff and glove remain a continuous rigid stack.',
        'f46-69: the charging hold does not continue to inflate the raised '
        'glove or sleeve.  At original resolution the glove bands retain '
        'their proportions as the fist rotates slightly and overlaps the '
        'hat differently.  f70-85 returns through the same rigid shapes.',
    ),
    'hurt': (
        'Source Staggered f4-17: the forward leg and open arms become '
        'more visible as the torso tips; no separate limb enlargement is '
        'supported.  f33-54 recovery preserves the same rigid proportions.',
    ),
    'summon': (
        'f0-12: torso lean and the cape changing from edge-on to broadside '
        'alter the outline; the near glove does not independently enlarge.',
        'f12-15: the rapid raise exposes both glove end faces and changes '
        'their projected lengths.  Original-size f13/f14 show ordinary '
        'cuboid gloves with unchanged band structure, not a stretched '
        'smear or a separately swelling fist.',
        'f14-33: the overhead hold has stable glove/cuff/sleeve proportions. '
        'f34-45 lowers the arms while the torso and legs rock, and f46-53 '
        'returns to guard without an independently measurable scale pulse.',
    ),
}

assert sum(last - first + 1 for first, last in REVIEWED_FRAMES.values()) == 530
