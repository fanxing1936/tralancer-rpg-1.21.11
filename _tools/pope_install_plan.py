"""只读生成教皇测试实例同步计划；本脚本不复制、删除或写入实例。"""
import argparse
import hashlib
import json
from pathlib import Path

from pope_integrate_check import ROOT, OWN, SHARED

INSTANCE = Path(r"D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3")
OUT = ROOT / "_tools/pope_ref/m4/install_plan.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world", default="新的世界")
    args = parser.parse_args()
    rp = INSTANCE / "resourcepacks/tralancer-rpg"
    dp = INSTANCE / "saves" / args.world / "datapacks/tralancer-rpg"
    assert rp.is_dir() and dp.is_dir(), "目标必须为已有正式包目录"
    assert dp.resolve().is_relative_to((INSTANCE / "saves").resolve())

    def target(rel):
        prefix, suffix = rel.split("/", 1)
        return (rp if prefix == "resourcepack" else dp) / suffix

    entries = []
    for folder in OWN:
        for src in sorted((ROOT / folder).rglob("*")):
            if not src.is_file():
                continue
            rel = src.relative_to(ROOT).as_posix()
            dst = target(rel)
            new = src.read_bytes()
            old = dst.read_bytes() if dst.exists() else None
            entries.append({"source": rel, "target": str(dst), "kind": "owned_file",
                            "action": "unchanged" if old == new else "replace" if old is not None else "add",
                            "before_sha256": digest(old) if old is not None else None,
                            "after_sha256": digest(new)})
    for rel in SHARED:
        src = json.loads((ROOT / rel).read_text("utf-8"))
        dst = target(rel)
        old_bytes = dst.read_bytes()
        doc = json.loads(old_bytes)
        if "/tags/" in rel:
            old_vals = list(doc["values"])
            vals = [v for v in old_vals if not str(v).startswith("rpg:pope/")]
            if rel.endswith("load.json"):
                vals.append("rpg:pope/load")
            else:
                at = vals.index("rpg:command/tick_end") if "rpg:command/tick_end" in vals else len(vals)
                vals.insert(at, "rpg:pope/tick")
                vals.append("rpg:pope/tick_late")
            doc["values"] = vals
        else:
            prefixes = ("pope.", "subtitles.rpg.pope.")
            doc = {k: v for k, v in doc.items() if not k.startswith(prefixes)}
            doc.update({k: v for k, v in src.items() if k.startswith(prefixes)})
        new = (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        entries.append({"source": rel, "target": str(dst), "kind": "merge_pope_entries_only",
                        "action": "unchanged" if json.loads(old_bytes) == doc else "merge",
                        "before_sha256": digest(old_bytes), "after_sha256": digest(new)})
    counts = {key: sum(e["action"] == key for e in entries) for key in ("add", "replace", "merge", "unchanged")}
    report = {"status": "proposal_requires_user_approval", "instance": str(INSTANCE), "world": args.world,
              "resourcepack": str(rp), "datapack": str(dp), "counts": counts,
              "pending_writes": sum(e["action"] != "unchanged" for e in entries), "entries": entries,
              "client_written": False, "deletions": [],
              "policy": ["仅新增/替换教皇模型自己的文件，五个共享索引只合并教皇条目",
                         "不更新pope_fight、末影之心或任何其他怪物产物",
                         "执行前复核目标hash；先备份计划内的已有文件，再写入并逐字节验证",
                         "未获用户同步批准；本脚本只在仓库m4目录写计划"]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({"world": args.world, "counts": counts, "pending_writes": report["pending_writes"],
                      "client_written": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
