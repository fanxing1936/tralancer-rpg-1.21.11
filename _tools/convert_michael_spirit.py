"""Convert the original Dungeons hero and Frost Armor with the TRA Michael weapon pair."""

import argparse
import copy
import json
import struct
from pathlib import Path

import numpy as np
from PIL import Image

from dungeons_conversion import generic as G
from dungeons_conversion import blueprint as BP

HERE = Path(__file__).resolve().parent
KEY = "michael_spirit"
UNIT_SCALE = 0.0192
HEIGHT_BLOCKS = 1.87
SOURCE_CONTENT = Path("Dungeons/Content")
MASTER = Path("Actors/Characters/Player/Master")
EQUIPMENT = Path("Actors/Equipment")
FROST = EQUIPMENT / "Armor/SnowArmor_Unique1"
HERO_SOURCE = MASTER / "SK_Player_Master"
ARMOR_ROLES = {
    "FrostArmor_Body": "frost_body", "FrostArmor_Head": "frost_helmet",
    "FrostArmor_Arm_L": "frost_l_arm", "FrostArmor_Arm_R": "frost_r_arm",
    "FrostArmor_Leg_L": "frost_r_leg", "FrostArmor_Leg_R": "frost_l_leg",
}
CLIPS = (
    ("Idle_Glaive", "idle", True), ("Walk_Glaive", "walk", True), ("Run_Glaive", "run", True),
    ("GlaiveUnique1Combo_Attack1", "slash1", False), ("GlaiveUnique1Combo_Attack2", "slash2", False),
    ("GlaiveUnique1Combo_Attack3", "sweep", False),
    ("Idle", "rib_idle", True), ("Walk", "rib_walk", True), ("Run", "rib_run", True),
    *((f"DaggersComboDeluxe_{index}", f"rib_slash{index}", False) for index in range(1, 7)),
    ("DodgeRollForward", "roll_f", False), ("DodgeRollBackward", "roll_b", False),
    ("DodgeRollSidewayLeft", "roll_l", False), ("DodgeRollSidewayRight", "roll_r", False),
    ("GetHitFront", "hurt", False), ("DownedFloor_Initiate", "fall", False),
    ("DownedFloored_Loop", "down", True),
)


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def wrap_export(path, target):
    """Wrap the original UModel glTF + external geometry buffer into the converter's GLB input."""
    doc = G.read(path)
    buffer, = doc["buffers"]
    binary = (path.parent / buffer.pop("uri")).read_bytes()
    if len(binary) != buffer["byteLength"]:
        raise ValueError(f"Invalid glTF buffer length for {path}")
    payload = json.dumps(doc, separators=(",", ":")).encode()
    payload += b" " * (-len(payload) % 4)
    binary += b"\0" * (-len(binary) % 4)
    target.write_bytes(struct.pack("<4sII", b"glTF", 2, 28 + len(payload) + len(binary))
                       + struct.pack("<I4s", len(payload), b"JSON") + payload
                       + struct.pack("<I4s", len(binary), b"BIN\0") + binary)
    return target


def spirit_texture(source, out, opacity, palette):
    albedo = np.array(Image.open(source).convert("RGBA"))
    luminance = (albedo[..., :3] @ [0.2126, 0.7152, 0.0722]) / 255.0
    low, high = opacity
    alpha = np.rint(albedo[..., 3] * (low + (high - low) * luminance))
    if len(palette) == 1:
        albedo[..., :3] = palette[0]
    else:
        # Map the source texture's dark details, midtones, and bright edges separately.
        for channel, stops in enumerate(zip(*palette)):
            albedo[..., channel] = np.rint(np.interp(luminance, (0.10, 0.55, 0.94), stops))
    albedo[..., 3] = alpha.astype(np.uint8)
    Image.fromarray(albedo).save(out)
    return out


