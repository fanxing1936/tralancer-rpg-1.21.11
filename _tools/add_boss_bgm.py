# -*- coding: utf-8 -*-
"""Boss 战各自的背景音乐（用户 2026-11-21「这些 boss 的 BGM 用的都相同，你在从网上找一些 bgm 使用并下载」）。

    python add_boss_bgm.py ../resourcepack

曲子在 _tools/bgm_ref/（来源与许可见 bgm_ref/SOURCES.md，全是 CC0 或 CC-BY），原样拷进
assets/rpg/sounds/bgm/，在 assets/rpg/sounds.json 里登记 rpg:bgm.<boss><段> 事件（流式播放：长曲整段解码会卡客户端）。
各 Boss 生成器的 STAGES 里写的就是这些事件名和长度（刻，向上取整）；教皇战仍用原来的 minecraft:boss1..3。
"""
import io
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "bgm_ref")
TRACKS = ["michael1", "michael2", "saul1", "saul2", "jacques1", "jacques2",
          "lucifer1", "lucifer2", "usurper1", "usurper2"]


def main(pack):
    out = os.path.join(pack, "assets", "rpg", "sounds", "bgm")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(pack, "assets", "rpg", "sounds.json")
    sounds = {}
    if os.path.isfile(path):
        with io.open(path, encoding="utf-8-sig") as fh:
            sounds = json.load(fh)
    for t in TRACKS:
        src = os.path.join(REF, t + ".ogg")
        with open(src, "rb") as fh:
            assert fh.read(4) == b"OggS", src
        shutil.copyfile(src, os.path.join(out, t + ".ogg"))
        sounds["bgm." + t] = {"sounds": [{"name": "rpg:bgm/" + t, "stream": True}]}
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(sounds, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    # CC-BY 要求署名：资源包里随曲子放一份来源说明
    shutil.copyfile(os.path.join(REF, "SOURCES.md"), os.path.join(out, "CREDITS.md"))
    print("boss bgm: %d tracks" % len(TRACKS))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../resourcepack")
