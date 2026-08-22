# -*- coding: utf-8 -*-
"""Zip the built data pack and resource pack, and install them into the
1.21.11 instance.  Deterministic ordering so a rebuild that changed nothing
produces an identical archive."""

import os
import shutil
import sys
import zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INST = r"F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric"

TARGETS = [
    ("rpg", "rpg-datapack-1.21.11.zip"),
    ("resourcepack", "rpg-resourcepack-1.21.11.zip"),
]


def pack(src, dst):
    src = os.path.join(ROOT, src)
    dst = os.path.join(ROOT, dst)
    if os.path.exists(dst):
        os.remove(dst)
    n = 0
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, dirs, files in os.walk(src):
            dirs.sort()
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, src).replace(os.sep, "/")
                z.write(p, rel)
                n += 1
    print("%-34s %5d files  %7.1f KB"
          % (os.path.basename(dst), n, os.path.getsize(dst) / 1024.0))
    return dst


def copy_tree(src, dst):
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    zips = [pack(s, d) for s, d in TARGETS]
    if "--install" not in sys.argv:
        return
    dp_zip, rp_zip = zips

    # the resource pack ships as a zip the launcher can select directly
    dest = os.path.join(INST, "resourcepacks", os.path.basename(rp_zip))
    if not os.path.isdir(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    shutil.copyfile(rp_zip, dest)
    print("installed -> " + dest)

    saves = os.path.join(INST, "saves")
    if not os.path.isdir(saves):
        print("no saves directory at " + saves)
        return
    for world in sorted(os.listdir(saves)):
        packs = os.path.join(saves, world, "datapacks")
        if not os.path.isdir(packs):
            continue
        # whichever form that world already uses -- unpacked folder or zip
        folder = os.path.join(packs, "rpg")
        if os.path.isdir(folder):
            copy_tree(os.path.join(ROOT, "rpg"), folder)
            print("installed -> " + folder)
        zipped = os.path.join(packs, os.path.basename(dp_zip))
        if os.path.isfile(zipped):
            shutil.copyfile(dp_zip, zipped)
            print("installed -> " + zipped)


if __name__ == "__main__":
    main()
