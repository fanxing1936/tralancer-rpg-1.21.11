# -*- coding: utf-8 -*-
"""Static meshes a Dungeons character blueprint hangs on its skeleton (helmets, shields, armour, spears).

    atts = blueprint_attachments(export_root, "Dungeons/Content/.../BP_SkeletonVanguardCharacter",
                                 socket_roots=[...], names={"Shield": "shield"})
    generic.convert(..., attachments=atts)

Reads the exported blueprint's SimpleConstructionScript: every SCS node attached to CharacterMesh0
(`AttachToName` = a bone or a skeleton socket) whose template is a StaticMeshComponent, or a
ChildActorComponent whose actor has StaticMeshComponents.  Each result is

    {"name": part name, "mesh": glb path, "bone": bone name, "matrix": 4x4 UE matrix relative to the bone,
     "material": override material name or None}

Transforms compose like UE attachment: bone @ socket @ component relative (@ child actor component).
UE FRotator to quaternion follows FRotator::Quaternion(); matrices are column-vector, matching
source_math.quat_matrix and generic.ue_world.
"""

import json
import math
import os
from pathlib import Path

import numpy as np

from source_math import quat_matrix


def _read(path):
    return json.load(open("\\\\?\\" + os.path.abspath(path), encoding="utf-8"))


def rotator_quat(rot):
    """UE FRotator {Pitch, Yaw, Roll} in degrees -> (x, y, z, w)."""
    p, y, r = (math.radians(float((rot or {}).get(k, 0.0))) / 2 for k in ("Pitch", "Yaw", "Roll"))
    sp, cp, sy, cy, sr, cr = math.sin(p), math.cos(p), math.sin(y), math.cos(y), math.sin(r), math.cos(r)
    return [cr * sp * sy - sr * cp * cy, -cr * sp * cy - sr * cp * sy, cr * cp * sy - sr * sp * cy, cr * cp * cy + sr * sp * sy]


def relative(props):
    """T @ R @ S of a SceneComponent's Relative* properties."""
    loc = props.get("RelativeLocation") or {}
    scale = props.get("RelativeScale3D") or props.get("RelativeScale") or {}
    m = np.eye(4)
    m[:3, :3] = quat_matrix(rotator_quat(props.get("RelativeRotation"))) @ np.diag(
        [float(scale.get(k, 1.0)) for k in "XYZ"])
    m[:3, 3] = [float(loc.get(k, 0.0)) for k in "XYZ"]
    return m


def _object_path(ref):
    """'Dungeons/Content/.../SM_X.2' -> 'Dungeons/Content/.../SM_X'"""
    path = ref["ObjectPath"]
    return path.rsplit(".", 1)[0] if path.rsplit(".", 1)[-1].isdigit() else path


def _material(props):
    over = [m for m in props.get("OverrideMaterials") or [] if m]
    return over[0]["ObjectName"].split("'")[1] if over else None


def sockets(socket_roots):
    """{socket name: (bone name, 4x4)} from exported SkeletalMeshSocket objects."""
    out = {}
    for root in socket_roots:
        for p in Path(root).rglob("SkeletalMeshSocket_*.uobject.json"):
            props = _read(p).get("Properties") or {}
            if props.get("SocketName") and props.get("BoneName"):
                out.setdefault(props["SocketName"], (props["BoneName"], relative(props)))
    return out


def _components(bp_meta_dir):
    """{variable name: (SCS properties, template properties)} of one blueprint."""
    out = {}
    for node in Path(bp_meta_dir).glob("SCS_Node_*.uobject.json"):
        props = _read(node).get("Properties") or {}
        name = props.get("InternalVariableName")
        template = Path(bp_meta_dir) / (name + "_GEN_VARIABLE.uobject.json")
        if name and template.exists():
            out[name] = (props, _read(template).get("Properties") or {})
    return out


def blueprint_attachments(export_root, blueprint, *, bones, socket_roots=(), names=None, skip=()):
    """blueprint: the BP path under the export (no extension).  bones: bone names of the mesh.
    names maps a component variable name to the part name it should get (default: lower case)."""
    root = Path(export_root)
    names = names or {}
    socket_map = sockets(list(socket_roots) + [root / "metadata"])
    found = []
    for var, (scs, props) in sorted(_components(root / "metadata" / blueprint).items()):
        if scs.get("ParentComponentOrVariableName") != "CharacterMesh0" or not scs.get("AttachToName") or var in skip:
            continue
        attach = scs["AttachToName"]
        if attach in bones:
            bone, socket = attach, np.eye(4)
        elif attach in socket_map:
            bone, socket = socket_map[attach]
        else:
            raise KeyError("%s: attach point %s is neither a bone nor a known socket" % (var, attach))
        base = socket @ relative(props)
        meshes = []
        if props.get("StaticMesh"):
            meshes.append((var, _object_path(props["StaticMesh"]), np.eye(4), _material(props)))
        elif props.get("ChildActorClass"):
            child = _object_path(props["ChildActorClass"])
            for cvar, (_cscs, cprops) in sorted(_components(root / "metadata" / child).items()):
                if cprops.get("StaticMesh"):
                    meshes.append((var if len(meshes) == 0 else var + "_" + cvar, _object_path(cprops["StaticMesh"]),
                                   relative(cprops), _material(cprops)))
        for part, mesh, local, material in meshes:
            glb = root / "assets" / (mesh + ".glb")
            if not glb.exists():
                raise FileNotFoundError(glb)
            found.append({"name": names.get(part, part.lower()), "mesh": glb, "bone": bone,
                          "matrix": base @ local, "material": material, "component": var, "attach": attach})
    return found
