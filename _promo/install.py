# -*- coding: utf-8 -*-
"""把拍摄用的存档和资源包装进本机实例，全部用宣传片自己的名字。

    python _promo/install.py            # 首次：复制存档 + 资源包
    python _promo/install.py --refresh  # 只刷新存档里的两个数据包和资源包

- 存档：从「新的世界」复制成「破碎大陆-宣传片拍摄」，原存档只读不碰；
  datapacks/ 换成本分支的 rpg/（tralancer-rpg）和 _promo/datapack/（promo）。
- 资源包：本分支的 resourcepack/ 复制成 resourcepacks/tralancer-rpg-promo。
- 不改 options.txt / iris.properties：录制时在游戏里手动选资源包和光影。
"""
import gzip
import os
import shutil
import struct
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_tools"))
from mc_env import INST  # noqa: E402

SRC_WORLD = "新的世界"
WORLD = "破碎大陆-宣传片拍摄"
PACK = "tralancer-rpg-promo"
# 别的会话在用的测试环境，任何情况下都不写
PROTECTED = {"新的世界", "破碎大陆-美术风格检查", "tralancer-rpg", "tralancer-rpg-artstyle"}


def game_running():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq javaw.exe"],
                         capture_output=True, text=True, errors="replace").stdout
    return "javaw.exe" in out


def rename_level(world, name):
    """改 level.dat 里的 LevelName，免得存档列表里出现两个「新的世界」。

    TAG_String = 0x08 + 名字长度(u16) + "LevelName" + 值长度(u16) + 值（UTF-8）。
    """
    path = os.path.join(world, "level.dat")
    with gzip.open(path, "rb") as f:
        data = f.read()
    key = b"\x08" + struct.pack(">H", 9) + b"LevelName"
    at = data.index(key) + len(key)
    old_len = struct.unpack(">H", data[at:at + 2])[0]
    new = name.encode("utf-8")
    data = data[:at] + struct.pack(">H", len(new)) + new + data[at + 2 + old_len:]
    with gzip.open(path, "wb") as f:
        f.write(data)


def replace_tree(src, dst):
    assert os.path.basename(dst) not in PROTECTED, dst
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    if game_running():
        sys.exit("客户端正在运行，先退出游戏再装。")
    refresh = "--refresh" in sys.argv
    saves = os.path.join(INST, "saves")
    world = os.path.join(saves, WORLD)
    if not os.path.isdir(world):
        if refresh:
            sys.exit("还没有拍摄存档，先不带 --refresh 跑一次。")
        shutil.copytree(os.path.join(saves, SRC_WORLD), world)
        rename_level(world, WORLD)
        print("copied world ->", world)
    packs = os.path.join(world, "datapacks")
    for name in os.listdir(packs):
        p = os.path.join(packs, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    shutil.copytree(os.path.join(ROOT, "rpg"), os.path.join(packs, "tralancer-rpg"))
    shutil.copytree(os.path.join(ROOT, "_promo", "datapack"), os.path.join(packs, "promo"))
    print("datapacks ->", packs)
    replace_tree(os.path.join(ROOT, "resourcepack"), os.path.join(INST, "resourcepacks", PACK))
    print("resource pack ->", PACK)


if __name__ == "__main__":
    main()