def components(path):
    parsed = G.read(path)
    exports = {entry["index"]: entry for entry in parsed["exports"]}
    for node in exports.values():
        if not node["name"].startswith("SCS_Node_"):
            continue
        links = {prop["name"]: prop["value"] for prop in node["properties"]}
        if "AttachToName" not in links:
            continue
        component = exports[links["ComponentTemplate"]["index"]]
        properties = {prop["name"]: prop["value"] for prop in component["properties"]}
        referenced_mesh = properties.get("StaticMesh", properties.get("SkeletalMesh"))
        if not referenced_mesh:
            continue
        package = Path(referenced_mesh["path"].removeprefix("/Game/").split(".", 1)[0])
        relative = {key: dict(zip(axes, properties[key])) for key, axes in (
            ("RelativeLocation", "XYZ"), ("RelativeScale3D", "XYZ"),
            ("RelativeRotation", ("Pitch", "Yaw", "Roll"))) if key in properties}
        yield package, links["AttachToName"], BP.relative(relative), component["name"]


def attachment(name, package, bone, matrix, material, socket, component, mesh_for):
    return {"name": name, "mesh": mesh_for(package), "bone": bone, "matrix": matrix,
            "material": material, "attach": socket, "component": component, "package": package.as_posix()}


def resolve_attachments(work, metadata, mesh_for):
    sockets = BP.sockets([metadata / MASTER / "Player_Master_Skeleton"])
    result = []
    for package, socket, relative, component in components(work / "BP_SnowArmor_Unique1.parsed.json"):
        bone, socket_matrix = sockets[socket]
        result.append(attachment(ARMOR_ROLES[package.name], package, bone, socket_matrix @ relative,
                                 "FROST", socket, component, mesh_for))
    weapons = work / "custom_weapons"
    (_, _, glaive_basis, _), = components(work / "BP_Glaive_Unique1.parsed.json")
    # The centered custom blade runs +Y, while the original Glaive blade runs -Y.
    glaive_basis = glaive_basis @ np.diag([-1., -1., 1., 1.])
    # Align the rib's +Y blade axis and +Z face normal to the source dagger's -Z and +X axes.
    dagger_left = np.eye(4)
    dagger_left[:3, :3] = [[0, 0, 1], [-1, 0, 0], [0, -1, 0]]
    dagger_right = BP.relative({"RelativeRotation": {"Yaw": -180.0}}) @ dagger_left
    for name, asset, socket in (("spine", "spine", "J_R_Weapon_Socket"),
                                ("rib", "rib", "J_L_Weapon_Socket"),
                                ("rib_attack", "rib", "J_R_Weapon_Socket")):
        bone, socket_matrix = sockets[socket]
        mesh = weapons / f"{asset}.glb"
        basis = {"spine": glaive_basis, "rib": dagger_left, "rib_attack": dagger_right}[name]
        matrix = np.eye(4)
        matrix[:3, :3] = socket_matrix[:3, :3] @ (basis[:3, :3] / np.linalg.norm(basis[:3, :3], axis=0))
        result.append({"name": name, "mesh": mesh, "bone": bone, "matrix": matrix,
                       "material": asset.upper(), "attach": socket, "component": asset,
                       "package": f"TRA/{asset}"})
    return result


