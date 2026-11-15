"""Source-GIF scale accents for the three strike clips.

Values are LOCAL bone scales (sx, sy, sz), not additive scale deltas.
Frames are zero-based original GIF frame IDs, not 20-TPS tick indices.
This module preserves every existing Astra rotation and root position.

The shoulders and hands are descendants of their arm.  Scale the arm once:
the shoulder panels, wrist pivot and fist must inherit that transform.  Do
not also copy the arm's scale onto the hand; that would square the effect.
No positional seam correction is needed on this hierarchy.

Measurements below are reproducible 2-D pixel observations, rounded at the
raster boundary.  The 3-D scale values are a conservative reconstruction,
not recovered engine animation data.  Read the original native-size GIFs;
the normalized detail sheets obscure part of the size change.
"""

UNIT = (1.0, 1.0, 1.0)

SCALE = {
    'forward_strike': {
        # Character-right arm: the extended fist is on screen-left.
        # Local Y runs along the sleeve; local Z makes the broad vertical
        # side-face edge in this punch.  X stays unchanged.
        'right_arm': [
            (0, UNIT),
            (34, UNIT),
            (35, (1.0, 1.4, 2.0)),
            (36, (1.0, 2.0, 1.5)),
            (37, (1.0, 1.15, 1.0)),
            (38, UNIT),
            (59, UNIT),
        ],
    },
    # The forward punches in this clip are not copies of the large
    # Forward Strike accent.  No comparable hard-edge scale change was
    # found at f17-19, f31-33, f89-91, f105-108 or f130-134.  Preserve the
    # accepted pose-only clip rather than adding unsupported enlargement.
    'fury_fist': {},
    'lightning_slam': {
        # Character-left arm: near arm on screen-right during landing.
        # The far right arm remains ordinary size.  The dark shoulder side
        # widens first, then its perpendicular top edge also expands.
        'left_arm': [
            (0, UNIT),
            (62, UNIT),
            (63, (1.0, 1.0, 2.0)),
            (64, (1.5, 1.0, 2.0)),
            (65, UNIT),
            (105, UNIT),
        ],
    },
}

# Intentionally empty: native hierarchical scale keeps arm/wrist contact.
POSITION = {}

EVIDENCE = {
    'forward_strike': {
        'source': 'originals/MCD2_Prime_Enchanter_Forward_Strike.gif',
        'times_seconds': {34: 1.42, 35: 1.46, 36: 1.50, 37: 1.54, 38: 1.58},
        'visible_interval': (35, 37),
        'confidence': 'high for interval and axes; scale ratios about +/- 0.1',
        # Same RGB (82, 33, 39) stripe on the broad red sleeve face.
        # Endpoints are (x,y) pixels on the unresized 632x494 source.
        'sleeve_stripe_long_edges_px': {
            35: ((177, 270), (236, 240)),  # 66.19 px / 47.41 ~= 1.40
            36: ((112, 352), (197, 308)),  # 95.71 px / 47.41 ~= 2.02
            37: ((220, 316), (268, 291)),  # 54.12 px / 47.41 ~= 1.14
            38: ((230, 312), (272, 290)),  # 47.41 px
            39: ((232, 340), (274, 318)),  # 47.41 px
        },
        'same_stripe_repeat_vertical_spacing_px': {
            35: 66, 36: 49, 37: 32, 38: 32, 39: 32,
        },
        # The gray strike-face patch of RGB (83,91,91) retains a 20px
        # transverse span; the extra width is on the other local axis.
        'gray_fist_patch_x_bounds_px': {
            35: (107, 127), 36: (19, 40),
            37: (160, 180), 39: (177, 197),
        },
        'interpretation': (
            'Crisp repeated sleeve stripes and fist faces change size while '
            'the head remains approximately constant.  The longitudinal '
            'stripe slope stays near -0.52, ruling out a foreshortening-only '
            'explanation.  f37 still has about 15% excess arm length; use '
            'f38, not f37, as the return-to-unit key.'
        ),
    },
    'fury_fist': {
        'source': 'originals/MCD2_Prime_Enchanter_Fury_Fist.gif',
        'full_timeline_checked': (0, 165),
        'critical_ranges_checked': [(16, 19), (30, 34), (88, 96),
                                    (104, 109), (130, 136)],
        'confidence': 'no supported non-unit keys',
        'interpretation': (
            'The sleeve stripes, cuff depth and shoulder width remain '
            'ordinary during the punch and slam transitions.  Silhouette '
            'changes come from the turn, arm direction and overlapping '
            'cape.  This clip supplies a useful negative control.'
        ),
    },
    'lightning_slam': {
        'source': 'originals/MCD2_Prime_Enchanter_Lightning_Slam.gif',
        'times_seconds': {62: 2.58, 63: 2.63, 64: 2.67, 65: 2.71},
        'visible_interval': (63, 64),
        'confidence': 'high for interval and left side; local ratios about +/- 0.1',
        # Native 528x1482 source, no crop-coordinate offset.
        # This is the local-Z edge of the near shoulder's dark blue side.
        'shoulder_z_edge_px': {
            63: ((265, 894), (347, 900)),  # 82.22 px, before the impact turn
            64: ((239, 1353), (317, 1322)),  # 83.93 px
            65: ((228, 1339), (266, 1322)),  # 41.63 px
        },
        # The perpendicular top edge at f64 grows by about 1.6x; choose
        # 1.5 rather than exaggerating the raster/pose uncertainty to 2x.
        'shoulder_x_edge_px': {
            64: ((260, 1273), (315, 1308)),  # 65.19 px
            65: ((232, 1286), (266, 1309)),  # 41.05 px
        },
        'shoulder_side_longitudinal_band_height_px': {63: 17, 64: 24, 65: 23},
        'interpretation': (
            'Near shoulder and cuff widen together, with sharp straight '
            'texture boundaries.  The cap side band at f64 is 24px high '
            'against 23px at f65, so do not lengthen local Y.  The matched '
            'dark-side edge is about 2x wide in both f63 and f64.  Only '
            'f64 clearly expands the perpendicular top edge.  The far '
            'right sleeve stays narrow; do not scale both arms.'
        ),
    },
}


def validate():
    """Small data-integrity check; does not edit or open the model."""
    last_frames = {'forward_strike': 59, 'fury_fist': 165, 'lightning_slam': 105}
    for clip, tracks in SCALE.items():
        for bone, keys in tracks.items():
            assert bone in {'right_arm', 'left_arm'}
            assert keys[0] == (0, UNIT)
            assert keys[-1] == (last_frames[clip], UNIT)
            assert all(a[0] < b[0] for a, b in zip(keys, keys[1:]))
            assert all(len(value) == 3 and all(v > 0 for v in value)
                       for _, value in keys)
    assert not POSITION
    return True


if __name__ == '__main__':
    validate()
    print('Strike scale data valid: right-arm punch; left-arm slam; no wrist double-scale.')
