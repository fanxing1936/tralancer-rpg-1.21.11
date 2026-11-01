# -*- coding: utf-8 -*-
"""本地 1.21.11 实例的位置 —— 所有需要客户端 jar / 库 / Java 的脚本都从这里取。

以前每个脚本各写一份 HMCL 实例的绝对路径，换一台机器就得改十几处。
现在按顺序找第一个存在的实例；都不在时退回第一个候选，让调用方照旧在
打开 jar 那一刻报出清楚的 FileNotFoundError。

需要指向别处时，设环境变量即可，不用改代码：

    RPG_MC_GAME      .minecraft 根目录（含 libraries、assets）
    RPG_MC_VERSION   版本名（versions 下的文件夹名，也是 jar/json 的文件名）
    RPG_MC_JAVA      java 可执行文件；不设时用候选里的，或 PATH 上的 java
"""
import os
import shutil

# (game_dir, version_name, java, natives_dir_name)
CANDIDATES = [
    # 作者的 HMCL 实例
    (r"F:/筑梦 MCBE/HMCL启动器/新建文件夹", "1.21.11-Fabric",
     r"F:/筑梦 MCBE/MCA Selector/jre/bin/java.exe", "natives-windows-x86_64"),
    # PCL 实例
    (r"D:/minecraft/PCL启动器/.minecraft", "1.21.11-Fabric 0.19.3",
     None, "1.21.11-Fabric 0.19.3-natives"),
]


def _pick():
    game = os.environ.get("RPG_MC_GAME")
    version = os.environ.get("RPG_MC_VERSION")
    if game and version:
        return game, version, None, None
    for cand in CANDIDATES:
        g, v = game or cand[0], version or cand[1]
        if os.path.isfile("%s/versions/%s/%s.jar" % (g, v, v)):
            return g, v, cand[2], cand[3]
    return CANDIDATES[0]


GAME, VERSION, _java, _natives = _pick()
INST = "%s/versions/%s" % (GAME, VERSION)
JAR = "%s/%s.jar" % (INST, VERSION)
VJSON = "%s/%s.json" % (INST, VERSION)
LIBS = GAME + "/libraries"
NATIVES = INST + "/" + (_natives or "natives-windows-x86_64")
JAVA = (os.environ.get("RPG_MC_JAVA")
        or (_java if _java and os.path.isfile(_java) else None)
        or shutil.which("java") or "java")


if __name__ == "__main__":
    for k in ("GAME", "VERSION", "INST", "JAR", "VJSON", "NATIVES", "JAVA"):
        v = globals()[k]
        print("%-8s %s%s" % (k, v, "" if k == "VERSION" or os.path.exists(v) else "   [missing]"))
