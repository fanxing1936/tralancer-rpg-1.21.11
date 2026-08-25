# -*- coding: utf-8 -*-
"""Load the data pack on a real 1.21.11 dedicated server and read the console.

The server parses every function line, loot table, item modifier and advancement
at start-up, so anything the pack gets wrong shows up here with a file and line
number.  Runs headless -- no window, no client.
"""

import io
import json
import os
import re
import subprocess
import sys
import time

GAME = r"F:/筑梦 MCBE/HMCL启动器/新建文件夹"
INST = GAME + "/versions/1.21.11-Fabric"
VJSON = INST + "/1.21.11-Fabric.json"
JAVA = r"F:/筑梦 MCBE/MCA Selector/jre/bin/java.exe"
LIBS = GAME + "/libraries"

RUNDIR = sys.argv[1]
WAIT = int(sys.argv[2]) if len(sys.argv) > 2 else 240

SKIP_LIB = ("sponge-mixin", "fabric-loader", "mixinextras", "tiny-mappings",
            "tiny-remapper", "access-widener", "lwjgl", "text2speech", "jinput")


def maven_path(name):
    parts = name.split(":")
    group, artifact, version = parts[0], parts[1], parts[2]
    classifier = parts[3] if len(parts) > 3 else None
    fn = "%s-%s%s.jar" % (artifact, version, "-" + classifier if classifier else "")
    return os.path.join(LIBS, group.replace(".", "/"), artifact, version, fn)


def classpath(doc):
    out = []
    for lib in doc["libraries"]:
        name = lib["name"]
        if any(s in name for s in SKIP_LIB):
            continue
        p = maven_path(name)
        if os.path.isfile(p):
            out.append(p)
    out.append(INST + "/1.21.11-Fabric.jar")
    return out


def main():
    doc = json.load(io.open(VJSON, encoding="utf-8"))
    cmd = [JAVA, "-Xmx2G", "-Dfile.encoding=UTF-8",
           "-cp", os.pathsep.join(classpath(doc)),
           "net.minecraft.server.Main", "--nogui",
           "--universe", RUNDIR, "--world", "packtest"]

    print("starting dedicated 1.21.11 server...")
    proc = subprocess.Popen(cmd, cwd=RUNDIR, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            bufsize=1, universal_newlines=True,
                            encoding="utf-8", errors="replace")

    lines = []
    deadline = time.time() + WAIT
    done = False
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        lines.append(line.rstrip())
        if 'For help, type "help"' in line or "Done (" in line:
            done = True
            break
    probes = ["datapack list", "function rpg:command/index", "function rpg:command/tick",
              "function rpg:item/sword/legend/legend1",
              "function rpg:entities/warden/warden",
              "function rpg:command/tick_end",
              "gamerule send_command_feedback true",
              "execute in minecraft:overworld run forceload add 0 0"]
    extra = os.environ.get("MC_PROBE_FILE")
    if extra and os.path.isfile(extra):
        probes += [l.strip() for l in io.open(extra, encoding="utf-8")
                   if l.strip() and not l.startswith("#")]
    probes.append("stop")

    if done:
        for c in probes:
            lines.append(">>> " + c)
            try:
                proc.stdin.write(c + "\n")
                proc.stdin.flush()
            except Exception:
                pass
            # A sprint runs asynchronously; leave enough time for its result
            # before issuing the next probe so benchmark samples do not mix.
            sprint_wait = float(os.environ.get("MC_SPRINT_WAIT", "5"))
            time.sleep(sprint_wait if c.startswith("tick sprint ") else 0.7)
        # drain to EOF -- the console replies were buffered while we typed
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            lines.append(line.rstrip())
    if proc.poll() is None:
        proc.kill()

    txt = "\n".join(lines)
    print("server reached 'Done': %s   (%d console lines)" % (done, len(lines)))

    bad = [l for l in lines if re.search(
        r"Whilst parsing|Parsing error|Failed to |Couldn't |Unknown |Invalid |"
        r"ERROR|/WARN|Exception|Ambiguity|Missing", l)]
    ignore = re.compile(r"authlib|Realms|EULA|user properties|SignedJWT|"
                        r"secure profile|offline mode|no-op|Advanced terminal|"
                        r"level seed|Ambiguity between arguments", re.I)
    bad = [l for l in bad if not ignore.search(l)]
    print("\n--- server complaints (%d) ---" % len(bad))
    for l in bad[:80]:
        print("  " + l[:220])
    if not bad:
        print("  (none)")

    print("\n--- full console ---")
    for l in lines:
        print("  " + l[:220])


if __name__ == "__main__":
    main()