def resolve_inputs(work, source):
    """Prepared GLBs, baked-orange PNGs and attachment transforms for Java and native Blockbench."""
    work, source = Path(work).resolve(), Path(source).resolve()
    fresh = work / "exported" / "Game"
    prepared = work / "prepared"
    prepared.mkdir(exist_ok=True)

    def mesh_for(package):
        return wrap_export(fresh / package.with_suffix(".gltf"), prepared / package.with_suffix(".glb").name)

    meta_root = source / "metadata"
    attachments = resolve_attachments(work, meta_root / SOURCE_CONTENT, mesh_for)
    if len(attachments) != 9:
        raise ValueError("Expected six Frost Armor parts and three weapon attachments")
    weapons = work / "custom_weapons"
    texture_specs = {
        "MI_Valorie": (fresh / MASTER / "Skins/Nephrologist/T_Nephrologist_Skin.png", (.18, .34), ((255, 245, 238),)),
        "FROST": (fresh / FROST / "T_SnowArmor_Unique1.png", (.19, .43),
                  ((255, 51, 0), (255, 128, 95), (255, 208, 189))),
        "SPINE": (weapons / "spine.png", (.32, .48), ((255, 51, 0),)),
        "RIB": (weapons / "rib.png", (.32, .48), ((255, 51, 0),)),
    }
    textures = {material: spirit_texture(path, prepared / f"{material}.png", opacity, palette)
                for material, (path, opacity, palette) in texture_specs.items()}
    return {
        "mesh": mesh_for(HERO_SOURCE), "meta": meta_root / SOURCE_CONTENT / HERO_SOURCE / "SK_Player_Master.meta.json",
        "attachments": attachments, "material_textures": textures,
        "material_colors": {name: {"palette": palette, "opacity": opacity}
                            for name, (_, opacity, palette) in texture_specs.items()},
        "animation_metadata_roots": [meta_root, work / "cue_daggers" / "metadata"], "unit_scale": UNIT_SCALE,
        "clips": [(f"Player_Master_{source_name}", clip, loop) for source_name, clip, loop in CLIPS],
    }


def serial_attachment(attachment):
    return dict(attachment, mesh=str(attachment["mesh"]), matrix=attachment["matrix"].tolist())


def write_native_inputs(work, inputs):
    handoff = dict(inputs, mesh=str(inputs["mesh"]), meta=str(inputs["meta"]),
                   attachments=[serial_attachment(a) for a in inputs["attachments"]],
                   material_textures={k: str(v) for k, v in inputs["material_textures"].items()},
                   animation_metadata_roots=[str(p) for p in inputs["animation_metadata_roots"]])
    write_json(work / "native_inputs.json", handoff)


def convert(inputs, source, out):
    mesh, meta, attachments = (inputs[k] for k in ("mesh", "meta", "attachments"))
    doc, report = G.convert(mesh, meta, source, out, name=KEY, unit_scale=UNIT_SCALE,
                            attachments=copy.deepcopy(attachments),
                            material_textures_override={k: (v, None) for k, v in inputs["material_textures"].items()})
    hero, _ = G.load_any(mesh, meta)
    source_height = float(np.ptp(hero["vertices_ue_cm"][:, 2]))
    scale = HEIGHT_BLOCKS * 16 / (source_height * UNIT_SCALE)
    doc, clips = G.author(doc, meta, mesh, inputs["animation_metadata_roots"], inputs["clips"], model_scale=scale)
    doc["display_dungeons"]["model_scale"] = scale
    for cube in doc["elements"]:
        for face in ("north", "east", "south", "west", "up", "down"):
            cube["faces"].setdefault(face, {"texture": None, "uv": [0, 0, 0, 0]})
    doc["textures"][0]["render_mode"] = "translucent"
    write_json(out / f"{KEY}.bbmodel", doc)
    write_json(out / "model_config.json", {
        "model_scale": scale, "height_blocks": HEIGHT_BLOCKS, "source_height_cm": source_height, "turn": 0,
        "merge": {}, "held_bone": None,
        "attachments": [serial_attachment(a) for a in attachments],
        "source": {"mesh": str((SOURCE_CONTENT / HERO_SOURCE).as_posix()),
                   "skin": "Nephrologist (Cloudwatcher)", "export_root": str(source)},
        "material_colors": inputs["material_colors"],
        "clips": clips, "conversion": report,
    })
    print(f"{KEY}: {report['display_parts']} display parts, {report['triangles']} source triangles, {len(clips)} clips")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path, help="Root containing fresh UModel exports and parsed Frost Armor blueprint")
    parser.add_argument("--source", type=Path, default=Path("D:/agent/dungeons_extract/upgrade/jacques"),
                        help="Existing player socket, skeleton and original animation track metadata export")
    parser.add_argument("--out", type=Path, default=HERE / f"{KEY}_dungeons_ref")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    inputs = resolve_inputs(args.work, args.source)
    write_native_inputs(args.work, inputs)
    if not args.prepare_only:
        convert(inputs, args.source, args.out)


if __name__ == "__main__":
    main()
