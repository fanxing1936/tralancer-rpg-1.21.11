"""Key poses fitted to the Wiki GIFs on the accepted M2 rig.

Rows store original source frame numbers, absolute local ZYX Euler angles
in degrees, and root displacement in Blockbench units. Unlisted bones
retain the accepted rest pose. The GIFs show projected poses, so the fitted
angles and local depth are authoring estimates. They are not extracted keys.
"""


POSES = {
    # Keep the accepted guard and backstep through the loop. The hat and
    # shoulders rise and settle, while the long cloth bends at both folds.
    "idle": [
        (0, {}, (0, 0, 0)),
        (4, {
            "body": (1.5, -12, 4.3), "head": (-6, 12, -7.8),
            "right_arm": (110, 4, 7), "left_arm": (103.5, -12.5, -2),
            "cape_upper": (-17, 0, 0), "cape_mid": (-4, 0, 0),
            "cape_lower": (5, 0, 0), "hat_ribbons": (-45, 0, 0),
        }, (0, .15, 0)),
        (9, {
            "body": (2.2, -11.3, 5.5), "head": (-5.6, 11.4, -8.6),
            "right_arm": (109, 3, 7.5), "left_arm": (102.6, -12, -2.5),
            "cape_upper": (-15.5, 0, 1), "cape_mid": (-2, 0, 0),
            "cape_lower": (3, 0, -1), "hat_ribbons": (-44, 0, 0),
        }, (0, .05, 0)),
        (14, {
            "body": (4.1, -12.2, 6), "head": (-4.6, 12.3, -8.8),
            "right_arm": (106.8, 3.8, 7), "left_arm": (101.3, -12.2, -1.7),
            "cape_upper": (-20, 0, 1), "cape_mid": (-8, 0, -.5),
            "cape_lower": (-8, 0, -1.5), "hat_ribbons": (-48, 0, 0),
        }, (0, -.14, 0)),
        (19, {
            "body": (2.4, -12.7, 4.8), "head": (-6, 12.8, -8),
            "right_arm": (109, 3.8, 6.8), "left_arm": (103, -11.8, -2),
            "cape_upper": (-16.4, 0, .5), "cape_mid": (-1.8, 0, 0),
            "cape_lower": (6, 0, 0), "hat_ribbons": (-44, 0, 0),
        }, (0, .13, 0)),
        (23, {}, (0, 0, 0)),
    ],
    # Left/yellow leg leads in f0. The right/white leg leads after f8.
    # The arm on the other side swings forward, with hands turned down.
    "walk": [
        (0, {
            "body": (13, -2, 1), "head": (-12, 2, -1),
            "right_arm": (15, 0, 7), "left_arm": (-31, 0, -7),
            "right_hand": (5, -4, 0), "left_hand": (3, 4, 0),
            "right_leg": (-25, 2, 1), "left_leg": (32, -2, -2),
            "cape_upper": (-34, 0, 1), "cape_mid": (-8, 0, 0),
            "cape_lower": (5, 0, -1), "hat_ribbons": (-74, 0, 2),
        }, (0, -.35, 0)),
        (4, {
            "body": (11.7, -1, .5), "head": (-10.8, 1.3, -.5),
            "right_arm": (7, 0, 7), "left_arm": (-25, 0, -7),
            "right_hand": (5, -4, 0), "left_hand": (3, 4, 0),
            "right_leg": (-11, 2, 2), "left_leg": (18, -2, -2),
            "cape_upper": (-30, 0, 1), "cape_mid": (-9, 0, 0),
            "cape_lower": (1, 0, -1), "hat_ribbons": (-70, 0, 2),
        }, (0, .05, 0)),
        (8, {
            "body": (13.7, 2.8, -.4), "head": (-12.8, -3, .4),
            "right_arm": (-8, 0, 6), "left_arm": (2, 0, -7),
            "right_hand": (4, -4, 0), "left_hand": (4, 4, 0),
            "right_leg": (11, 2, 2), "left_leg": (-9, -2, -2),
            "cape_upper": (-35, 0, -1), "cape_mid": (-9, 0, -.5),
            "cape_lower": (1, 0, 0), "hat_ribbons": (-77, 0, -1),
        }, (0, .34, 0)),
        (12, {
            "body": (14, 3, -1), "head": (-12.5, -3.8, 1),
            "right_arm": (-27, 0, 7), "left_arm": (21, 0, -6),
            "right_hand": (3, -4, 0), "left_hand": (6, 4, 0),
            "right_leg": (32, 2, 2), "left_leg": (-33, -2, -2),
            "cape_upper": (-31, 0, -1), "cape_mid": (-10, 0, 0),
            "cape_lower": (6, 0, 1), "hat_ribbons": (-74, 0, -2),
        }, (0, -.72, 0)),
        (16, {
            "body": (12.7, 1.1, -.5), "head": (-12, -.5, .6),
            "right_arm": (-22, 0, 7), "left_arm": (14, 0, -6),
            "right_hand": (3, -4, 0), "left_hand": (6, 4, 0),
            "right_leg": (20, 2, 1), "left_leg": (-20, -2, -2),
            "cape_upper": (-31, 0, -1), "cape_mid": (-7, 0, 0),
            "cape_lower": (5, 0, 0), "hat_ribbons": (-75, 0, -1),
        }, (0, .06, 0)),
        (19, {
            "body": (13.5, -1.6, .5), "head": (-12.2, 1.5, -.5),
            "right_arm": (3, 0, 7), "left_arm": (-16, 0, -7),
            "right_hand": (5, -4, 0), "left_hand": (3, 4, 0),
            "right_leg": (-10, 2, 1), "left_leg": (14, -2, -2),
            "cape_upper": (-32, 0, 0), "cape_mid": (-9, 0, 0),
            "cape_lower": (3, 0, 0), "hat_ribbons": (-73, 0, 0),
        }, (0, .24, 0)),
        (21, {
            "body": (13, -2, 1), "head": (-12, 2, -1),
            "right_arm": (15, 0, 7), "left_arm": (-30, 0, -7),
            "right_hand": (5, -4, 0), "left_hand": (3, 4, 0),
            "right_leg": (-23, 2, 1), "left_leg": (30, -2, -2),
            "cape_upper": (-34, 0, 1), "cape_mid": (-8, 0, 0),
            "cape_lower": (5, 0, -1), "hat_ribbons": (-74, 0, 2),
        }, (0, -.27, 0)),
    ],
    # Single raised LEFT fist in the hold. The right sleeve first goes
    # forward and down, then retracts until the hand is beside the hip.
    "overcharge": [
        (0, {}, (0, 0, 0)),
        (10, {
            "body": (1, 17, -6), "head": (-4, -14, 4),
            "right_arm": (35, -8, 10), "left_arm": (117, -14, 20.6),
            "right_hand": (9, -6, 3), "left_hand": (9, 8, 15),
            "right_leg": (17, 5, 5), "left_leg": (-18, -7, -8),
            "cape_upper": (-19, 0, -6), "cape_mid": (-3, 0, 1),
            "cape_lower": (5, 0, 1), "hat_ribbons": (-35, 0, -1),
        }, (0, .02, .1)),
        (28, {
            "body": (0, 18, -5), "head": (-3, -13, 4),
            "right_arm": (31, -7, 10), "left_arm": (121, -12, 19.6),
            "right_hand": (9, -7, 3), "left_hand": (9, 8, 15),
            "right_leg": (19, 6, 6), "left_leg": (-18, -7, -8),
            "cape_upper": (-18, 0, -5), "cape_mid": (-3, 0, 1),
            "cape_lower": (5, 0, 1), "hat_ribbons": (-35, 0, -1),
        }, (0, -.02, .08)),
        (39, {
            "body": (2, 22, -8), "head": (9, -15, 7),
            "right_arm": (23, -10, 24), "left_arm": (159, -12.8, 23.4),
            "right_hand": (3, -9, 0), "left_hand": (-20, 5, 3),
            "right_leg": (19, 7, 7), "left_leg": (-19, -7, -8),
            "cape_upper": (-16, 0, -4), "cape_mid": (-6, 0, 1),
            "cape_lower": (1, 0, 2), "hat_ribbons": (-39, 0, 0),
        }, (0, .03, 0)),
        (46, {
            "body": (3, 25, -6), "head": (13, -17, 4),
            "right_arm": (4, -10, 11), "left_arm": (175, -14.5, 21.4),
            "right_hand": (1, -4, 1), "left_hand": (-30, 8, 6),
            "right_leg": (19, 7, 7), "left_leg": (-19, -8, -9),
            "cape_upper": (-12, 0, -4), "cape_mid": (-3, 0, 0),
            "cape_lower": (4, 0, 0), "hat_ribbons": (-41, 0, 0),
        }, (0, .15, 0)),
        (60, {
            "body": (3.2, 24, -6.4), "head": (12, -16, 4.6),
            "right_arm": (1, -9, 10), "left_arm": (176.5, -13.5, 21.4),
            "right_hand": (1, -4, 1), "left_hand": (-28, 8, 6),
            "right_leg": (19, 7, 7), "left_leg": (-19, -8, -9),
            "cape_upper": (-9, 0, -4), "cape_mid": (1, 0, 0),
            "cape_lower": (4, 0, 1), "hat_ribbons": (-40, 0, 0),
        }, (0, .13, 0)),
        (68, {
            "body": (3, 23, -7), "head": (11, -16, 5),
            "right_arm": (5, -9, 13), "left_arm": (169, -13.9, 21.7),
            "right_hand": (3, -4, 2), "left_hand": (-26, 7, 8),
            "right_leg": (18, 7, 7), "left_leg": (-19, -8, -9),
            "cape_upper": (-11, 0, -4), "cape_mid": (-1, 0, 0),
            "cape_lower": (3, 0, 1), "hat_ribbons": (-40, 0, 0),
        }, (0, .08, 0)),
        (78, {
            "body": (0, 0, 3), "head": (-6, 2, -3),
            "right_arm": (84, 9, 11), "left_arm": (143, -.3, 14.4),
            "right_hand": (1, -9, 8), "left_hand": (7, 7, 13),
            "right_leg": (-3, -1, 2), "left_leg": (11, -7, -5),
            "cape_upper": (-24, 0, 3), "cape_mid": (-8, 0, 1),
            "cape_lower": (-3, 0, 1), "hat_ribbons": (-43, 0, 0),
        }, (0, .14, 0)),
        (85, {}, (0, 0, 0)),
    ],
    # The two arms lift asymmetrically. The right fist leads the lift and
    # sits higher, while the left fist stays farther from the face.
    "summon": [
        (0, {}, (0, 0, 0)),
        (8, {
            "body": (-22, -17, 8), "head": (13, 11, -6),
            "right_arm": (127, 2, 10), "left_arm": (114, -15, -3),
            "right_hand": (9, -13, 4), "left_hand": (9, 8, 15),
            "right_leg": (-20, -8, 5), "left_leg": (14, -10, -4),
            "cape_upper": (-36, 0, 0), "cape_mid": (-11, 0, 0),
            "cape_lower": (-4, 0, 0), "hat_ribbons": (-45, 0, 0),
        }, (0, .1, .45)),
        (13, {
            "body": (6, 4, -6), "head": (12, -1, -8),
            "right_arm": (131, 5, -20), "left_arm": (128, -6, 12),
            "right_hand": (8, -9, 6), "left_hand": (9, 9, 13),
            "right_leg": (9, 3, 4), "left_leg": (-6, -8, -5),
            "cape_upper": (-27, 0, 0), "cape_mid": (-4, 0, 0),
            "cape_lower": (4, 0, 0), "hat_ribbons": (-29, 0, 0),
        }, (0, .12, -.12)),
        (14, {
            "body": (7, 11, -7), "head": (18, -7, -12),
            "right_arm": (154, -13.5, -27.5), "left_arm": (140, -7, 20),
            "right_hand": (9, -8, 6), "left_hand": (9, 8, 10),
            "right_leg": (9, 4, 5), "left_leg": (-6, -8, -6),
            "cape_upper": (-20, 0, 1), "cape_mid": (-6, 0, 0),
            "cape_lower": (4, 0, 0), "hat_ribbons": (-35, 0, 0),
        }, (0, .06, -.18)),
        (24, {
            "body": (5, 8, -4), "head": (14, -5, -8),
            "right_arm": (156, -8.3, -24), "left_arm": (141, -7, 21),
            "right_hand": (8, -8, 6), "left_hand": (10, 8, 12),
            "right_leg": (16, 6, 7), "left_leg": (-17, -8, -7),
            "cape_upper": (-28, 0, -1), "cape_mid": (-10, 0, 0),
            "cape_lower": (-6, 0, 0), "hat_ribbons": (-52, 0, -1),
        }, (0, .08, -.04)),
        (33, {
            "body": (4.5, 8, -3), "head": (13, -4, -7),
            "right_arm": (154, -6.1, -23.5), "left_arm": (141, -7, 20),
            "right_hand": (8, -8, 6), "left_hand": (10, 8, 12),
            "right_leg": (16, 6, 7), "left_leg": (-17, -8, -7),
            "cape_upper": (-27, 0, -1), "cape_mid": (-9, 0, 0),
            "cape_lower": (-5, 0, 0), "hat_ribbons": (-49, 0, -1),
        }, (0, .08, 0)),
        (38, {
            "body": (1, 4, 4), "head": (2, 2, -2),
            "right_arm": (120, 7, 1), "left_arm": (88, -9, -8),
            "right_hand": (10, -10, 6), "left_hand": (12, 7, 15),
            "right_leg": (15, 5, 6), "left_leg": (-22, -8, -7),
            "cape_upper": (-35, 0, 2), "cape_mid": (-9, 0, 1),
            "cape_lower": (-4, 0, 0), "hat_ribbons": (-62, 0, 0),
        }, (0, .12, .18)),
        (44, {
            "body": (-18, -9, 5), "head": (12, 10, -8),
            "right_arm": (118, 6, 8), "left_arm": (113, -13, -3),
            "right_hand": (5, -10, 8), "left_hand": (7, 8, 14),
            "right_leg": (-8, -2, 5), "left_leg": (2, -8, -5),
            "cape_upper": (-41, 0, 3), "cape_mid": (-8, 0, 1),
            "cape_lower": (-8, 0, 1), "hat_ribbons": (-57, 0, 0),
        }, (0, .12, .1)),
        (53, {}, (0, 0, 0)),
    ],
}
