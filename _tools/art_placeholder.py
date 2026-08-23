# -*- coding: utf-8 -*-
"""还没画好的贴图，先拿原版的顶上 —— 而且是**逐字节复制**。

为什么不自己生成：上一版的玛门占位图是我用 png_tool 重新编码出来的，
然后又用同一个 png_tool 读回来"验证"通过 —— 那是自己证明自己，什么也没说明。
客户端读不读得动是另一回事。这里改成从原版 jar 里把 PNG **原样搬过来**，
连一个字节都不重编：那些图客户端每天都在读，不可能不认。

代价是占位图长得和原版一样（金色的玛门弓变回木弓的样子），但"看得见"
比"好看"重要 —— 缺失材质的紫黑格会让人以为整条模型链断了，
而实际上断的可能只是一张图。

**已经存在的文件一律不碰。**作者把真图放进去之后，这个脚本就再也不会覆盖它。
"""
import io
import os
import shutil
import sys
import zipfile

RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
JAR = (sys.argv[2] if len(sys.argv) > 2 else
       r"F:/筑梦 MCBE/HMCL启动器/新建文件夹/versions/1.21.11-Fabric/1.21.11-Fabric.jar")

OUT = os.path.join(RP, "assets/rpg/textures/item")

# 我们的名字 -> 拿原版哪一张顶着
WANT = {
    # 玛门的弓：四个拉弓阶段
    "mammon_bow": "bow",
    "mammon_bow_pulling_0": "bow_pulling_0",
    "mammon_bow_pulling_1": "bow_pulling_1",
    "mammon_bow_pulling_2": "bow_pulling_2",
    # 七柱契约之书
    "pact_lucifer": "enchanted_book",
    "pact_leviathan": "enchanted_book",
    "pact_abaddon": "enchanted_book",
    "pact_beelzebub": "enchanted_book",
    "pact_samael": "enchanted_book",
    "pact_belial": "enchanted_book",
    "pact_mammon": "enchanted_book",
}


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    if not os.path.isfile(JAR):
        print("art placeholder: 找不到原版 jar，跳过")
        return
    made, kept = 0, 0
    with zipfile.ZipFile(JAR) as z:
        for name, src in sorted(WANT.items()):
            dst = os.path.join(OUT, name + ".png")
            if os.path.isfile(dst):
                kept += 1
                continue
            try:
                data = z.read("assets/minecraft/textures/item/%s.png" % src)
            except KeyError:
                print("  原版里没有 %s.png，跳过" % src)
                continue
            with io.open(dst, "wb") as fh:
                fh.write(data)
            made += 1
    print("art placeholder: 新补 %d 张，作者已有的 %d 张原样保留" % (made, kept))


if __name__ == "__main__":
    main()
