"""首席附魔师本体。盒件用静态原件与动作帧可见形状拟合，UV 指向 64² 原图。"""

SIDE_FACES = ("east", "north", "west", "south")
HEAD_CHILDREN = ("hat_right_flap", "hat_left_flap", "hat_back_flap", "head_glow")

PIVOTS = {
    "body": (0, 12, 0),
    "head": (0, 24, 0),
    "right_arm": (6, 22.3, 0),
    "left_arm": (-6, 22.3, 0),
    "right_hand": (6, 14.3, 0),
    "left_hand": (-6, 14.3, 0),
    "right_leg": (2, 12, 0),
    "left_leg": (-2, 12, 0),
}

# Local rotations in degrees. The near (character-left) fist is held across
# the chest. The far right fist is higher and rolled toward the face.
REST = {
    "body": (3, -13, 5),
    "head": (-5, 13, -8),
    "right_arm": (108, 4, 7),
    "left_arm": (102, -12, -2),
    "right_hand": (3, -14, 8),
    "left_hand": (1, 8, 12),
    "right_leg": (-14, -9, 1),
    "left_leg": (14, -10, -1),
}


def sides(u, v, width, depth, height):
    """Four faces from the observed right, front, left, back strip."""
    cuts = (u, u + depth, u + depth + width, u + 2 * depth + width,
            u + 2 * depth + 2 * width)
    return {name: [a, v, b, v + height]
            for name, a, b in zip(SIDE_FACES, cuts, cuts[1:])}


def box(u, v, width, depth, height):
    """Box side strip plus the pair of upper tiles in the source atlas."""
    return dict(sides(u, v, width, depth, height),
                up=[u + depth, v - depth, u + depth + width, v],
                down=[u + depth + width, v, u + depth + 2 * width, v - depth])


def front_patch(rig, bone, name, x0, y0, x1, y1, z, uv):
    rig.cube(bone, name, (x0, y0, z), (x1, y1, z + .004), {"north": uv})


def build_head(rig):
    rig.cube("head", "gray_head", (-4, 24, -4), (4, 36, 4), box(0, 8, 8, 8, 12))
    # This open overlay shares the head's 8x8 footprint and is enlarged
    # slightly to keep the borders visible above the opaque head surface.
    hat = sides(13, 50, 8, 8, 12)
    hat["up"] = [21, 50, 29, 42]
    rig.cube("head", "red_hat_shell", (-4.12, 23.92, -4.12), (4.12, 36.16, 4.12), hat)

    rig.cube("head", "long_nose", (-1, 24.25, -5.92), (1, 28.25, -3.92), box(24, 2, 2, 2, 4))
    # A thin light-gray strip sits below each brow. The white island is
    # reserved for the inner glow seen beside the nose in the intro close-up.
    for side, sign in (("right", 1), ("left", -1)):
        x_outer, x_inner = sign * 3.38, sign * 1.01
        x0, x1 = sorted((x_outer, x_inner))
        front_patch(rig, "head", side + "_eye_white", x0, 27.36, x1, 27.87, -4.028, [23, 29, 24, 30])
        # The original 3×2 island has a transparent upper inner pixel.
        # North U runs from the character's right toward their left.
        brow0, brow1 = sorted((sign * 1.0, sign * 3.76))
        front_patch(rig, "head", side + "_brow", brow0, 27.87, brow1, 29.39, -4.052,
                    [5, 4, 8, 6] if sign > 0 else [8, 4, 5, 6])
        gl0, gl1 = sorted((sign * 1.01, sign * 1.82))
        front_patch(rig, "head_glow", side + "_inner_pupil", gl0, 27.36, gl1, 27.78, -4.038, [7, 6, 8, 8])
        socket0, socket1 = sorted((sign * .86, sign * 2.1))
        front_patch(rig, "head", side + "_nose_socket", socket0, 25.0, socket1, 26.0, -4.017, [2, 6, 6, 8])

    front_patch(rig, "head_glow", "cyan_soul_core", -.998, 31.0, .998, 35.0, -4.04, [11, 9, 13, 13])
    # Source islands show matched narrow side flaps and a wider rear flap.
    # These are single-axis child bones because display_mob bakes rigid
    # children into the head's item model rather than using cube rotation.
    rig.cube("hat_right_flap", "right_hat_flap", (4.11, 24.33, -3.45), (4.24, 29.3, 3.55),
             {"east": [35, 1, 42, 6], "west": [42, 1, 35, 6]})
    rig.cube("hat_left_flap", "left_hat_flap", (-4.24, 24.33, -3.45), (-4.11, 29.3, 3.55),
             {"west": [35, 13, 42, 18], "east": [42, 13, 35, 18]})
    rig.cube("hat_back_flap", "rear_hat_flap", (-4.04, 24.33, 4.11), (4.04, 29.3, 4.24),
             {"south": [34, 7, 42, 12], "north": [42, 7, 34, 12]})


