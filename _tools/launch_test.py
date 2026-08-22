# -*- coding: utf-8 -*-
"""Boot the real 1.21.11 client with a resource pack selected, then read the log.

The client bakes every model and stitches every atlas during the startup
resource reload, so reaching the title screen is enough to surface any
"Unable to find texture", broken item definition or bad model.
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

PACK = sys.argv[1] if len(sys.argv) > 1 else "file/rpg_resourcepack_claude"
WORLD = os.environ.get("MC_TEST_WORLD")   # boot straight into this save
WAIT = int(sys.argv[2]) if len(sys.argv) > 2 else 150
# run out of a scratch game directory: the user's own instance may be open, and
# a throwaway dir also means no mods to confuse the resource-reload log
RUNDIR = sys.argv[3] if len(sys.argv) > 3 else INST


def maven_path(name):
    parts = name.split(":")
    group, artifact, version = parts[0], parts[1], parts[2]
    classifier = parts[3] if len(parts) > 3 else None
    fn = "%s-%s%s.jar" % (artifact, version, "-" + classifier if classifier else "")
    return os.path.join(LIBS, group.replace(".", "/"), artifact, version, fn)


def rules_ok(lib):
    for rule in lib.get("rules", []):
        os_name = (rule.get("os") or {}).get("name")
        allow = rule["action"] == "allow"
        matches = os_name in (None, "windows")
        if allow and not matches:
            return False
        if not allow and matches:
            return False
    return True


def classpath(doc):
    out = []
    for lib in doc["libraries"]:
        if not rules_ok(lib):
            continue
        p = maven_path(lib["name"])
        if os.path.isfile(p):
            out.append(p)
        else:
            print("  [warn] missing library %s" % lib["name"])
    out.append(INST + "/1.21.11-Fabric.jar")
    return out


def flatten_args(args):
    out = []
    for a in args:
        if isinstance(a, str):
            out.append(a)
        elif isinstance(a, dict) and rules_ok(a):
            v = a.get("value")
            out.extend(v if isinstance(v, list) else [v])
    return out


def set_pack():
    path = RUNDIR + "/options.txt"
    lines = io.open(path, encoding="utf-8").read().split("\n")
    out = []
    for ln in lines:
        if ln.startswith("resourcePacks:"):
            ln = 'resourcePacks:["vanilla","%s"]' % PACK
        elif ln.startswith("pauseOnLostFocus:"):
            ln = "pauseOnLostFocus:false"
        out.append(ln)
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("selected resource pack: %s" % PACK)


def main():
    doc = json.load(io.open(VJSON, encoding="utf-8"))
    cp = classpath(doc)
    set_pack()

    log = RUNDIR + "/logs/latest.log"
    if os.path.exists(log):
        os.remove(log)

    subst = {
        "${natives_directory}": INST + "/natives-windows-x86_64",
        "${launcher_name}": "claude", "${launcher_version}": "1",
        "${classpath}": os.pathsep.join(cp),
        "${auth_player_name}": "PackTest",
        "${version_name}": "1.21.11-Fabric",
        "${game_directory}": RUNDIR,
        "${assets_root}": GAME + "/assets",
        "${assets_index_name}": doc["assetIndex"]["id"],
        "${auth_uuid}": "00000000000000000000000000000001",
        "${auth_access_token}": "0", "${clientid}": "0", "${auth_xuid}": "0",
        "${user_type}": "legacy", "${version_type}": "release",
        "${resolution_width}": "854", "${resolution_height}": "480",
    }

    def sub(s):
        for k, v in subst.items():
            s = s.replace(k, v)
        return s

    jvm = [sub(a) for a in flatten_args(doc["arguments"]["jvm"])]

    # drop quickPlay/demo switches and any flag whose placeholder we did not
    # fill in -- the client refuses to start if more than one is present
    raw = [sub(a) for a in flatten_args(doc["arguments"]["game"])]
    game, i = [], 0
    while i < len(raw):
        a = raw[i]
        val = raw[i + 1] if i + 1 < len(raw) and not raw[i + 1].startswith("--") else None
        if a.startswith("--quickPlay") or a == "--demo" or "${" in a or (val and "${" in val):
            i += 2 if val is not None else 1
            continue
        game.append(a)
        if val is not None:
            game.append(val)
            i += 2
        else:
            i += 1
    if WORLD:
        game += ["--quickPlayPath", os.path.join(RUNDIR, "quickplay.json"),
                 "--quickPlaySingleplayer", WORLD]
    print("game args: %s" % " ".join(game))
    cmd = [JAVA] + jvm + ["-Xmx2G"] + [doc["mainClass"]] + game

    print("launching 1.21.11 (Fabric)...")
    proc = subprocess.Popen(cmd, cwd=RUNDIR,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    deadline = time.time() + WAIT
    ready = False
    while time.time() < deadline:
        time.sleep(5)
        if proc.poll() is not None:
            print("client exited early with code %s" % proc.returncode)
            break
        if os.path.exists(log):
            txt = io.open(log, encoding="utf-8", errors="replace").read()
            marker = ("Time elapsed" if WORLD else "textures/atlas/items.png-atlas")
            if "Created: " in txt and marker in txt:
                ready = True
                time.sleep(8)
                break
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except Exception:
            proc.kill()
    print("resource reload reached: %s" % ready)

    txt = io.open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    bad = [l for l in txt.split("\n")
           if re.search(r"Unable to find|Failed to load|Couldn't|Missing|Invalid|"
                        r"Exception|ERROR|Error loading|not found", l)
           and not re.search(r"iris|sodium|shader|Distant|OptiFine|Realms|"
                             r"authlib|Narrator|telemetry|is_alive", l, re.I)]
    print("\n--- suspicious log lines (%d) ---" % len(bad))
    for l in bad[:60]:
        print("  " + l.strip()[:200])
    atlases = [l for l in txt.split("\n") if "Created: " in l and "atlas" in l]
    print("\n--- atlases built (%d) ---" % len(atlases))
    for l in atlases[:20]:
        print("  " + l.split("]: ")[-1])


if __name__ == "__main__":
    main()
