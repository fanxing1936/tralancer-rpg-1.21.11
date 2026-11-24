# -*- coding: utf-8 -*-
"""新手开局配乐转码：_tools/onboard_ref/bgm_src/ 的原件 → _tools/bgm_ref/onboard_*.ogg（Ogg Vorbis）。

    python convert_onboard_bgm.py

同 convert_prologue_bgm.py：只换格式，不剪辑、不改音量；原本就是 Vorbis 的原样拷贝。
来源与许可见 bgm_ref/SOURCES.md 的「新手开局」一节（2026-11-23 下载，用户同意）。
"""
import os
import shutil

import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "onboard_ref", "bgm_src")
DST = os.path.join(HERE, "bgm_ref")
JOBS = [("onboard_flow.mp3", "onboard_flow.ogg")]
COPY = [("onboard_intro.ogg", "onboard_intro.ogg")]


def main():
    for a, b in JOBS:
        data, sr = sf.read(os.path.join(SRC, a), always_2d=True, dtype="float32")
        out = os.path.join(DST, b)
        # 分块写：libsndfile 的 Vorbis 编码器一次写入整首长曲会崩
        with sf.SoundFile(out, "w", sr, data.shape[1], format="OGG", subtype="VORBIS", compression_level=0.4) as fh:
            for i in range(0, len(data), 4096):
                fh.write(data[i:i + 4096])
        info = sf.info(out)
        print("%-20s %6.1f s  %d Hz %dch  %5d KB" % (b, info.duration, info.samplerate, info.channels,
                                                  os.path.getsize(out) // 1024))
        assert abs(info.duration - len(data) / float(sr)) < 0.1, b
    for a, b in COPY:
        shutil.copyfile(os.path.join(SRC, a), os.path.join(DST, b))
        info = sf.info(os.path.join(DST, b))
        print("%-20s %6.1f s  copied as is" % (b, info.duration))


if __name__ == "__main__":
    main()