def build_arm(rig, side, x):
    arm = side + "_arm"
    hand = side + "_hand"
    shift = PIVOTS[arm][1] - 23

    def cube(bone, name, lo, hi, faces):
        rig.cube(bone, name, (lo[0], lo[1] + shift, lo[2]), (hi[0], hi[1] + shift, hi[2]), faces)

    sleeve = sides(46, 26, 4, 4, 8)
    sleeve["up"] = [50, 22, 54, 26]
    cube(arm, side + "_red_sleeve", (x - 2, 15, -2), (x + 2, 23, 2), sleeve)
    # Each edge is fixed at the top. The four panels open at the hem,
    # exposing the small wedges of sleeve visible in the reference.
    top, hem, width, thickness = 23.26, 19.15, 2.12, .075
    cube(arm, side + "_shoulder_top", (x-width, top-thickness, -width),
         (x+width, top, width), {"up": [51, 43, 55, 47]})
    shoulder = sides(47, 47, 4, 4, 4)
    panels = (
        ("north", (x, top, -width), (7.5, 0, 0),
         (x-width, hem, -width), (x+width, top, -width+thickness)),
        ("south", (x, top, width), (-6, 0, 0),
         (x-width, hem, width-thickness), (x+width, top, width)),
        ("east", (x+width, top, 0), (0, 0, 7.5),
         (x+width-thickness, hem, -width), (x+width, top, width)),
        ("west", (x-width, top, 0), (0, 0, -7.5),
         (x-width, hem, -width), (x-width+thickness, top, width)),
    )
    for face, hinge, rotation, lo, hi in panels:
        bone = f"{side}_shoulder_{face}"
        rig.bone(bone, (hinge[0], hinge[1] + shift, hinge[2]), parent=arm, rotation=rotation)
        cube(bone, bone, lo, hi, {face: shoulder[face]})
    fist = sides(46, 34, 4, 4, 4)
    fist["down"] = [54, 26, 58, 22]
    cube(hand, side + "_gray_fist", (x - 1.88, 11.12, -1.9), (x + 1.88, 15.03, 1.9), fist)

    # 4 rows of the original wrist strip have the horizontal dark/light
    # wrapping visible on straight and raised fists. Reusing it on inner
    # sides is a reconstruction where the atlas is not a closed box net.
    cuff = {name: [54, 59, 58, 63] for name in SIDE_FACES}
    cube(hand, side + "_brown_cuff", (x - 2.13, 11.72, -2.13),
             (x + 2.13, 15.06, 2.13), cuff)
    # The wrist wrap leaves the grey strike surface exposed. Small knuckle
    # rim pieces cover the visibly brown outside of the grey distal face.
    rim = [47, 60, 52, 61]
    outside_x = x + (1.39 if x > 0 else -2.13)
    inside_x = x + (2.13 if x > 0 else -1.39)
    cube(hand, side + "_outer_knuckle_rim", (outside_x, 11.09, -2.13),
             (inside_x, 11.74, 2.13), {"down": rim, "east" if x > 0 else "west": [63, 59, 64, 64]})
    cube(hand, side + "_knuckle_top_rim", (x - 1.42, 11.09, 1.52),
             (x + 1.42, 11.74, 2.13), {"down": [63, 59, 64, 64], "south": rim})


def build_leg(rig, side, x, v):
    leg = side + "_leg"
    rig.cube(leg, side + "_trouser_and_boot", (x - 1.97, 0, -1.99),
             (x + 1.97, 12, 1.99), box(0, 26, 4, 4, 12))

    # Each coat panel has a 3 px wide extension over the hip and a strip
    # 11 px wide. The 3+4+4 reading is tested against the open inner seam.
    front = [1, v + 4, 4, v + 12]
    side_uv = [4, v + 4, 8, v + 12]
    back = [8, v + 4, 12, v + 12]
    front_x0, front_x1 = ((x - 1.18, x + 2.09) if x > 0 else (x - 2.09, x + 1.18))
    if x > 0:
        front = [front[2], front[1], front[0], front[3]]
    front_bone = side + "_skirt_front"
    outer_bone = side + "_skirt_outer"
    back_bone = side + "_skirt_back"
    rig.bone(front_bone, (x, 11.96, -2.12), parent=leg, rotation=(5, 0, 0))
    rig.bone(outer_bone, (x + (2.07 if x > 0 else -2.07), 11.96, 0), parent=leg,
             rotation=(0, 0, 5 if x > 0 else -5))
    rig.bone(back_bone, (x, 11.96, 2.10), parent=leg, rotation=(-5, 0, 0))
    rig.cube(front_bone, side + "_coat_front", (front_x0, 3.23, -2.17),
             (front_x1, 10.75, -2.07), {"north": front})
    rig.cube(front_bone, side + "_coat_hip_tab", (front_x0, 10.75, -2.15),
             (front_x1, 11.96, -2.06), {"north": [1, v, 4, v + 4]})

    shell_x0, shell_x1 = (x + 2.02, x + 2.12) if x > 0 else (x - 2.12, x - 2.02)
    shell_side = "east" if x > 0 else "west"
    rig.cube(outer_bone, side + "_coat_outer_side", (shell_x0, 3.23, -2.15),
             (shell_x1, 10.75, 2.14), {shell_side: side_uv})
    rig.cube(back_bone, side + "_coat_back", (x - 2.09, 3.23, 2.05),
             (x + 2.09, 10.75, 2.15), {"south": back})


def build_body(rig):
    """Build the eight main independently movable display parts."""
    for bone, parent in (
        ("body", "root"), ("head", "body"),
        ("right_arm", "body"), ("left_arm", "body"),
        ("right_hand", "right_arm"), ("left_hand", "left_arm"),
        ("right_leg", "root"), ("left_leg", "root"),
    ):
        rig.bone(bone, PIVOTS[bone], parent=parent, rotation=REST[bone])

    rig.bone("hat_right_flap", (4.15, 24.33, 0), parent="head", rotation=(0, 0, -16))
    rig.bone("hat_left_flap", (-4.15, 24.33, 0), parent="head", rotation=(0, 0, 16))
    rig.bone("hat_back_flap", (0, 24.33, 4.15), parent="head", rotation=(10, 0, 0))
    rig.bone("head_glow", PIVOTS["head"], parent="head")

    rig.cube("body", "red_tunic", (-4, 12, -3), (4, 24, 3), box(16, 26, 8, 6, 12))
    build_head(rig)
    build_arm(rig, "right", 6)
    build_arm(rig, "left", -6)
    build_leg(rig, "right", 2, 51)
    build_leg(rig, "left", -2, 39)
