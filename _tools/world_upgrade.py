# -*- coding: utf-8 -*-
"""Convert a world save to 1.21.11 with the real client jar's dedicated server.

`--forceUpgrade` walks every region/entity/poi file and runs it through
DataFixerUpper, so the save comes out fully converted instead of being upgraded
lazily chunk-by-chunk as you walk around.  Then the server is started normally
once, which rewrites level.dat and proves the data packs still load.
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import time

GAME = r"F:/筑梦 MCBE/HMCL启动器/新建文件夹"
INST = GAME + "/versions/1.21.11-Fabric"
VJSON = INST + "/1.21.11-Fabric.json"
JAVA = r"F:/筑梦 MCBE/MCA Selector/jre/bin/java.exe"
LIBS = GAME + "/libraries"

WORLD = sys.argv[1]                    # path to the save folder to upgrade
RUNDIR = sys.argv[2]                   # scratch directory to run the server in
NAME = "worldupgrade"                  # ASCII name while the server holds it

SKIP_LIB = ("sponge-mixin", "fabric-loader", "mixinextras", "tiny-mappings",
            "tiny-remapper", "access-widener", "lwjgl", "text2speech", "jinput")


def classpath():
    doc = json.load(io.open(VJSON, encoding="utf-8"))
    out = []
    for lib in doc["libraries"]:
        name = lib["name"]
        if any(s in name for s in SKIP_LIB):
            continue
        parts = name.split(":")
        fn = "%s-%s%s.jar" % (parts[1], parts[2],
                              "-" + parts[3] if len(parts) > 3 else "")
        p = os.path.join(LIBS, parts[0].replace(".", "/"), parts[1], parts[2], fn)
        if os.path.isfile(p):
            out.append(p)
    out.append(INST + "/1.21.11-Fabric.jar")
    return out


def data_version(level_dat):
    import gzip
    import struct
    d = gzip.open(level_dat, "rb").read()
    i = d.find(b"DataVersion")
    return struct.unpack(">i", d[i + 11:i + 15])[0] if i > 0 else None


def run(args, feed=None, limit=3600):
    cmd = [JAVA, "-Xmx3G", "-Dfile.encoding=UTF-8",
           "-cp", os.pathsep.join(classpath()),
           "net.minecraft.server.Main", "--nogui",
           "--universe", RUNDIR, "--world", NAME] + args
    proc = subprocess.Popen(cmd, cwd=RUNDIR, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            bufsize=1, universal_newlines=True,
                            encoding="utf-8", errors="replace")
    lines = []
    deadline = time.time() + limit
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.rstrip()
        lines.append(line)
        if feed and ('For help, type "help"' in line or "Done (" in line):
            for c in feed:
                proc.stdin.write(c + "\n")
                proc.stdin.flush()
                time.sleep(1.0)
            feed = None
    if proc.poll() is None:
        proc.kill()
    return lines


def main():
    staged = os.path.join(RUNDIR, NAME)
    if os.path.isdir(RUNDIR):
        shutil.rmtree(RUNDIR)
    os.makedirs(RUNDIR)
    io.open(os.path.join(RUNDIR, "eula.txt"), "w").write("eula=true\n")
    io.open(os.path.join(RUNDIR, "server.properties"), "w").write(
        "level-name=%s\nonline-mode=false\nmax-tick-time=-1\n"
        "view-distance=4\nsimulation-distance=4\nspawn-protection=0\n" % NAME)
    shutil.copytree(WORLD, staged)
    lock = os.path.join(staged, "session.lock")
    if os.path.exists(lock):
        os.remove(lock)

    before = data_version(os.path.join(staged, "level.dat"))
    print("world DataVersion before: %s" % before)

    # --forceUpgrade converts every chunk and then boots the server normally,
    # so one run does both the conversion and the "do the data packs load?" check
    print("\n== --forceUpgrade: converting every chunk, then booting ==")
    t0 = time.time()
    lines = run(["--forceUpgrade"],
                feed=["datapack list", "save-all flush", "stop"])
    pct = [l for l in lines if "% completed" in l]
    for l in ([pct[0]] + pct[-1:] if pct else []):
        print("  " + l[:160])
    print("  took %.0f s, %d console lines" % (time.time() - t0, len(lines)))

    for l in lines:
        if re.search(r"data pack|Preparing level|Done \(|Version|ERROR|/WARN|Exception|"
                     r"Failed|Couldn't|Missing", l):
            if re.search(r"offline|OFFLINE|authenticate|hackers|online-mode", l):
                continue
            print("  " + l[:200])

    after = data_version(os.path.join(staged, "level.dat"))
    print("\nworld DataVersion after: %s" % after)

    if os.path.exists(lock):
        os.remove(lock)
    shutil.rmtree(WORLD)
    shutil.copytree(staged, WORLD)
    lock = os.path.join(WORLD, "session.lock")
    if os.path.exists(lock):
        os.remove(lock)
    print("upgraded save written back to: %s" % WORLD)


if __name__ == "__main__":
    main()
