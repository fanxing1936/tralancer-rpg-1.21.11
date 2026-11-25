# -*- coding: utf-8 -*-
"""失乐园与主世界配乐转码：_tools/world_bgm_ref/bgm_src/ 的原件 → _tools/bgm_ref/{pl,ow}_*.ogg（Ogg Vorbis）。

    python convert_world_bgm.py

同 convert_onboard_bgm.py：只换格式，不剪辑、不改音量；原本就是 Vorbis 的原样拷贝。
来源与许可见 bgm_ref/SOURCES.md 的「失乐园与主世界」一节（2026-11-25 下载，用户同意）。
"""
import os
import shutil

import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "world_bgm_ref", "bgm_src")
DST = os.path.join(HERE, "bgm_ref")


def main():
    for f in sorted(os.listdir(SRC)):
        name, ext = os.path.splitext(f)
        if ext not in (".ogg", ".mp3", ".wav", ".flac"):
            continue
        out = os.path.join(DST, name + ".ogg")
        if ext == ".ogg":
            shutil.copyfile(os.path.join(SRC, f), out)
        else:
            data, sr = sf.read(os.path.join(SRC, f), always_2d=True, dtype="float32")
            # 分块写：libsndfile 的 Vorbis 编码器一次写入整首长曲会崩
            with sf.SoundFile(out, "w", sr, data.shape[1], format="OGG", subtype="VORBIS", compression_level=0.4) as fh:
                for i in range(0, len(data), 4096):
                    fh.write(data[i:i + 4096])
            assert abs(sf.info(out).duration - len(data) / float(sr)) < 0.1, name
        info = sf.info(out)
        assert info.channels == 2 and info.subtype == "VORBIS", (name, info.channels, info.subtype)
        print("%-12s %6.1f s  %d Hz  %5d KB" % (name, info.duration, info.samplerate, os.path.getsize(out) // 1024))


if __name__ == "__main__":
    main()
