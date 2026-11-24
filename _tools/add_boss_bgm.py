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
          "lucifer1", "lucifer2", "usurper1", "usurper2",
          # 序章（2026-11-22，原件与来源在 prologue_ref/bgm_src/，convert_prologue_bgm.py 转码）
          "prologue_intro", "prologue_waves", "prologue_michael", "prologue_end",
          # 新手开局（2026-11-23，原件在 onboard_ref/bgm_src/，convert_onboard_bgm.py 转码）
          "onboard_intro", "onboard_flow"]
# 新手开局：黑屏里玩家悬在出生点上空，声音在玩家身上放；旁白配乐要压在配音下面（作者也说这首要放得很轻）
ONBOARD_VOLUME = {"onboard_intro": 0.45, "onboard_flow": 0.6}


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
        if t.startswith("prologue"):     # 序章过场镜头离玩家服务端位置可能很远（同 prologue_text 的配音）
            sounds["bgm." + t]["sounds"][0]["attenuation_distance"] = 1024
            # 给台词让位（用户 2026-11-22「台词声音太小了」）：开场配乐本来就轻，其余三首压低
            sounds["bgm." + t]["sounds"][0]["volume"] = 0.85 if t == "prologue_intro" else 0.55
        if t in ONBOARD_VOLUME:
            sounds["bgm." + t]["sounds"][0]["volume"] = ONBOARD_VOLUME[t]
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(sounds, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    # CC-BY 要求署名：资源包里随曲子放一份来源说明
    shutil.copyfile(os.path.join(REF, "SOURCES.md"), os.path.join(out, "credits.md"))
    print("boss bgm: %d tracks" % len(TRACKS))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../resourcepack")
