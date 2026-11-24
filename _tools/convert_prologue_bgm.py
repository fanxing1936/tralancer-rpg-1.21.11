# -*- coding: utf-8 -*-
"""序章配乐转码：_tools/prologue_ref/bgm_src/ 的原件 → _tools/bgm_ref/prologue_*.ogg（Ogg Vorbis）。

    python convert_prologue_bgm.py

用户 2026-11-22 同意在本机装 soundfile（自带 libsndfile 1.2.2，能读 MP3、写 Vorbis），代替原来交给 Codex 的
CONVERT-BRIEF.md。要求同那份说明：只换格式，不剪辑、不淡入淡出、不改音量，保留原采样率与立体声；
prologue_end.ogg 原本就是 Vorbis，原样拷贝。来源与许可见 bgm_src/SOURCES.md。
"""
import os
import shutil

import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "prologue_ref", "bgm_src")
DST = os.path.join(HERE, "bgm_ref")
JOBS = [("prologue_intro.flac", "prologue_intro.ogg"), ("prologue_waves.mp3", "prologue_waves.ogg"),
        ("prologue_michael.wav", "prologue_michael.ogg")]
COPY = [("prologue_end.ogg", "prologue_end.ogg")]


def main():
    for a, b in JOBS:
        data, sr = sf.read(os.path.join(SRC, a), always_2d=True, dtype="float32")
        out = os.path.join(DST, b)
        # 分块写：libsndfile 的 Vorbis 编码器一次写入整首长曲会崩（实测）。
        # compression_level 0.4 ≈ Vorbis 质量 6（libsndfile 里 quality = 1 - level）
        with sf.SoundFile(out, "w", sr, data.shape[1], format="OGG", subtype="VORBIS", compression_level=0.4) as fh:
            for i in range(0, len(data), 4096):
                fh.write(data[i:i + 4096])
        info = sf.info(out)
        print("%-22s %6.1f s  %d Hz %dch  %5d KB" % (b, info.duration, info.samplerate, info.channels,
                                                    os.path.getsize(out) // 1024))
        assert abs(info.duration - len(data) / float(sr)) < 0.1, b
    for a, b in COPY:
        shutil.copyfile(os.path.join(SRC, a), os.path.join(DST, b))
        info = sf.info(os.path.join(DST, b))
        print("%-22s %6.1f s  copied as is" % (b, info.duration))


if __name__ == "__main__":
    main()
